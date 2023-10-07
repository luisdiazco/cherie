from flask import Blueprint, render_template, request

bp = Blueprint("user", __name__)


@bp.route('/user/', methods=["GET", "POST"])
def user():
    if request.method == "POST":
        return "create new user"
    else:
        return render_template("user/index.html", id=id)


@bp.route("/user/<int:id>")
def about(id):
    return render_template("user/show.html", id=id)
