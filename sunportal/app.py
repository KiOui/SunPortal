from flask import Flask, render_template, jsonify
from database import DatabaseHandler

app = Flask(__name__)

app.config.from_object("config")


@app.route("/")
def index():
    """
    Index route.

    :return: render of the index.html template
    """
    return render_template("index.html")


@app.route("/update", methods=["POST"])
def update():
    """
    Update route.

    :return: a 500 error on failure or a JSON response on success
    """
    db = DatabaseHandler(app.config["DATABASE_FILE"], app.config["CO2_MULTIPLIER"])
    json_return = dict()
    json_return["last24h"] = db.get_power_last_24h()
    json_return["dayTotal"] = db.get_current_day()
    json_return["total"] = round(db.get_current_total(), 0)
    json_return["co2"] = round(db.get_current_co2(), 2)
    json_return["update"] = db.get_last_update()
    db.close()
    return jsonify(json_return)


if __name__ == "__main__":
    app.run()
