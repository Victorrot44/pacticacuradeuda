from flask import request, jsonify
from datetime import datetime

def init (app, connection):

  @app.route("/api/order", methods = ["POST"])
  def createOrder():
    return 0