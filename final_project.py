import os

from flask import Flask, render_template, request, redirect, url_for, flash

from db import DBSession
from models import Restaurant, MenuItem
from api import api

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(api)


@app.before_request
def clear_trailing():
    rp = request.path
    if rp != "/" and rp.endswith("/"):
        return redirect(rp[:-1])


@app.route("/")
@app.route("/restaurants")
def show_restaurants():
    session = DBSession()
    restaurants = session.query(Restaurant).all()
    return render_template("0_restaurants.html", restaurants=restaurants)


@app.route("/restaurants/new", methods=["GET", "POST"])
def create_new_restaurant():
    session = DBSession()

    if request.method == "POST":
        new_restaurant = Restaurant(name=request.form["name"])
        session.add(new_restaurant)
        session.commit()
        return redirect(url_for("show_restaurants"))
    else:
        return render_template("1_new_restaurants.html")


@app.route("/restaurants/<int:restaurant_id>/edit", methods=["GET", "POST"])
def edit_restaurant(restaurant_id: int):
    session = DBSession()
    restaurant_to_edit = (
        session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
    )

    if request.method == "POST":
        if request.form["name"]:
            restaurant_to_edit.name = request.form["name"]
        session.add(restaurant_to_edit)
        session.commit()
        flash(f"Edited restaurant to {restaurant_to_edit.name}")
        return redirect(url_for("show_restaurants"))
    else:
        return render_template(
            "2_edit_restaurants.html",
            restaurant_id=restaurant_id,
            restaurant=restaurant_to_edit,
        )


@app.route("/restaurants/<int:restaurant_id>/delete", methods=["GET", "POST"])
def delete_restaurant(restaurant_id: int):
    session = DBSession()

    restaurant_to_delete = (
        session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
    )

    if request.method == "POST":
        session.delete(restaurant_to_delete)
        session.commit()
        flash(f"Deleted restaurant {restaurant_to_delete.name}")
        return redirect(url_for("show_restaurants"))
    else:
        return render_template(
            "3_delete_restaurants.html",
            restaurant_id=restaurant_id,
            restaurant=restaurant_to_delete,
        )


@app.route("/restaurants/<int:restaurant_id>")
@app.route("/restaurants/<int:restaurant_id>/menus")
def show_menu(restaurant_id: int):
    session = DBSession()

    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()

    return render_template(
        "4_menu.html",
        restaurant=restaurant,
        items=items,
    )


@app.route("/restaurants/<int:restaurant_id>/menus/new", methods=["GET", "POST"])
def create_new_menu_item(restaurant_id: int):
    session = DBSession()

    if request.method == "POST":
        new_item = MenuItem(name=request.form["name"], restaurant_id=restaurant_id)
        session.add(new_item)
        session.commit()
        flash("New menu item created!")
        return redirect(url_for("show_menu", restaurant_id=restaurant_id))
    else:
        return render_template("5_new_menu_item.html", restaurant_id=restaurant_id)


@app.route(
    "/restaurants/<int:restaurant_id>/menus/<int:menu_id>/edit",
    methods=["GET", "POST"],
)
def edit_menu_item(restaurant_id: int, menu_id: int):
    session = DBSession()

    item_to_edit = session.query(MenuItem).filter_by(id=menu_id).one_or_none()

    if request.method == "POST":
        if request.form["name"]:
            item_to_edit.name = request.form["name"]

        session.add(item_to_edit)
        session.commit()
        flash(f"Edited menu item to {item_to_edit.name}")
        return redirect(url_for("show_menu", restaurant_id=restaurant_id))
    else:
        return render_template(
            "6_edit_menu_item.html",
            restaurant_id=restaurant_id,
            item=item_to_edit,
        )


@app.route(
    "/restaurants/<int:restaurant_id>/menus/<int:menu_id>/delete",
    methods=["GET", "POST"],
)
def delete_menu_item(restaurant_id: int, menu_id: int):
    session = DBSession()

    item_to_delete = session.query(MenuItem).filter_by(id=menu_id).one_or_none()

    if request.method == "POST":
        session.delete(item_to_delete)
        session.commit()
        flash(f"Deleted menu item {item_to_delete.name}")
        return redirect(url_for("show_menu", restaurant_id=restaurant_id))
    else:
        return render_template(
            "7_delete_menu_item.html",
            item=item_to_delete,
        )


if __name__ == "__main__":
    app.secret_key = os.environ["SECRET_KEY"]
    app.run(host="0.0.0.0")
