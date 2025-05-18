from flask import Flask

from .controller.bank_controller import bank_controller
from .db import db
from .db_config import DbConfig

app = Flask(__name__)
app.config.from_object(DbConfig)
app.register_blueprint(bank_controller, url_prefix='/api/banks')
db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
