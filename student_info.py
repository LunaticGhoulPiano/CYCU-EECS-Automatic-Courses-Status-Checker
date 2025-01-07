# -*- coding: utf-8 -*-
import os
import re
import json
from html.parser import HTMLParser

def format_string(string):
    return string

class StudentInfo:
    # init
    def __init__(self, enroll_year, historical_courses, basic_user_info, total_overview, basic_rules, credit_details):
        self.enroll_year = enroll_year
        self.historical_courses = historical_courses
        self.basic_user_info = basic_user_info
        self.total_overview = total_overview
        self.basic_rules = basic_rules
        self.credit_details = credit_details
    
    def check_init(self):
        if not self.enroll_year or not self.historical_courses or not self.basic_user_info or \
            not self.total_overview or not self.basic_rules or not self.credit_details:
            return False
        return True
    
    # TODO: ---------- parse & set file from ./CYCU-Myself ----------
    
    ## 選課系統_基本資料.json (i.e. self.basic_user_info)
    ### 'st_info' (基本資料)
    def set_basic_infos(self):
        pass

    ## 歷年修課.json (i.e. self.historical_courses)
    ### 'YEAR_TEAM' (現在學期)
    def set_current_semester(self):
        pass
    
    ### 'STD_COURSE_LIST' (所有課程資料)
    def set_historical_courses(self):
        pass

    ### 'STD_FULL_ENGLISH' (系統認列之全課程英文課程), 'STD_ENGLISH_PASS' (系統認列之英文是否通過門檻)
    def set_system_english_status(self):
        pass

    ## 選課系統_總覽.json (i.e. self.total_overview)
    ### 'register_get' (登記清單)
    def set_register_list(self):
        pass

    ### 'track_get' (追蹤清單)
    def set_track_list(self):
        pass

    ### 'take_course_get' (現階段已選上的下學期課程)
    def set_already_selected_courses(self):
        pass

    ### 'sys_open' (選課系統是否開放), 'announcement_td' (現在選課階段)
    def course_selection_system_open(self):
        pass

    # TODO: ---------- parse & set file from ./Generated ----------

    # TODO: ---------- set getter & setter of all data ----------