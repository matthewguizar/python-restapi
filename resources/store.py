import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

import schemas
from db import db
from models import StoreModel
from schemas import StoreSchema


blue_print = Blueprint("stores", __name__, description="Operations on stores")


@blue_print.route("/store/<int:store_id>")
class Store(MethodView):
    @blue_print.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "store deleted"}


@blue_print.route("/store")
class StoreList(MethodView):
    @blue_print.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blue_print.arguments(StoreSchema)
    @blue_print.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="a store with that name already exists"
            )
        except SQLAlchemyError:
            abort(500, message="an error occurred creating the store")

        return store

