# coding: ascii
from app import app
from flask import json, jsonify, request, abort
from mysql import DataBase

@app.route('/api/admin', methods = ['GET'])
def admin():
    return 'admin'

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
