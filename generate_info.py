# -*- coding: utf-8 -*-
import os
import json
import openpyxl

def load_file(file_path, file_name):
    if os.path.exists(file_path):
        return json.load(open(f'{file_path}/{file_name}', 'r', encoding = 'utf-8'))
    else:
        print(f'> 錯誤：\"./{file_path}/{file_name}\"不存在！')
        return None

def generate_status_table(historical_courses, basic_rules, credit_details):
    pass
    # build df and judge/set status
    
    # create xlsx file

    # write xlsx file

def generate_future_course_table():
    pass

# read json files, and generate excel file of course status
def generate_info(enroll_year):
    historical_courses = load_file('./CYCU-Myself', '歷年修課.json')
    basic_rules = load_file('./Generated', f'{enroll_year}_基本畢業條件.json')
    credit_details = load_file('./Generated', '各學程之必修_核心_選修總表.json')
    if historical_courses and basic_rules and credit_details:
        generate_status_table(historical_courses, basic_rules, credit_details)
        # TODO: generate future courses (預排課表)
        ## load files
        ## generate future table in new worksheet (in the same workbook)

#generate_info('110')