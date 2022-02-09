import os
from flask import Flask
from controllers.home_controller import home_controller
from controllers.stocks_controller import stocks_controller

app = Flask(__name__)

app.register_blueprint(home_controller)
app.register_blueprint(stocks_controller)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
