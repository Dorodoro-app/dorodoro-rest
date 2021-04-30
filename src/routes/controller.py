from flask import Blueprint, Response, request
from cerberus import Validator
from ..db import db
import datetime

api_router = Blueprint("api", __name__, url_prefix="/api")


@api_router.route("/start", methods=["POST"])
def start():
    out = request.json
    schema = {
        "user_id": {"type": "integer", "required": True},
        "length": {"type": "integer", "required": True},
        "type": {"type": "string", "required": True},
        "task_id": {"type": "integer", "required": False},
        "start_time": {"type": "integer", "required": False},
    }
    validator = Validator(schema)
    if not validator.validate(out):
        return {"MSG": "INVALID REQUEST"}
    timestamp = datetime.datetime.fromtimestamp(out["start_time"])
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    query = f"INSERT INTO pomodoro (user_id, length, type, task_id, start_time, status) VALUES({out['user_id']}, '{out['length']}', '{out['type']}',\
        {out['task_id']}, TIMESTAMP '{timestamp}', 'active') RETURNING *;"
    out = next(db.execute(query))
    return {"user_id": out[0], "timer_id": out[1]}


@api_router.route("/pause", methods=["POST"])
def pause():
    out = request.json
    schema = {
        "timer_id": {"type": "integer", "required": True},
        "time_elasped": {"type": "integer", "required": True},
    }
    validator = Validator(schema)
    if not validator.validate(out):
        return {"MSG": "INVALID REQUEST"}
    query = f"UPDATE pomodoro SET time_elasped = {out['time_elasped']} WHERE pomodoro_id = {out['timer_id']} RETURNING *;"
    print(query)
    db.execute(query)
    query = f"UPDATE pomodoro SET status = 'paused' WHERE pomodoro_id = {out['timer_id']} RETURNING *;"
    out = next(db.execute(query))
    return {i: j for i, j in out.items()}


@api_router.route("/stopped", methods=["POST"])
@api_router.route("/completed", methods=["POST"])
def completed():
    out = request.json
    schema = {
        "timer_id": {"type": "integer", "required": True},
        "current_time": {"type": "integer", "required": True},
    }
    validator = Validator(schema)
    if not validator.validate(out):
        return {"MSG": "INVALID REQUEST"}
    timestamp = datetime.datetime.fromtimestamp(out["current_time"])
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    query = f"UPDATE pomodoro SET stop_time = TIMESTAMP '{timestamp}' WHERE pomodoro_id = {out['timer_id']} RETURNING *;"
    print(query)
    db.execute(query)
    query = f"UPDATE pomodoro SET status = 'completed' WHERE pomodoro_id = {out['timer_id']} RETURNING *;"
    out = next(db.execute(query))
    return {i: j for i, j in out.items()}


@api_router.route("/abonded", methods=["POST"])
@api_router.route("/cancel", methods=["POST"])
def cancel():
    out = request.json
    schema = {
        "timer_id": {"type": "integer", "required": True},
        "current_time": {"type": "integer", "required": True},
    }
    validator = Validator(schema)
    if not validator.validate(out):
        return {"MSG": "INVALID REQUEST"}
    timestamp = datetime.datetime.fromtimestamp(out["current_time"])
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    query = f"SELECT * FROM pomodoro WHERE pomodoro_id = {out['timer_id']};"
    tmp = next(db.execute(query))
    tmp = {i: j for i, j in tmp.items()}["status"]
    if tmp in ["completed", "abonded"]:
        return Response('{"MSG" : "THIS POMODORO IS NO LONGER ACTIVE OR PAUSED"}', 400)
    query = f"UPDATE pomodoro SET stop_time = TIMESTAMP '{timestamp}' WHERE pomodoro_id = {out['timer_id']} RETURNING *;"
    db.execute(query)
    query = f"UPDATE pomodoro SET status = 'abonded' WHERE pomodoro_id = {out['timer_id']} RETURNING *;"
    out = next(db.execute(query))
    return {i: j for i, j in out.items()}
