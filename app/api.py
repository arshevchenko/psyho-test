# coding: ascii
from app import app
from flask import json, jsonify, request, abort
from mysql import DataBase

@app.route('/api/admin', methods = ['POST'])
def add_test():
    json_data = request.json
    if request.method == 'POST':
        DataBase.add_test(json_data['text'], json_data['uid'], json_data['name'])
        return jsonify([{"result": True}])
    else:
        return abort(404)
    return 'admin'


@app.route('/api/admin/<int:id>', methods = ['DELETE'])
def remove_test(id):
    if request.method != 'DELETE':
        return abort(404)
    else:
        DataBase.remove_test(id)
        return jsonify([{"result": True}])


@app.route('/api/login', methods = ['POST'])
def login():
    return 'login'

@app.route('/api/signin', methods = ['POST'])
def signin():
    return 'sign in'

@app.route('/api/test', methods = ['GET'])
def show_all_tests():
    data = DataBase.user_select_tests()

    result = jsonify(data)
    result.status_code = 200
    return result

@app.route('/api/test/<int:id>', methods = ['GET'])
def show_test(id):
    return 'test %s' % id
