"""
Flask blueprint exposing the data connector framework via REST.

Routes (all under /api/connectors):
    GET   /                       list all connectors (optional ?vertical=)
    GET   /<name>                 connector info
    GET   /<name>/health          health check (auth presence)
    POST  /<name>/fetch           fetch + transform → return Document JSON
    GET   /health                 aggregate health for every connector
"""
from __future__ import annotations

from flask import Blueprint, jsonify, request

from ..connectors import registry

connectors_bp = Blueprint("connectors", __name__, url_prefix="/api/connectors")


@connectors_bp.route("", methods=["GET"])
@connectors_bp.route("/", methods=["GET"])
def list_connectors():
    vertical = request.args.get("vertical")
    items = registry.list(vertical=vertical)
    return jsonify({
        "success": True,
        "data": [i.to_dict() for i in items],
        "count": len(items),
    })


@connectors_bp.route("/health", methods=["GET"])
def health_all():
    return jsonify({
        "success": True,
        "data": registry.health_check_all(),
    })


@connectors_bp.route("/<name>", methods=["GET"])
def get_info(name: str):
    try:
        connector = registry.get(name)
    except KeyError:
        return jsonify({"success": False, "error": f"Unknown connector: {name}"}), 404
    return jsonify({"success": True, "data": connector.info().to_dict()})


@connectors_bp.route("/<name>/health", methods=["GET"])
def get_health(name: str):
    try:
        connector = registry.get(name)
    except KeyError:
        return jsonify({"success": False, "error": f"Unknown connector: {name}"}), 404
    return jsonify({"success": True, "data": connector.health_check()})


@connectors_bp.route("/<name>/fetch", methods=["POST"])
def fetch(name: str):
    try:
        connector = registry.get(name)
    except KeyError:
        return jsonify({"success": False, "error": f"Unknown connector: {name}"}), 404

    params = request.get_json(silent=True) or {}
    try:
        documents = connector.run(params)
    except Exception as exc:  # noqa: BLE001
        return jsonify({"success": False, "error": str(exc)}), 502

    return jsonify({
        "success": True,
        "data": {
            "connector": name,
            "count": len(documents),
            "documents": [d.to_dict() for d in documents],
        },
    })
