from flask import request, jsonify
from datetime import datetime
from helpers.encrypt_helper import encrypt_password

def init(app, connection):
  
  @app.route("/api/user", methods=["POST"])
  def saveUser():
    data = request.get_json()
    firstname = data['firstname']
    lastname = data['lastname']
    email = data['email']
    password = encrypt_password(data['password'])
    typeUser = data['type']
    createdAt = datetime.now()

    cursor = connection.connection.cursor()
    sql = "INSERT INTO usuario (usuarioNombre, usuarioApellidos, usuarioCorreo, usuarioPassword, usuarioTipoUsuario, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
    
    try: 
      cursor.execute(sql, (firstname, lastname, email, password, typeUser, createdAt))
      cursor.connection.commit()
      cursor.close()

      response = jsonify({
        "status_code": 201,
        "title_message": "New User Created.",
        "message": "The record has been saved successfully."
      })

    except cursor.IntegrityError as e:
      
      string = str(e)
      array = string.split(',')
      message = array[1]

      response = jsonify({
        "status_code": 400,
        "title_message": "Bad Request",
        "message": message[:-1]
      })

    return response

  @app.route("/api/users", methods=["GET"])
  def getUsers():
    cursor = connection.connection.cursor()
    sql = "SELECT usuarioId, usuarioNombre, usuarioApellidos, usuarioCorreo FROM usuario"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()

    response = jsonify({
      "status_code": 200,
      "title_message": "OK",
      "data": {
        "users" : data
      }
    })
    
    return response