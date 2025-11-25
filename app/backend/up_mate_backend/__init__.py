import pathlib
import typing

import flask
import pymongo

import up_mate_backend._db

_MODULE_DIR = pathlib.Path(__name__).parent

app = flask.Flask(
    template_folder=(_MODULE_DIR / "_templates"),
    static_folder=(_MODULE_DIR / "_static"),
    static_url_path="/static",
    import_name=__name__
)


# TODO: consider pydantic -> creates tooling for max/min controls...
class Message(typing.NamedTuple):
    # TODO: make this configurable
    user: str
    pain_level: float
    notes: str

people = {"John", "Jane"} # TODO: make this configurable

@app.route("/<string:name>")
def main(name: str):
    return flask.render_template("app.html", me=name, mate=[o for o in (people - {name})][0])

@app.route("/")
def index():
    return flask.render_template("index.html", people=sorted(people))

def _get_user_info(user: str) -> dict:
    try:
        return up_mate_backend._db.get_latest_status(user=user)
    except up_mate_backend._db.NotFoundError:
        raise flask.abort(404, "Not Found")

@app.route("/api/get", methods=["GET", "POST"])
def get_current():
    user = flask.request.form.get("user")
    return flask.jsonify(_get_user_info(user))

NO_DEFAULT = object()

@app.route("/api/update", methods=["POST"])
def update():
    data = {}
    for field in Message._fields:
        value = data[field] = flask.request.form.get(field)
        if value is None and Message._field_defaults.get(field, NO_DEFAULT) == NO_DEFAULT:
            raise flask.abort(400, f'Missing value for "{field}"')

    up_mate_backend._db.add_status(
        Message(**data)._asdict()
    )
    # TODO: publish notifications
    return flask.Response("ACK")
