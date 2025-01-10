# -*- coding: utf-8 -*-
import os
import json
import pandas as pd
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font
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

def get_char_width(ch): # 中文、全型字元寬度為兩倍
    if '\u1100' <= ch <= '\uFFDC' or '\u4e00' <= ch <= '\u9fff':
        return 2
    return 1

def generate(info):
    # init workbook
    wb = Workbook()
    ws = wb.active
    ws.title = '修課狀態表'

    # 16 columns
    max_cell_width = [0 for _ in range(16)]

    # set head contents
    head = []
    ## append-something
    
    # set body contents
    body = []
    for idx, (credit_type, course) in enumerate(info.sort_historical_courses.items(), start = 1): # list
        row_header = [f'{idx}. {credit_type}', '課程代碼', '學分數', '期程', '修畢學期', \
            '課程性質', '分數', '修課狀態', '天人物我類別', \
                '主修學程一之必修/核心/選修', '主修學程二之必修/核心/選修', '副修學程之必修/核心/選修', \
                    '資工四大類類別', '主修學程一之課程審查備註', '主修學程一之課程審查備註', '副修學程之課程審查備註']
        body.append(row_header)
        for course_name, course_dict in course: # tuple
            course_property = ' / '.join([p for p in course_dict['課程性質'] if p != ''])
            cs_four_type = ' / '.join([t for t in course_dict['資工四大類類別'] if t != ''])
            row_content = [course_name, course_dict['課程代碼'], course_dict['學分數'], course_dict['期程'], course_dict['修畢學期'], \
                course_property, course_dict['分數'], course_dict['修課狀態'], course_dict['天人物我類別'], \
                    course_dict['課程所屬學程性質']['主修學程一'], course_dict['課程所屬學程性質']['主修學程二'], course_dict['課程所屬學程性質']['副修學程'], \
                        cs_four_type, course_dict['審查備註']['主修學程一'], course_dict['審查備註']['主修學程二'], course_dict['審查備註']['副修學程']]
            # write row content
            body.append(row_content)
        # TODO: 新增未修的必修課
    
    # set tail contents
    tail = []
    ## append-something
    
    # write everything to ws
    ## set cell width
    ### TODO: correct max cell width
    for part in [head, body, tail]:
        for row in part:
            for i, cell in enumerate(row):
                cell_length = sum(get_char_width(c) for c in str(cell))
                #print(f'\'{cell}\', length: {cell_length}, max_cell_width[{i}]: {max_cell_width[i]}', end='')
                if cell_length > max_cell_width[i]:
                    max_cell_width[i] = cell_length
                #    print(' 更新')
                #else:
                #    print(' 不')
    ### set column width
    for i in range(16):
        ws.column_dimensions[chr(65 + i)].width = max_cell_width[i] + 10 # offset
    ## write head and set details
    head_start_row_index = 1

    ## write body and set details
    body_row_header_fill = PatternFill(start_color = 'B7DEE8', end_color = 'B7DEE8', fill_type = 'solid')
    body_row_header_font = Font(bold = True)
    body_row_content_fill = PatternFill(start_color = 'FFFF00', end_color = 'FFFF00', fill_type = 'solid')
    body_start_row_index = head_start_row_index + len(head)
    for row_index, row_data in enumerate(body, start = body_start_row_index):
        for column_index, cell_data in enumerate(row_data, start = 1):
            cell = ws.cell(row = row_index, column = column_index, value = cell_data)
        if row_data[7] == '修課狀態':
            for column in range(1, 17):
                ws.cell(row = row_index, column = column).fill = body_row_header_fill
                ws.cell(row = row_index, column = column).font = body_row_header_font
        elif row_data[7] == '正在修習':
            for column in range(1, 17):
                ws.cell(row = row_index, column = column).fill = body_row_content_fill
    ## write tail and set details

    file_path = './Generated/總表.xlsx'
    wb.save(file_path)

    # TODO: calculate credits and still-need credits
    # TODO: call function in info to generate status table
    ## worksheet 0: 歷年修課.json + 選課系統_基本資料.json + 選課系統_總覽.json = 修課狀態表
    ## 7 columns for each row
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
        info.sort_historical_courses()
        #info.print_sorted_historical_courses()
        info.write_sorted_historical_courses()
        # generate
        generate(info)
    else:
        print('error')
        return
#generate_info('110')