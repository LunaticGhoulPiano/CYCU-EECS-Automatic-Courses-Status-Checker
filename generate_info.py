# -*- coding: utf-8 -*-
import os
import json
import pandas as pd
import openpyxl
from student_info import StudentInfo

def load_file(file_path, file_name):
    if os.path.exists(f'{file_path}/{file_name}'):
        if file_name.endswith('.json'):
            return json.load(open(f'{file_path}/{file_name}', 'r', encoding = 'utf-8'))
        elif file_name.endswith('.html'):
            return open(f'{file_path}/{file_name}', 'r', encoding = 'utf-8').read()
    else:
        print(f'> 錯誤：\"{file_path}/{file_name}\"不存在！')
        return None

def generate(info):
    # TODO: call function in info to generate status table
    ## worksheet 0: 歷年修課.json + 選課系統_基本資料.json + 選課系統_總覽.json = 修課狀態表
    ## 7 columns for each row
    status_table = pd.DataFrame(columns = ['Column1', 'Column2', 'Column3', 'Column4', 'Column5', 'Column6', 'Column7'])
    major1 = info.basic_rules['學系選修']['主修學程一']
    major2 = info.basic_rules['學系選修']['主修學程二']
    sub_major = info.basic_rules['學系選修']['副修學程']
    overview_header = [f'主修一：{major1}，主修二：{major2}, 副修：{sub_major}',
                       '畢業門檻學分數',
                       '已修學分數',
                       '整學年（上+下）缺項',
                       '缺項備註',
                       '當學期正在修習',
                       '下學期預計修習']
    overview_content = []
    
    
    # TODO: call function in info to generate future course table (if needed)
    ## worksheet 1: 歷年修課.json + 選課系統_基本資料.json + 選課系統_總覽.json = 預排課表

    # if already has excel file, then append in new worksheets

# read json files, and generate excel file of course status
def generate_info(enroll_year):
    basic_user_info = load_file('./CYCU-Myself', '選課系統_基本資料.json')
    historical_courses = load_file('./CYCU-Myself', '歷年修課.json')
    total_overview = load_file('./CYCU-Myself', '選課系統_總覽.json')
    course_properties = load_file('./CYCU-Myself', '歷年修課與狀態表.html')
    basic_rules = load_file('./Generated', f'{enroll_year}_基本畢業條件.json')
    credit_details = load_file('./Generated', '各學程之必修_核心_選修總表.json')
    if all([basic_user_info, historical_courses, total_overview, course_properties, basic_rules, credit_details]):
        # initialize
        info = StudentInfo(enroll_year, basic_rules, credit_details)
        info.read(basic_user_info, historical_courses, total_overview, course_properties)
        info.parse()
        # generate
        #generate(info)
        info.PrintCourses()
        """i = 1
        for course_name, course_dict in info.historical_course_list.items():
            print(course_name, course_dict['性質'])
            i += 1"""
    else:
        print('error')
        return

#generate_info('110')