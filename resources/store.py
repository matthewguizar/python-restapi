import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

import schemas
from db import db
from models import StoreModel
from schemas import PlainStoreSchema


blue_print = Blueprint("stores", __name__, description="Operations on stores")


@blue_print.route("/store/<string:store_id>")
class Store(MethodView):
    @blue_print.response(200, PlainStoreSchema)
    def get(self, store_id):
        store = StoreModel.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("deleting a store is not implemented")


@blue_print.route("/store")
class StoreList(MethodView):
    @blue_print.response(200, PlainStoreSchema(many=True))
    def get(self):
        return {"stores": list(stores.values())}

    @blue_print.arguments(PlainStoreSchema)
    @blue_print.response(200, PlainStoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="a store weith that name already exists"
            )
        except SQLAlchemyError:
            abort(500, message="an error occurred creating the store")

        return store

