from flask import Flask
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app)

# 127.0.0.1/hello
@api.route("/hello")
class hello(Resource):
    def get(self):
        return {"content": "Hello from Flask!"}

if __name__ == "__main__":
    app.run(port = 5005)   

