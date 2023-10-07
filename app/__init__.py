# app.py
from flask import Flask, request
from app.blueprints import web, user

app = Flask(__name__)

app.register_blueprint(web.bp)
app.register_blueprint(user.bp)


# if __name__ == "__main__":
#     app.run()
