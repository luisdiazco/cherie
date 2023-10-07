# app.py
from flask import Blueprint, render_template, request

home_bp = Blueprint("web", __name__)


@home_bp.route('/')
def home():
    return render_template("pages/home.html")


@home_bp.route('/about')
def about():
    return render_template("pages/about.html")
