from flask import Blueprint, render_template, redirect, url_for, request

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route('/signin-cherie')
def signin_cherie():
    return render_template("signin_cherie.html")
