"""
Scenario Branch Manager
Run multiple "what-if" variants of the same simulation in parallel and compare outcomes.

Workflow
--------
1. prepare_simulation() as usual → base simulation is READY
2. create_branch_experiment(base_simulation_id, branches)
   - Copies the base dir N times (no re-generation cost)
   - Patches event_config in each copy's simulation_config.json
3. run_branch_experiment(experiment_id, ...)
   - Starts all branches via SimulationRunner in parallel threads
4. compare_branches(experiment_id)
   - Computes per-round sentiment trajectories and finds divergence point
"""

from __future__ import annotations

import json
import os
import shutil
import threading
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..config import Config
from ..utils.logger import get_logger
from ..utils.security import safe_id
from .simulation_runner import SimulationRunner, RunnerStatus

logger = get_logger("mirofish.scenario_branch")

# Positive action types used to compute per-round sentiment ratio
_POSITIVE_ACTIONS = {"CREATE_POST", "LIKE_POST", "LIKE_COMMENT", "FOLLOW", "QUOTE_POST"}
_NEGATIVE_ACTIONS = {"DISLIKE_POST", "DISLIKE_COMMENT", "MUTE"}


# ── Data models ────────────────────────────────────────────────────────────────

@dataclass
class ScenarioBranch:
    """
    One what-if variant of the base simulation.

    ``injection`` is a *partial* override of ``event_config`` inside
    ``simulation_config.json``.  Only the keys present in ``injection``
    are overwritten; everything else is inherited from the base.

    Example
    -------
    ScenarioBranch(
        name="Price +10%",
        description="Announce a moderate price increase",
        injection={
            "initial_posts": [{"content": "We are raising prices by 10%.",
                               "poster_type": "Official"}],
            "narrative_direction": "Moderate public concern",
        }
    )
    """
    name: str
    description: str
    injection: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BranchResult:
    """Outcome data for a single branch after the simulation completes."""
    branch_name: str
    branch_description: str
    simulation_id: str
    status: str                             # RunnerStatus value
    rounds_completed: int
    action_counts: Dict[str, int]           # {action_type: count}
    sentiment_per_round: List[float]        # positive_ratio per round (0.0–1.0)
    top_posts: List[str]                    # first 3 CREATE_POST contents
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BranchComparisonResult:
    """Comparison of all branches in one experiment."""
    experiment_id: str
    base_simulation_id: str
    branches: List[BranchResult]
    divergence_round: Optional[int]         # first round where max spread > threshold
    winner: Optional[str]                   # branch with highest final sentiment
    summary: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "base_simulation_id": self.base_simulation_id,
            "branches": [b.to_dict() for b in self.branches],
            "divergence_round": self.divergence_round,
            "winner": self.winner,
            "summary": self.summary,
            "created_at": self.created_at,
        }


# ── Manager ────────────────────────────────────────────────────────────────────

