from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS

import config.DB
import routers.user
import routers.auth
import routers.product
import routers.domicile

app = Flask(__name__)

CORS(app, resources={r"/api/*": { "origins" : "*" }})

mysql = config.DB.init(app)

routers.auth.init(app, mysql)
routers.user.init(app, mysql)
routers.product.init(app, mysql)
routers.domicile.init(app, mysql)

if __name__ == '__main__':
  load_dotenv()
  app.run(host="0.0.0.0", port=4000, debug=True)