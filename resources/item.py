import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import PlainItemSchema, ItemUpdateSchema, ItemSchema

blue_print = Blueprint("Items", __name__, description="Operations on items")


@blue_print.route("/item/<string:item_id>")
class Item(MethodView):
    @blue_print.response(200, PlainItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("deleting an item is not implemented")

    @blue_print.arguments(ItemUpdateSchema)
    @blue_print.response(200, PlainItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("updating an item is not implemented")


@blue_print.route("/item")
class ItemList(MethodView):
    blue_print.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blue_print.arguments(ItemSchema)
    @blue_print.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="an error occurred while inserting the item")

        return item
