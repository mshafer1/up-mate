import logging
import pathlib
import typing

import flask
import markupsafe
import up_mate_backend._config
import up_mate_backend._db
import up_mate_backend._notifications

_MODULE_DIR = pathlib.Path(__name__).parent

app = flask.Flask(
    template_folder=(_MODULE_DIR / "_templates"),
    static_folder=(_MODULE_DIR / "_static"),
    static_url_path="/static",
    import_name=__name__,
)
app.config["MAX_CONTENT_LENGTH"] = 26 * 1024 * 1024  # 26 MB

logging.warning("Starting up...")
logging.warning("Module dir: %s", _MODULE_DIR)
logging.warning("db uri: %s", up_mate_backend._config.DB_CONNECTION_STRING)


# TODO: consider pydantic -> creates tooling for max/min controls...
class Message(typing.NamedTuple):
    # TODO: make this configurable
    user: str
    pain_level: float
    notes: str


PEOPLE = set(up_mate_backend._config.USERS)
logging.info("Known people: %s", PEOPLE)


@app.route("/<string:name>")
def main(name: str):
    if name not in PEOPLE:
        raise flask.abort(404, markupsafe.escape(f"User {name} not found"))
    return flask.render_template("app.html", me=name, mates=sorted([o for o in (PEOPLE - {name})]))


@app.route("/")
def index():
    return flask.render_template("index.html", people=sorted(PEOPLE))


def _get_user_info(user: str) -> dict:
    try:
        info = up_mate_backend._db.get_latest_status(user=user)
    except up_mate_backend._db.NotFoundError:
        raise flask.abort(404, "Not Found")
    info["timestamp"] = info["timestamp"].isoformat()
    return info

@app.route("/api/get", methods=["GET", "POST"])
def get_current():
    user = flask.request.form.get("user")
    return flask.jsonify(_get_user_info(user))


NO_DEFAULT = object()


@app.route("/api/update", methods=["POST"])
def update():
    data = {}
    for field in Message._fields:
        value = data[field] = markupsafe.escape(flask.request.form.get(field))
        if value is None and Message._field_defaults.get(field, NO_DEFAULT) == NO_DEFAULT:
            raise flask.abort(400, f'Missing value for "{field}"')

    up_mate_backend._db.add_status(Message(**data)._asdict())
    up_mate_backend._notifications.send_notification(updated_user=data["user"])
    return flask.Response("ACK")


logging.warning("Setup complete")