class ScenarioBranchManager:
    """
    Create and run parallel scenario branches from a single prepared simulation.
    """

    EXPERIMENTS_DIR = os.path.join(Config.UPLOAD_FOLDER, "experiments")
    SIMULATIONS_DIR = os.path.join(Config.UPLOAD_FOLDER, "simulations")

    # Sentiment divergence threshold: if the range across branches exceeds this
    # value in a round, that round is flagged as the divergence point.
    DIVERGENCE_THRESHOLD = 0.15

    def __init__(self) -> None:
        os.makedirs(self.EXPERIMENTS_DIR, exist_ok=True)

    # ── Public API ─────────────────────────────────────────────────────────────

    def create_branch_experiment(
        self,
        base_simulation_id: str,
        branches: List[ScenarioBranch],
    ) -> Dict[str, Any]:
        """
        Clone the base simulation directory once per branch and patch each
        copy's ``event_config`` with the branch-specific injection.

        Returns the experiment manifest dict (also saved to disk).

        Raises
        ------
        ValueError
            If the base simulation directory or its config file does not exist,
            or if fewer than 2 branches are supplied.
        """
        if len(branches) < 2:
            raise ValueError("Provide at least 2 branches for a meaningful comparison.")

        base_dir = os.path.join(self.SIMULATIONS_DIR, base_simulation_id)
        base_config_path = os.path.join(base_dir, "simulation_config.json")

        if not os.path.isdir(base_dir):
            raise ValueError(f"Base simulation not found: {base_simulation_id}")
        if not os.path.isfile(base_config_path):
            raise ValueError(
                f"Base simulation has no config (run /prepare first): {base_simulation_id}"
            )

        with open(base_config_path, encoding="utf-8") as fh:
            base_config = json.load(fh)

        experiment_id = f"exp_{uuid.uuid4().hex[:10]}"
        branch_simulation_ids: List[str] = []

        for branch in branches:
            branch_sim_id = f"sim_{uuid.uuid4().hex[:12]}"
            branch_dir = os.path.join(self.SIMULATIONS_DIR, branch_sim_id)

            # Copy entire base directory (profiles, state, config)
            shutil.copytree(base_dir, branch_dir)
            logger.info(f"Cloned base sim → {branch_sim_id} for branch '{branch.name}'")

            # Patch event_config with the branch injection
            patched_config = self._patch_event_config(base_config, branch.injection)
            patched_config_path = os.path.join(branch_dir, "simulation_config.json")
            with open(patched_config_path, "w", encoding="utf-8") as fh:
                json.dump(patched_config, fh, ensure_ascii=False, indent=2)

            branch_simulation_ids.append(branch_sim_id)

        manifest = {
            "experiment_id": experiment_id,
            "base_simulation_id": base_simulation_id,
            "created_at": datetime.now().isoformat(),
            "status": "created",
            "branches": [
                {
                    "name": b.name,
                    "description": b.description,
                    "injection": b.injection,
                    "simulation_id": sid,
                }
                for b, sid in zip(branches, branch_simulation_ids)
            ],
        }

        self._save_experiment(manifest)
        logger.info(
            f"Created experiment {experiment_id} with {len(branches)} branches"
        )
        return manifest

    def run_branch_experiment(
        self,
        experiment_id: str,
        platform: str = "parallel",
        max_rounds: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Start all branch simulations in parallel threads and wait for them.

        Returns the updated experiment manifest.
        """
        manifest = self._load_experiment(experiment_id)
        if manifest is None:
            raise ValueError(f"Experiment not found: {experiment_id}")

        manifest["status"] = "running"
        manifest["started_at"] = datetime.now().isoformat()
        self._save_experiment(manifest)

        errors: Dict[str, str] = {}
        threads: List[threading.Thread] = []

        def _run_branch(sim_id: str) -> None:
            try:
                SimulationRunner.start_simulation(
                    simulation_id=sim_id,
                    platform=platform,
                    max_rounds=max_rounds,
                )
                logger.info(f"Branch {sim_id} started")
            except Exception as exc:
                logger.error(f"Branch {sim_id} failed to start: {exc}")
                errors[sim_id] = str(exc)

        for branch_meta in manifest["branches"]:
            t = threading.Thread(
                target=_run_branch,
                args=(branch_meta["simulation_id"],),
                daemon=True,
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        if errors:
            manifest["status"] = "partial_failure"
            manifest["errors"] = errors
        else:
            manifest["status"] = "running_branches"

        self._save_experiment(manifest)
        return manifest

    def compare_branches(
        self,
        experiment_id: str,
        divergence_threshold: float = DIVERGENCE_THRESHOLD,
    ) -> BranchComparisonResult:
        """
        Collect run-state data for all branches and compute comparison metrics.

        Can be called while branches are still running (returns partial data)
        or after they have finished.
        """
        manifest = self._load_experiment(experiment_id)
        if manifest is None:
            raise ValueError(f"Experiment not found: {experiment_id}")

        branch_results: List[BranchResult] = []

        for branch_meta in manifest["branches"]:
            sim_id = branch_meta["simulation_id"]
            result = self._collect_branch_result(
                sim_id=sim_id,
                branch_name=branch_meta["name"],
                branch_description=branch_meta["description"],
            )
            branch_results.append(result)

        divergence_round = self._find_divergence_round(branch_results, divergence_threshold)
        winner = self._find_winner(branch_results)
        summary = self._build_summary(branch_results, divergence_round, winner)

        comparison = BranchComparisonResult(
            experiment_id=experiment_id,
            base_simulation_id=manifest["base_simulation_id"],
            branches=branch_results,
            divergence_round=divergence_round,
            winner=winner,
            summary=summary,
        )

        # Persist comparison result
        exp_dir = os.path.join(self.EXPERIMENTS_DIR, experiment_id)
        os.makedirs(exp_dir, exist_ok=True)
        with open(os.path.join(exp_dir, "comparison.json"), "w", encoding="utf-8") as fh:
            json.dump(comparison.to_dict(), fh, ensure_ascii=False, indent=2)

        return comparison

    def get_experiment(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        """Return the raw experiment manifest (or None if not found)."""
        return self._load_experiment(experiment_id)

    def list_experiments(self) -> List[Dict[str, Any]]:
        """List all experiment manifests sorted by creation time (newest first)."""
        results = []
        if not os.path.isdir(self.EXPERIMENTS_DIR):
            return results
        for name in os.listdir(self.EXPERIMENTS_DIR):
            manifest = self._load_experiment(name)
            if manifest:
                results.append(manifest)
        results.sort(key=lambda m: m.get("created_at", ""), reverse=True)
        return results

    # ── Private helpers ────────────────────────────────────────────────────────

    @staticmethod
    def _patch_event_config(
        base_config: Dict[str, Any],
        injection: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Return a deep-copy of base_config with event_config patched by injection."""
        import copy
        patched = copy.deepcopy(base_config)
        event_cfg = patched.setdefault("event_config", {})
        for key, value in injection.items():
            event_cfg[key] = value
        return patched

    def _collect_branch_result(
        self,
        sim_id: str,
        branch_name: str,
        branch_description: str,
    ) -> BranchResult:
        """Load run state + actions for one branch and compute metrics."""
        run_state = SimulationRunner.get_run_state(sim_id)

        if run_state is None:
            return BranchResult(
                branch_name=branch_name,
                branch_description=branch_description,
                simulation_id=sim_id,
                status="not_started",
                rounds_completed=0,
                action_counts={},
                sentiment_per_round=[],
                top_posts=[],
            )

        rounds_completed = run_state.current_round
        status = run_state.runner_status.value if run_state.runner_status else "unknown"

        # Load all recorded actions
        try:
            all_actions = SimulationRunner.get_all_actions(sim_id)
        except Exception as exc:
            logger.warning(f"Could not load actions for {sim_id}: {exc}")
            all_actions = []

        action_counts: Dict[str, int] = {}
        posts_by_round: Dict[int, List[str]] = {}
        top_posts: List[str] = []

        for action in all_actions:
            atype = action.get("action_type", "UNKNOWN")
            action_counts[atype] = action_counts.get(atype, 0) + 1

            # Collect CREATE_POST content for top_posts
            if atype == "CREATE_POST":
                content = (
                    action.get("action_args", {}).get("content", "")
                    or action.get("result", "")
                )
                rnd = action.get("round_num", 0)
                posts_by_round.setdefault(rnd, []).append(content)
                if len(top_posts) < 3 and content:
                    top_posts.append(content[:200])

        # Compute sentiment_per_round: ratio of positive to (positive + negative) actions
        sentiment_per_round = self._compute_sentiment_trajectory(all_actions, rounds_completed)

        return BranchResult(
            branch_name=branch_name,
            branch_description=branch_description,
            simulation_id=sim_id,
            status=status,
            rounds_completed=rounds_completed,
            action_counts=action_counts,
            sentiment_per_round=sentiment_per_round,
            top_posts=top_posts,
        )

    @staticmethod
    def _compute_sentiment_trajectory(
        actions: List[Dict[str, Any]],
        total_rounds: int,
    ) -> List[float]:
        """
        Return a list of per-round sentiment ratios.

        Sentiment ratio = positive_actions / (positive_actions + negative_actions).
        Rounds with no actions default to 0.5 (neutral).
        """
        per_round: Dict[int, Dict[str, int]] = {}

        for action in actions:
            rnd = action.get("round_num", 0)
            atype = action.get("action_type", "")
            bucket = per_round.setdefault(rnd, {"pos": 0, "neg": 0})
            if atype in _POSITIVE_ACTIONS:
                bucket["pos"] += 1
            elif atype in _NEGATIVE_ACTIONS:
                bucket["neg"] += 1

        trajectory: List[float] = []
        for r in range(total_rounds + 1):
            bucket = per_round.get(r, {"pos": 0, "neg": 0})
            total = bucket["pos"] + bucket["neg"]
            ratio = bucket["pos"] / total if total > 0 else 0.5
            trajectory.append(round(ratio, 3))

        return trajectory

    @staticmethod
    def _find_divergence_round(
        results: List[BranchResult],
        threshold: float,
    ) -> Optional[int]:
        """
        Find the first round where the spread of sentiment ratios across all
        branches exceeds ``threshold``.
        """
        if not results:
            return None

        # Align all trajectories to the shortest length
        min_len = min(len(r.sentiment_per_round) for r in results)
        if min_len == 0:
            return None

        for rnd in range(min_len):
            values = [r.sentiment_per_round[rnd] for r in results]
            if max(values) - min(values) > threshold:
                return rnd

        return None

    @staticmethod
    def _find_winner(results: List[BranchResult]) -> Optional[str]:
        """Return the branch name with the highest final-round sentiment ratio."""
        if not results:
            return None
        with_data = [r for r in results if r.sentiment_per_round]
        if not with_data:
            return None
        return max(with_data, key=lambda r: r.sentiment_per_round[-1]).branch_name

    @staticmethod
    def _build_summary(
        results: List[BranchResult],
        divergence_round: Optional[int],
        winner: Optional[str],
    ) -> str:
        lines = [f"Compared {len(results)} scenario branches."]
        if divergence_round is not None:
            lines.append(f"Scenarios diverged at round {divergence_round}.")
        else:
            lines.append("No significant divergence detected within the simulated period.")
        if winner:
            lines.append(f"Highest final sentiment: '{winner}'.")
        for r in results:
            final = r.sentiment_per_round[-1] if r.sentiment_per_round else 0.5
            lines.append(
                f"  • {r.branch_name}: {r.rounds_completed} rounds, "
                f"final sentiment {final:.2f}, "
                f"{sum(r.action_counts.values())} total actions"
            )
        return " ".join(lines)

    # ── Persistence ────────────────────────────────────────────────────────────

    def _experiment_path(self, experiment_id: str) -> str:
        exp_dir = os.path.join(self.EXPERIMENTS_DIR, experiment_id)
        os.makedirs(exp_dir, exist_ok=True)
        return os.path.join(exp_dir, "manifest.json")

    def _save_experiment(self, manifest: Dict[str, Any]) -> None:
        path = self._experiment_path(manifest["experiment_id"])
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, ensure_ascii=False, indent=2)
        os.replace(tmp, path)

    def _load_experiment(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        path = self._experiment_path(experiment_id)
        if not os.path.isfile(path):
            return None
        try:
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)
        except Exception as exc:
            logger.error(f"Failed to load experiment {experiment_id}: {exc}")
            return None
