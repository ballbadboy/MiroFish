"""
Flask blueprint exposing the Data Router via REST.

Routes (all under /api/router):
    POST   /subscribe                register a simulation's tag interest
    DELETE /subscribe/<sim_id>       remove a subscription
    GET    /subscribe/<sim_id>       fetch a single subscription
    GET    /subscriptions            list every subscription
    POST   /route                    fetch from a connector then route
    GET    /routings?limit=          tail the routing log
    GET    /stats                    aggregate stats
"""
from __future__ import annotations

from flask import Blueprint, jsonify, request

from ..connectors import registry
from ..services.data_router import DataRouter

router_bp = Blueprint("data_router", __name__, url_prefix="/api/router")

# Module-level singleton — DataRouter is stateless apart from on-disk files.
_router = DataRouter()


@router_bp.route("/subscribe", methods=["POST"])
def subscribe():
    body = request.get_json(silent=True) or {}
    simulation_id = body.get("simulation_id")
    tag_filters = body.get("tag_filters")
    description = body.get("description", "") or ""

    if not simulation_id or tag_filters is None:
        return jsonify({
            "success": False,
            "error": "simulation_id and tag_filters are required",
        }), 400

    try:
        sub = _router.subscribe(
            simulation_id=simulation_id,
            tag_filters=tag_filters,
            description=description,
        )
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400

    return jsonify({"success": True, "data": sub.to_dict()}), 201


@router_bp.route("/subscribe/<sim_id>", methods=["DELETE"])
def unsubscribe(sim_id: str):
    removed = _router.unsubscribe(sim_id)
    if not removed:
        return jsonify({"success": False, "error": "Subscription not found"}), 404
    return jsonify({"success": True, "data": {"simulation_id": sim_id}})


@router_bp.route("/subscribe/<sim_id>", methods=["GET"])
def get_subscription(sim_id: str):
    sub = _router.get_subscription(sim_id)
    if sub is None:
        return jsonify({"success": False, "error": "Subscription not found"}), 404
    return jsonify({"success": True, "data": sub.to_dict()})


@router_bp.route("/subscriptions", methods=["GET"])
def list_subscriptions():
    subs = _router.list_subscriptions()
    return jsonify({
        "success": True,
        "data": [s.to_dict() for s in subs],
        "count": len(subs),
    })


@router_bp.route("/route", methods=["POST"])
def route():
    body = request.get_json(silent=True) or {}
    connector_name = body.get("connector_name")
    params = body.get("params") or {}

    if not connector_name:
        return jsonify({"success": False, "error": "connector_name is required"}), 400

    try:
        connector = registry.get(connector_name)
    except KeyError:
        return jsonify({"success": False, "error": f"Unknown connector: {connector_name}"}), 404

    try:
        documents = connector.run(params)
    except Exception as exc:  # noqa: BLE001 — surface upstream connector errors
        return jsonify({"success": False, "error": str(exc)}), 502

    routed = _router.route_documents(documents)
    return jsonify({
        "success": True,
        "data": {
            "connector": connector_name,
            "fetched": len(documents),
            "routed": len(routed),
            "routings": [r.to_dict() for r in routed],
        },
    })


@router_bp.route("/routings", methods=["GET"])
def routings():
    try:
        limit = int(request.args.get("limit", 100))
    except ValueError:
        return jsonify({"success": False, "error": "limit must be an integer"}), 400
    entries = _router.recent_routings(limit=limit)
    return jsonify({
        "success": True,
        "data": [e.to_dict() for e in entries],
        "count": len(entries),
    })


@router_bp.route("/stats", methods=["GET"])
def stats():
    return jsonify({"success": True, "data": _router.stats()})
