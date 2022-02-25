from flask import request, jsonify

def init (app, connection):

  @app.route("/api/domiciles", methods = ["GET"])
  def getDomiciles():
    try:
      userId = request.args.get("userId")
      cursor = connection.connection.cursor()
      sql = "SELECT domicilioId , domicilioDireccion FROM domicilio WHERE domicilioUsuarioId = (%s)"
      cursor.execute(sql, (userId,))
      data = cursor.fetchall()
      cursor.close()

      domeciles = []

      for row in data:
        domecile = { "domicilioId": row[0], "domicilio": row[1] }
        domeciles.append(domecile)

      response = jsonify({
        "status_code": 200,
        "title_message": "OK.",
        "data": {
          "domeciles": domeciles
        }
      })
    except Exception as ex:
      response = jsonify({
        "status_code": 500,
        "title_message": "Error.",
        "message": "Error Internal"
      })

    return response

  @app.route("/api/domicile", methods = ["POST"])
  def saveDomicile():
    data = request.get_json()
    idUser = data["userId"]
    street = data["street"]
    noExt = data["noExt"]
    noInt = data["noInt"]
    cp = data["cp"]
    colonia = data["colonia"]
    municipio = data["municipio"]
    state = data["state"]

    domicile = ""
    if noInt == '':
      domicile = domicile + street + " #" + str(noExt) + ", " + colonia + ", C.P. " + str(cp) + ", " + municipio + ", " +state
    else:
      domicile = domicile + street + " #" + str(noExt) + ", No. Int. " + str(noInt) + ", " + colonia + ", C.P. " + str(cp) + ", " + municipio + ", " +state

    try:
      cursor = connection.connection.cursor()
      sql = "INSERT INTO domicilio (domicilioUsuarioId, domicilioDireccion) VALUES (%s, %s)"
      cursor.execute(sql, (idUser, domicile))
      cursor.connection.commit()
      cursor.close()

      response = jsonify({
        "status_code": 201,
        "title_message": "New Domicile Added.",
        "message": "Excellent, saved address for future deliveries."
      })
    except Exception as ex:
      response = jsonify({
        "status_code": 500,
        "title_message": "Error.",
        "message": "There was a problem saving the information, please try again later."
      })

    return response

  @app.route("/api/search/cp/<cp>", methods = ["GET"])
  def searchByCp(cp):
    cursor = connection.connection.cursor()
    sql = "SELECT coloniaNombre, coloniaMunicipioId, coloniaEstadoId FROM colonia WHERE coloniaCp = (%s)"
    cursor.execute(sql, (cp,))
    data = cursor.fetchall()
    cursor.close()

    if not data: 
      return jsonify({
        "status_code": 404,
        "title_message": "Not Found",
        "message": "Postal code not found."
      })

    colonias = []

    for row in data:
      colonia = { "colonia": row[0], "municipioId": row[1], "estadoId": row[2] }
      colonias.append(colonia)

    response = jsonify({
      "status_code": 200,
      "data": {
        "colonias" : colonias
      }
    })
    return response

  @app.route("/api/search/municipality/<municipality>", methods = ["GET"])
  def searchMunicipalityState(municipality):
    cursor = connection.connection.cursor()
    sql = "SELECT m.municipioNombre, e.estadoNombre FROM municipio AS m JOIN estado AS e ON m.municipioEstadoId = e.estadoId WHERE m.municipioId = (%s)"
    cursor.execute(sql, (municipality,))
    data = cursor.fetchone()
    
    cursor.close()

    if not data:
      return jsonify({
        "status_code": 404,
        "title_message": "Not Found",
        "message": "The municipality does not exist."
      })

    return jsonify({
      "status_code": 200,
      "title_message": "OK",
      "data": {
        "municipality" :  data[0],
        "state": data[1]
      },
    })


