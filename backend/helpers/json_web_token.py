
from jwt import encode, decode, exceptions
from os import getenv
from datetime import datetime, timedelta
from flask import jsonify

def expireTime(days: int):
  now = datetime.now()
  newDate = now + timedelta(days)
  return newDate

def createToken(data: dict):
  token = encode(payload = {**data, "exp": expireTime(1)}, key = getenv("jwt_secret_key"), algorithm = "HS256")
  token.encode("utf-8")
  return token

def validToken(token):
  try:
    decode(token, key = getenv("jwt_secret_key"), algorithm = ["HS256"])
  except exceptions.DecodeError:
    response = jsonify({
      "status_code": 401, 
      "title_message": "Invalid Token", 
      "message": ""
    })
    return response
  except exceptions.ExpiredSignatureError:
    response = jsonify({
      "status_code": 401, 
      "title_message": "Expired Token", 
      "message": token
    })
    return response