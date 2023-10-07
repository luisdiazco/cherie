from flask import Blueprint, render_template, redirect, url_for, request

bp = Blueprint("user", __name__)


@bp.route('/user/', methods=["GET", "POST"])
def user():
    if request.method == "POST":
        # store user in DB and redirect to same page
        return redirect(url_for("user.create"))
    else:
        return render_template("user/index.html", id=id)


@bp.route("/user/create")
def create():
    return render_template("user/create.html")


@bp.route("/user/<int:id>")
def about(id):
    return render_template("user/show.html", id=id)
