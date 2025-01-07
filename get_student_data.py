# -*- coding: utf-8 -*-
import os
import json
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

MYSELF_URL = 'https://myself.cycu.edu.tw'
MYMENTOR_URL = 'https://cmap.cycu.edu.tw:8443/MyMentor'
HEADERS = {'Content-Type': 'application/json',
           'User-Agent': 'CourseSelector/1.0',
           'Accept': '*/*',
           'Connection': 'keep-alive'}

def login(usr_id, usr_pwd):
    try:
        response = requests.post(url = MYSELF_URL + '/auth/myselfLogin',
                                data = json.dumps({'UserNm': usr_id, 'UserPasswd': usr_pwd}),
                                headers = HEADERS)
        response.raise_for_status() # ensure response is 200
    except requests.exceptions.RequestException as e:
        print('> 網頁獲取失敗：')
        print(e)
        return None, None
    if response.text == '伺服器執行錯誤(i)' or response.json()['done_YN'] != "Y":
        print('> 登入失敗！學號或密碼錯誤！')
        return None, None
    print('> 登入成功！')
    return response.json()['loginToken'], response.cookies

def authenticate(cookies, authApi):
    response = requests.post(url = MYSELF_URL + '/baseinfo',
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
    response = requests.post(url = MYSELF_URL + tgt_url,
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
        if json_file:
            with open(f'{file_name}.json', 'w', encoding = 'utf-8') as f:
                f.write(json.dumps(json_file, indent = 4, ensure_ascii = False))
        else:
            print(f'> \"{file_name}\"獲取失敗！')

# get from CYCU-Myself
def get_student_data(login_token, cookies):
    dir_name = './CYCU-Myself'
    os.makedirs(dir_name, exist_ok = True)
    get_file(login_token, cookies, '/credit/json/ss_loginUser.jsp', '/myself_api_127/credit/api/api_credit.jsp', 'query', f'{dir_name}/歷年修課')
    get_file(login_token, cookies, '/elective/json/ss_loginUser_student.jsp', '/myself_api_127/elective/mvc/elective_system.jsp', 'st_base_info', f'{dir_name}/選課系統_基本資料')
    #get_file(login_token, cookies, '/elective/json/ss_loginUser_student.jsp', '/myself_api_127/elective/mvc/elective_system.jsp', 'track_get', f'{dir_name}/選課系統_追蹤清單')
    get_file(login_token, cookies, '/elective/json/ss_loginUser_student.jsp', '/myself_api_127/elective/mvc/elective_system.jsp', 'st_info_get', f'{dir_name}/選課系統_總覽')

# get from MyMentor
def get_course_properties(usr_id, usr_pwd):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) 
        page = browser.new_page() 
        page.goto(f'{MYMENTOR_URL}/index.do')
        page.fill('input#userId', usr_id)
        page.fill('input#password', usr_pwd)
        page.evaluate("document.getElementById('stdLogin').submit()") # trigger onclick
        page.wait_for_load_state("networkidle")
        if 'stdLogin.do' in page.url:
            page.goto(f'{MYMENTOR_URL}/courseHistory.do')
            page.wait_for_load_state("networkidle")
            if 'courseHistory.do' in page.url:
                soup = BeautifulSoup(page.content(), 'html.parser')
                with open('./CYCU-Myself/歷年修課與狀態表.html', 'wb') as f:
                    f.write(soup.prettify('utf-8'))
            else:
                print(f'> 無法取得MyMentor歷年修課！')
        else:
            print(f'> 無法跳轉到MyMentor歷年修課！')
        browser.close()