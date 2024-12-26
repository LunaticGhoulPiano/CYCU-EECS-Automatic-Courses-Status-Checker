# -*- coding: utf-8 -*-
from get_data import get_data
from get_basic_course_table import get_basic_course_table

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

def main():
    print('> 中原大學電機資訊學院學士班 學程與修課狀態確認系統')
    print('> 正在取得CYCU-Myself檔案...')
    usr = Student(get_data())
    usr.parse_id()
    print('> 正在取得應修科目表...')
    get_basic_course_table(usr.enroll_year)

if __name__ == "__main__":
    main()