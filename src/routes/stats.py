from flask import Blueprint, Response, request
from cerberus import Validator
from ..db import db
import datetime

stats_router = Blueprint("stats", __name__, url_prefix="/api")


@stats_router.route("/histroy", methods=["GET"])
def start():
    #     # HISTORY

    # GET /api/histroy/?user_id=user_id&?timeline=today

    # RESPONSE
    # {
    #     timeline
    #     total_pomodoro
    #     total_pomodoro_time
    #     length_of_average_pomodoro
    #     each_pomodor_with_values [{pomodor_id, lenght, date}]
    # }
    val = dict(request.args.items())
    if list(val.keys()) != ['user_id', 'timeline']:
        return Response('{"MSG" : "INVALID PARAMETERS"}', 400)
    if val["timeline"] not in ["all"]:
        return Response('{"MSG" : "INVALID PARAMETERS"}', 400)
    query = f"SELECT * FROM pomodoro WHERE user_id = {int(val['user_id'])} and status = 'completed';"
    print(query)
    out = db.execute(query)
    vals = []
    for ii in out:
        vals.append({i: j for i, j in ii.items()})
    response = {
        "timeline" : val["timeline"],
        "total_pomodoro" : None,
        "total_pomodoro_time" : 0,
        "length_of_average_pomodoro" : None,
        "each_pomodor_with_values" : vals
    }
    for dicts in vals:
        response["total_pomodoro_time"] += dicts["length"]
    response["total_pomodoro"] = len(vals)  
    response["length_of_average_pomodoro"] = response["total_pomodoro_time"]/len(vals)  
    return response