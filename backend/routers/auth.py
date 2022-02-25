from flask import request, jsonify
from helpers.json_web_token import createToken
from helpers.encrypt_helper import valid_password

def init(app, connection):

  @app.route("/api/auth/login", methods=["POST"])
  def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    cursor = connection.connection.cursor()
    sql = "SELECT * FROM usuario WHERE usuarioCorreo = (%s)"
    cursor.execute(sql, (email,))
    user = cursor.fetchall()

    if not user:
      response = jsonify({
        "status_code": 400,
        "title_message": "Bad Request",
        "message": "The user is not registered."
      })
    else:
      if valid_password(user[0][4], password):
        data = {
          "id": user[0][0],
          "firstname": user[0][1],
          "lastname": user[0][2],
          "email": user[0][3],
          "type": user[0][5]
        }
        token = createToken(data)
        response = jsonify({
          "status_code": 200,
          "title_message": "Access Granted",
          "token": token,
          "user": data
        })
      else:
        response = jsonify({
          "status_code": 400,
          "title_message": "Bad Request",
          "message": "Password is incorrect."
        })
    
    cursor.close()
    return response

  @app.route("/api/auth/exit", methods = ["GET"])
  def exit():
    # Token Destroy
    return 0