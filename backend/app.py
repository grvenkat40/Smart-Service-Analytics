from flask import Flask
from route import main_routes

app = Flask(__name__)
app.secret_key = 'aS3cr3t!Key#789@dev'

app.register_blueprint(main_routes)



if __name__ == "__main__":
    app.run(debug=True)