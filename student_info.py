# -*- coding: utf-8 -*-
import os
import re
import json
from bs4 import BeautifulSoup

class StudentInfo:
    # init
    def __init__(self, enroll_year, basic_rules, credit_details):
        # get inputs
        self.basic_rules = basic_rules
        self.credit_details = credit_details
        # infos
        self.name = '' # 學生姓名
        self.class_id = '' # 班級代碼
        self.class_name = '' # 班級名稱
        self.id = '' # 學號
        self.enroll_year = enroll_year # 入學年度(學號前三碼)
        self.cur_semester = '' # 目前學期
        self.survey_finish_rate = '' # 教學評量問卷填答率
        self.cross_bits = [] # 跨/就/微學程
        self.sys_eng_course_pass = False # 學校系統內部判斷是否通過英文學程
        self.sys_eng_courses = [] # 學校系統內部認列的全英文課程
        self.select_system_open = False # 選課系統是否開放
        self.select_status = '' # 現在選課階段
        self.course_list = [] # 歷年修課清單
        self.course_properties_mapping = {} # 歷年課程對應的屬性
        self.chosed_courses = [] # 已選上的課程清單
        self.register_list = [] # 登記清單
        self.track_list = [] # 追蹤清單
    
    # read files
    def read(self, historical_courses, basic_user_info, total_overview, course_properties):
        historical_courses = historical_courses
        basic_user_info = basic_user_info
        total_overview = total_overview
        course_properties = BeautifulSoup(course_properties, 'html.parser')
        # 選課系統_基本資料.json (i.e. self.basic_user_info)
        basic_info = basic_user_info['st_info'][0]
        self.name = basic_info['STMD_NAME'].strip()
        self.class_id = basic_info['STMD_CUR_DPT'].strip()
        self.class_name = basic_info['STMD_DPT_NAME'].strip()
        self.id = basic_info['IDCODE'].strip()
        self.survey_finish_rate = basic_info['SURVEY_FINISH_RATE'].strip() + '%'
        self.cross_bits = [name.strip() for temp_dict in basic_info['CROSS_BITS_LIST'] for _, name in temp_dict.items()] # 跨/就/微學程

        # 歷年修課.json (i.e. self.historical_courses)
        self.cur_semester = historical_courses['YEAR_TERM'].strip()
        self.course_list = historical_courses['STD_COURSE_LIST'] # TODO: parse
        self.sys_eng_course_pass = historical_courses['STD_ENGLISH_PASS']
        self.sys_eng_courses = historical_courses['STD_FULL_ENGLISH'] # TODO: parse

        # 選課系統_總覽.json (i.e. self.total_overview)
        self.select_system_open = total_overview['sys_open']
        self.select_status = total_overview['announcement_td']
        self.chosed_courses = total_overview['take_course_get'] # TODO: parse
        self.register_list = total_overview['register_get'] # TODO: parse
        self.track_list = total_overview['track_get'] # TODO: parse

        # 歷年修課與狀態表.html (i.e. self.course_properties)
        ## add passed courses
        course_set = set()
        contents = course_properties.find('div', id = 'wrapper').find('div', id = 'content').find('div', id = 'right_content')
        for body in contents.find_all('tbody'):
            for course in body.find_all('tr', class_ = False):
                data = {'0': '', '1': '', '2': '', '3': '', '4': '', '5': ''}
                for idx, td in enumerate(course.find_all('td')): # 0: 學年, 1: 課程名稱, 2: 必選修, 3: 學分數, 4: 幾學期, 5: 最終成績/抵免
                    text = td.text.strip()
                    data[str(idx)] = text
                if data['5'] != '抵免' and data['5'] != '' and int(data['5']) < 60: # 不及格, 若為''表示正在修習
                    continue
                course_set.add(data['1'])
        ## extract properties
        for course in course_set:
            course_properties = []
            course_name = ''
            index = 0
            length = len(course)
            while index < length:
                course_property = ''
                if course[index] == '(':
                    index += 1
                    while course[index] != ')':
                        course_property += course[index]
                        index += 1
                    course_properties.append(course_property)
                    index += 1
                else:
                    course_name = course[index:].strip()
                    break
            self.course_properties_mapping[course_name] = course_properties

    # TODO: ---------- parse ----------
    ## self.course_list
    ## self.sys_eng_courses
    ## self.chosed_courses
    ## self.register_list
    ## self.track_list
    def parse(self):
        pass