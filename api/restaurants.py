from flask import jsonify, request, url_for
from . import api
from models import Restaurant
from db import DBSession


@api.route("/api/v1/restaurants")
def get_restaurants():
    offset = request.args.get("offset", None)
    limit = request.args.get("limit", None)
    session = DBSession()
    restaurants_query = session.query(Restaurant)
    if offset:
        restaurants_query = restaurants_query.offset(offset)
    if limit:
        restaurants_query = restaurants_query.limit(limit)
    restaurants = restaurants_query.order_by(Restaurant.id).all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants])


@api.route("/api/v1/restaurants", methods=["POST"])
def post_restaurants():
    session = DBSession()
    new_restaurant = Restaurant(name=request.json["name"])
    session.add(new_restaurant)
    session.commit()
    return (
        jsonify({"id": new_restaurant.id, "name": new_restaurant.name}),
        201,
        {"Location": url_for("api.get_restaurants") + f"/{new_restaurant.id}"},
    )


@api.route("/api/v1/restaurants/<int:restaurant_id>")
def get_restaurant(restaurant_id: int):
    session = DBSession()
    restaurant = (
        session.query(Restaurant).filter(Restaurant.id == restaurant_id).one_or_none()
    )
    if restaurant:
        return jsonify(restaurant.to_dict())
    else:
        return (
            jsonify({"details": f"Restaurant {restaurant_id} does not exist"}),
            404,
            {},
        )


@api.route("/api/v1/restaurants/<int:restaurant_id>", methods=["PUT"])
def put_restaurant(restaurant_id: int):
    session = DBSession()
    restaurant = (
        session.query(Restaurant).filter(Restaurant.id == restaurant_id).one_or_none()
    )
    if restaurant is None:
        return (
            jsonify({"details": f"Restaurant {restaurant_id} does not exist"}),
            404,
            {},
        )
    restaurant.name = request.json["name"]
    session.commit()
    return jsonify({"id": restaurant.id, "name": restaurant.name})


@api.route("/api/v1/restaurants/<int:restaurant_id>", methods=["DELETE"])
def delete_restaurant(restaurant_id: int):
    session = DBSession()
    restaurant = (
        session.query(Restaurant).filter(Restaurant.id == restaurant_id).one_or_none()
    )
    if restaurant is None:
        return (
            jsonify({"details": f"Restaurant {restaurant_id} does not exist"}),
            404,
            {},
        )
    session.delete(restaurant)
    session.commit()
    return (
        None,
        204,
        {},
    )
