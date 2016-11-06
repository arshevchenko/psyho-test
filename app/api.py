from app import app
from flask import json, jsonify, request, abort
from mysql import DataBase

@app.route('/api/admin/test', methods = ['POST', 'GET'])
def add_test():
    json_data = request.json
    if request.method == 'POST':
        DataBase.add_test(json_data['text'], json_data['uid'], json_data['name'])
        return jsonify([{"result": True}])

    else:
        return abort(404)

@app.route('/api/admin/stat', methods = ['GET'])
def get_all_stats():
    if request.method == 'GET':
        data = DataBase.admin_user_results()

        result = jsonify(data)
        result.status_code = 200
        return result
    else:
        return abort(404)


@app.route('/api/admin/test/<int:id>', methods = ['DELETE', 'GET'])
def remove_test(id):
    if request.method == 'DELETE':
        DataBase.remove_test(id)
        return jsonify([{"result": True}])

    elif request.method == 'GET':
        data = DataBase.get_one_test(id)
        result = jsonify(data)
        result.status_code = 200

        return result
    else:
        return abort(404)



@app.route('/api/admin', methods = ['POST'])
def login_as_admin():
    return 'login'

@app.route('/api/login', methods = ['POST'])
def login_as_user():
    json_data = request.json
    if request.method == 'POST':
        get_id = DataBase.add_user(json_data['first_name'], json_data['last_name'])
        return jsonify(get_id)
    else:
        return abort(404)

@app.route('/api/test', methods = ['GET'])
def show_all_tests():
    data = DataBase.user_select_tests()

    result = jsonify(data)
    result.status_code = 200
    return result

@app.route('/api/test/<int:id>', methods = ['GET'])
def show_test(id):
    data = DataBase.get_one_test(id)
    result = jsonify(data)
    result.status_code = 200

    return result

@app.route('/api/stat', methods = ['POST', 'GET'])
def user_stats():
    if request.method == "POST":
        json_data = request.json
        DataBase.add_stat(json_data['uid'],
                          json_data['test_id'],
                          json_data['test_time'],
                          json_data['err_count'])
        return jsonify([{"result" : True}])

    elif request.method == "GET":
        data = DataBase.get_user_results()

        result = jsonify(data)
        result.status_code(200)
        return result

    else:
        return abort(404)
