from uuid import uuid4
from http import HTTPStatus

from flask import Blueprint, jsonify, request

from app.classes.storage import Storage
from app.classes.mine_field import MineField
from handlers.response_messages import MessageType
from handlers.validators import NEW_MINE_FIELD, EXISTING_MINE_FIELD, MINE_FIELD_ID

bp = Blueprint("mine_field", __name__)


@bp.route("/", methods=["POST"])
def create_mine_field():
    json_data = request.get_json()
    NEW_MINE_FIELD.check(json_data)
    new_mine_field_id = uuid4()

    try:
        mine_field = MineField(
            horizontal_size=json_data["horizontalFieldSize"],
            vertical_size=json_data["verticalFieldSize"],
            mines=json_data["mines"],
            discoverable_radius=json_data["discoverableRadius"],
            opened_cells=json_data["openedCells"]
        )
    except ValueError as error:
        return jsonify({
            "message": MessageType.IncorrectInput.value,
            "error": str(error)
        }), HTTPStatus.UNPROCESSABLE_ENTITY

    Storage().set(new_mine_field_id, mine_field)
    return jsonify({
        "message": MessageType.FieldCreated.value,
        "mineFieldId": new_mine_field_id,
        "gameState": mine_field.get_game_state(),
        "mineField": mine_field.to_dict()
    }), HTTPStatus.CREATED


@bp.route("/<mine_field_id>", methods=["PUT"])
def update_mine_field(mine_field_id: str):
    MINE_FIELD_ID.check(mine_field_id)
    json_data = request.get_json()
    EXISTING_MINE_FIELD.check(json_data)
    storage = Storage()
    mine_field = storage.get(mine_field_id)

    if not mine_field:
        return jsonify({
            "message": MessageType.IncorrectInput.value,
            "error": f"no mine field with `{mine_field_id}` was found"
        }), HTTPStatus.CONFLICT

    try:
        mine_field.discover_cell(json_data["x"], json_data["y"])
    except ValueError as error:
        return jsonify({
            "message": MessageType.IncorrectInput.value,
            "error": str(error)
        }), HTTPStatus.UNPROCESSABLE_ENTITY

    storage.set(mine_field_id, mine_field)
    return jsonify({
        "message": MessageType.CellDiscovered.value,
        "mineFieldId": mine_field_id,
        "gameState": mine_field.get_game_state(),
        "mineField": mine_field.to_dict()
    })
