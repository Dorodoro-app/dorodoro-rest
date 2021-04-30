from flask import Flask
from src.routes.controller import api_router
from src.routes.stats import stats_router

app = Flask(__name__)
app.register_blueprint(api_router)
app.register_blueprint(stats_router)

if __name__ == "__main__":
    print(app.url_map)
    app.run(host="0.0.0.0", port=5002, debug=True)
