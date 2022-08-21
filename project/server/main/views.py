# project/server/main/views.py

from celery.result import AsyncResult
from flask import render_template, Blueprint, jsonify, request
import json

from project.server.main.db import DB
from project.server.tasks import create_task

main_blueprint = Blueprint("main", __name__, )


# @main_blueprint.route('/', methods=['GET'])
# def index_page():
#     return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@main_blueprint.route('/', methods=['GET'])
def index_page():
    links = DB().get_links()
    return render_template('main/index.html', links=links)


@main_blueprint.route('/bookmark', methods=['POST'])
def add_bookmark():
    link = request.form['link']
    title = request.form['title']
    tags = request.form['tags']
    return json.dumps(
        {
            'success': True,
            'link': link,
            'title': title,
            'tags': tags
        }), 200, {'ContentType': 'application/json'}


@main_blueprint.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    if f.filename != '':
        f.save(f.filename)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@main_blueprint.route("/tasks", methods=["POST"])
def run_task():
    content = request.json
    task_type = content["type"]
    task = create_task.delay(int(task_type))
    return jsonify({"task_id": task.id}), 202


@main_blueprint.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return jsonify(result), 200
