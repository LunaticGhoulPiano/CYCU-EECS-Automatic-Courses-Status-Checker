# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv, set_key
from get_student_data import login, get_student_data
from get_files import get_files

ENV_PATH = '.env'

class Student:
    def __init__(self, usr_id):
        self.id = usr_id
        self.enroll_year = None
        self.dept_number = None
        self.class_num = None
        self.number = None
    
    def parse_id(self):
        self.enroll_year = self.id[0:3]
        self.dept_number = self.id[3:5] # 電資: 20
        self.class_num = self.id[5:6]
        self.number = self.id[6:8]

    def print_info(self):
        print(f'入學年度：{self.enroll_year}')
        print(f'系所編號：{self.dept_number}')
        print(f'班級編號：{self.class_num}')
        print(f'座號：{self.number}')

def init(failed = False):
    usr_id = os.getenv('USR_ID')
    usr_pwd = os.getenv('USR_PWD')
    if not usr_id or not usr_pwd or failed:
        usr_id = input('學號：')
        set_key(ENV_PATH, 'USR_ID', usr_id)
        usr_pwd = input('密碼：')
        set_key(ENV_PATH, 'USR_PWD', usr_pwd)
    
    # login
    login_token, cookies = login(usr_id, usr_pwd)
    if not login_token:
        if input('是否重新登入?(Y/N)') == 'Y':
            return init(failed = True)
        else:
            return None, None, None
    
    # parse id
    usr = Student(usr_id)
    usr.parse_id()
    return usr, login_token, cookies

def main():
    print('> 中原大學電機資訊學院學士班 學程與修課狀態確認系統')
    usr, login_token, cookies = init(failed = False)
    if not usr and not login_token and not cookies:
        print('> 正在結束系統...')
        return
    print('> 正在取得CYCU-Myself檔案...')
    get_student_data(login_token, cookies)
    print('> 正在取得應修科目表...')
    get_files(usr.enroll_year)

if __name__ == "__main__":
    if not load_dotenv():
        if not os.path.exists(ENV_PATH):
            with open(ENV_PATH, 'w', encoding = 'utf-8') as f:
                f.write('USR_ID=\n')
                f.write('USR_PWD=\n')
    main()
    os.system('pause')