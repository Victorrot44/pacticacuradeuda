from flask_mysqldb import MySQL
from os import getenv

def init(app):
  app.config['MYSQL_HOST'] = getenv("db_host")
  app.config['MYSQL_USER'] = getenv("db_user")
  app.config['MYSQL_PASSWORD'] = getenv("db_password")
  app.config['MYSQL_DB'] = getenv("db_name")

  mysql = MySQL(app)
  return mysql