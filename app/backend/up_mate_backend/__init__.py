import pathlib
import typing

import flask
import pymongo

import up_mate_backend._db

_MODULE_DIR = pathlib.Path(__name__).parent

app = flask.Flask(
    template_folder=(_MODULE_DIR / "templates"),
    import_name=__name__
)

class Message(typing.NamedTuple):
    # TODO: make this configurable
    user: str
    pain_level: float
    notes: str

_keys_in_update = ["pain_level", "notes", "user"]

@app.route("/")
def index():
    return flask.render_template("index.html")

def _get_user_info(user: str) -> dict:
    try:
        return up_mate_backend._db.get_latest_status(user=user)
    except up_mate_backend._db.NotFoundError:
        raise flask.abort(404, "Not Found")

@app.route("/api/get", methods=["GET", "POST"])
def get_current():
    user = flask.request.form.get("user")
    return flask.jsonify(_get_user_info(user))
    

@app.route("/api/update", methods=["POST"])
def update():
    data = {}
    for field in _keys_in_update:
        value = data[field] = flask.request.form.get(field)
        if value is None:
            raise flask.abort(403, "Missing key " + field)

    up_mate_backend._db.add_status(
        Message(**data)._asdict()
    )
    # TODO: publish notifications
    return flask.Response("ACK")
