from flask import request, jsonify
from datetime import datetime

def init (app, connection):

  @app.route("/api/products", methods = ["GET"])
  def getProducts():
    cursor = connection.connection.cursor()
    sql = "SELECT productoId, productoDescripcion, productoStock, productoUrlImagen, productoPrecio FROM producto"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()

    products = []

    for row in data:
      product = { "productoId": row[0], "descripcion": row[1], "stock": row[2], "urlImg": row[3], "price": row[4] }
      products.append(product)

    response = jsonify({
      "status_code": 200,
      "title_message": "OK",
      "data": {
        "products" : products
      }
    })
    return response

  @app.route("/api/products", methods=["POST"])
  def saveProduct():
    data = request.get_json()
    description = data["description"]
    stock = data["stock"]
    price = data["price"]
    urlImg = data["url"]
    createdAt = datetime.now()

    try:
      cursor = connection.connection.cursor()
      sql = ""

      if urlImg == "":
        sql = sql + "INSERT INTO producto (productoDescripcion, productoStock, productoPrecio, created_at) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (description, stock, price, createdAt))
      else:
        sql = sql + "INSERT INTO producto (productoDescripcion, productoStock, productoUrlImagen, productoPrecio, created_at) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (description, stock, urlImg, price, createdAt))
      
      cursor.connection.commit()
      cursor.close()

      response = jsonify({
        "status_code": 201,
        "title_message": "New Product Created.",
        "message": "The record has been saved successfully."
      })
    
    except Exception as ex:
      print(ex)
      response = jsonify({
        "status_code": 500,
        "title_message": "Product could not be saved.",
        "message": "Oops!, There was a problem saving the record."
      })

    return response
