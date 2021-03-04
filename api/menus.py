from flask import jsonify, request, url_for
from . import api
from models import MenuItem, Restaurant
from db import DBSession


@api.route("/api/v1/restaurants/<int:restaurant_id>/menus")
def get_menus(restaurant_id: int):
    session = DBSession()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify([item.to_dict() for item in items])


@api.route("/api/v1/restaurants/<int:restaurant_id>/menus", methods=["POST"])
def post_menus(restaurant_id: int):
    session = DBSession()
    new_item = MenuItem(
        name=request.json["name"],
        description=request.json["description"],
        price=request.json["price"],
        course=request.json["course"],
        restaurant_id=restaurant_id,
    )
    session.add(new_item)
    session.commit()
    return (
        jsonify(
            {
                "name": new_item.name,
                "description": new_item.description,
                "id": new_item.id,
                "price": new_item.price,
                "course": new_item.course,
            },
        ),
        201,
        {
            "Location": url_for("api.get_menus", restaurant_id=restaurant_id)
            + f"/{new_item.id}",
        },
    )


@api.route("/api/v1/restaurants/<int:restaurant_id>/menus/<int:menu_id>")
def get_menu(restaurant_id: int, menu_id: int):
    session = DBSession()
    item = session.query(MenuItem).filter_by(id=menu_id).one_or_none()
    return jsonify(MenuItem=[item.to_dict()])


@api.route(
    "/api/v1/restaurants/<int:restaurant_id>/menus/<int:menu_id>",
    methods=["PATCH", "PUT"],
)
def put_patch_menu(restaurant_id: int, menu_id: int):
    session = DBSession()
    item = session.query(MenuItem).filter_by(id=menu_id).one_or_none()
    if request.json.get("name") is not None:
        item.name = request.json["name"]
    if request.json.get("price") is not None:
        item.price = request.json["price"]
    if request.json.get("description") is not None:
        item.description = request.json["description"]
    if request.json.get("course") is not None:
        item.course = request.json["course"]
    session.commit()
    return jsonify(
        {
            "name": item.name,
            "description": item.description,
            "id": item.id,
            "price": item.price,
            "course": item.course,
        },
    )


@api.route(
    "/api/v1/restaurants/<int:restaurant_id>/menus/<int:menu_id>",
    methods=["DELETE"],
)
def delete_menu(restaurant_id: int, menu_id: int):
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
    item = (
        session.query(MenuItem)
        .filter_by(id=menu_id, restaurant_id=restaurant_id)
        .one_or_none()
    )
    if restaurant is None:
        return (
            jsonify({"details": f"Restaurant {restaurant_id} does not exist"}),
            404,
            {},
        )
    if item is None:
        return (
            jsonify(
                {
                    "details": f"Menu item {menu_id} does not exist in restaurant {restaurant.name}",
                },
            ),
            404,
            {},
        )
    session.delete(item)
    session.commit()
    return (
        None,
        204,
        {},
    )
