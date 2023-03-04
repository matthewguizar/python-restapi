import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from schemas import PlainItemSchema, ItemUpdateSchema

blue_print = Blueprint("Items", __name__, description="Operations on items")


@blue_print.route("/item/<string:item_id>")
class Item(MethodView):
    @blue_print.response(200, PlainItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            return abort(404, message="item not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="item not found")

    @blue_print.arguments(ItemUpdateSchema)
    @blue_print.response(200, PlainItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data  # merges two dictionaries

            return item
        except KeyError:
            abort(404, message="item not found")


@blue_print.route("/item")
class ItemList(MethodView):
    blue_print.response(200, PlainItemSchema(many=True))
    def get(self):
        return items.values()

    @blue_print.arguments(PlainItemSchema)
    @blue_print.response(201, PlainItemSchema)
    def post(self, item_data):
        for item in items.values():
            if (
                    item_data["name"] == item["name"]
                    and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message=f"item already exists")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item
