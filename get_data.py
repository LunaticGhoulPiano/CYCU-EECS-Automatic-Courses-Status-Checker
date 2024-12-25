# -*- coding: utf-8 -*-
import os
import json
import getpass
import requests

URL = 'https://myself.cycu.edu.tw'
HEADERS = {'Content-Type': 'application/json',
           'User-Agent': 'CourseSelector/1.0',
           'Accept': '*/*',
           'Connection': 'keep-alive'}

def login(usr_id, usr_pwd):
    response = requests.post(url = URL + '/auth/myselfLogin',
                             data = json.dumps({'UserNm': usr_id, 'UserPasswd': usr_pwd}),
                             headers = HEADERS)
    
    if response.status_code != 200:
        print('> 網頁獲取失敗！')
        return None, None
    if response.text == '伺服器執行錯誤(i)' or response.json()['done_YN'] != "Y":
        print('> 登入失敗！學號或密碼錯誤！')
        return None, None
    print('> 登入成功！')
    return response.json()['loginToken'], response.cookies

def authenticate(cookies, authApi):
    response = requests.post(url = URL + '/baseinfo',
                            data = json.dumps({'authUrl': '/myself_api_127',
                                               'authApi': authApi}),
                            headers = HEADERS,
                            cookies = cookies,
                            params = None)
    msg = response.json()
    if 'APP_AUTH_token' not in msg:
        return None, None
    return msg["APP_AUTH_token"], cookies

def get_json(login_token, auth_token, cookies, tgt_url, method):
    response = requests.post(url = URL + tgt_url,
                            data = json.dumps({'APP_AUTH_token': auth_token}),
                            headers = HEADERS,
                            cookies = cookies,
                            params = {'loginToken': login_token,
                                      'method': method})
    return response.json()

def get_file(login_token, cookies, authApi, tgt_url, method, file_name):
    auth_token, cookies = authenticate(cookies, authApi)
    if auth_token:
        json_file = get_json(login_token, auth_token, cookies, tgt_url, method)
        with open(f'{file_name}.json', 'w', encoding = 'utf-8') as f:
            f.write(json.dumps(json_file, indent = 4, ensure_ascii = False))

def get_data():
    # init
    usr_id = input('學號：')
    usr_pwd = getpass.getpass('密碼：')
    
    # login
    login_token, cookies = login(usr_id, usr_pwd)
    if not login_token:
        if input('是否重新登入?(Y/N)') == 'Y':
            return get_data()
        else:
            return
        return get_data()

    # get files
    dir_name = './CYCU-Myself'
    os.makedirs(dir_name, exist_ok = True)
    get_file(login_token, cookies, '/credit/json/ss_loginUser.jsp', '/myself_api_127/credit/api/api_credit.jsp', 'query', f'{dir_name}/歷年修課')
    get_file(login_token, cookies, '/elective/json/ss_loginUser_student.jsp', '/myself_api_127/elective/mvc/elective_system.jsp', 'st_base_info', f'{dir_name}/選課系統-基本資料')
    get_file(login_token, cookies, '/elective/json/ss_loginUser_student.jsp', '/myself_api_127/elective/mvc/elective_system.jsp', 'track_get', f'{dir_name}/選課系統-追蹤清單')
    get_file(login_token, cookies, '/elective/json/ss_loginUser_student.jsp', '/myself_api_127/elective/mvc/elective_system.jsp', 'st_info_get', f'{dir_name}/選課系統-總覽')