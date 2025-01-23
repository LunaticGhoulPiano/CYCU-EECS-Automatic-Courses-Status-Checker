# -*- coding: utf-8 -*-
import json
from bs4 import BeautifulSoup

class StudentInfo:
    # init
    def __init__(self, enroll_year, basic_rules, credit_details):
        self.name = '' # 學生姓名
        self.class_id = '' # 班級代碼
        self.class_name = '' # 班級名稱
        self.id = '' # 學號
        self.enroll_year = enroll_year # 入學年度(學號前三碼)
        self.majors = { # 學程
            '主修學程一': {
                '學程名稱': basic_rules['學系選修']['主修學程一'], # ex. '資訊軟體學程'
                '所屬學系': basic_rules['學系選修']['主修學程一所屬學系'], # ex. '資訊工程學系'
                '對應xlsx名': basic_rules['學系選修']['學程細項'][basic_rules['學系選修']['主修學程一']]['對應xlsx名'] # ex. '資工'
            },
            '主修學程二': {
                '學程名稱': basic_rules['學系選修']['主修學程二'],
                '所屬學系': basic_rules['學系選修']['主修學程二所屬學系'],
                '對應xlsx名': basic_rules['學系選修']['學程細項'][basic_rules['學系選修']['主修學程二']]['對應xlsx名']
            },
            '副修學程': {
                '學程名稱': basic_rules['學系選修']['副修學程'],
                '所屬學系': basic_rules['學系選修']['副修學程所屬學系'],
                '對應xlsx名': basic_rules['學系選修']['學程細項'][basic_rules['學系選修']['副修學程']]['對應xlsx名']
            }
        }
        self.cur_semester = '' # 目前學期
        self.survey_finish_rate = '' # 教學評量問卷填答率
        self.cross_bits = [] # 跨/就/微學程
        self.sys_eng_course_pass = False # 學校系統內部判斷是否通過英文學程
        self.sys_eng_courses = [] # 學校系統內部認列的全英文課程
        self.select_system_open = False # 選課系統是否開放
        self.pass_credits = '0' # 已修畢總數分
        self.current_credits = '0' # 正在修總習學分數
        self.order = ['基本知能', '通識基礎必修', '通識延伸選修', '學系必修', '學系選修', '自由選修', '其他選修']
        self.sub_total_credits = {
            '基本知能': '0',
            '通識基礎必修': '0',
            '通識延伸選修': '0',
            '學系必修': '0',
            '學系選修': '0',
            '自由選修': '0',
            '其他選修': '0'
        }
        self.religion_mapping= { # P_KIND
            # 通識基礎必修
            '2': '天',
            '3': '人',
            '4': '物',
            '5': '我',
            # 通識延伸選修
            '6': '天',
            '7': '人',
            '8': '物',
            '9': '我'
        }
        self.historical_course_list = [] # 歷年修課清單
        self.unfinished_courses = { # 未修的課
            '基本知能': [],
            '通識基礎必修': [],
            '通識延伸選修': [],
            '學系必修': [],
            '學系選修': [],
            '自由選修': []
        }
        self.sorted_historical_courses = [] # 按照self.order排序的歷年修課清單
        self.course_properties_mapping = {} # 歷年課程對應的屬性
        self.chose_list = [] # 已選上的課程清單
        self.future_courses = {} # 將已選上的課程清單轉為預排課表
        self.register_list = [] # 登記清單
        self.track_list = [] # 追蹤清單
        self.basic_rules = basic_rules # 基本畢業條件
        self.credit_details = credit_details # 各學程之必修/核心/選修
    
    def __extract_properties(self, course): # private method
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
        return course_name, course_properties
    
    def read(self, basic_user_info, historical_courses, total_overview, course_properties):
        # 選課系統_基本資料.json (basic_user_info)
        basic_info = basic_user_info['st_info'][0]
        self.name = basic_info['STMD_NAME'].strip()
        self.class_id = basic_info['STMD_CUR_DPT'].strip()
        self.class_name = basic_info['STMD_DPT_NAME'].strip()
        self.id = basic_info['IDCODE'].strip()
        self.survey_finish_rate = basic_info['SURVEY_FINISH_RATE'].strip() + '%'
        self.cross_bits = [name.strip() for temp_dict in basic_info['CROSS_BITS_LIST'] for _, name in temp_dict.items()] # 跨/就/微學程

        # 歷年修課.json (historical_courses)
        self.cur_semester = historical_courses['YEAR_TERM'].strip()
        self.historical_course_list = historical_courses['STD_COURSE_LIST'] # TODO: parse
        self.sys_eng_course_pass = historical_courses['STD_ENGLISH_PASS']
        self.sys_eng_courses = historical_courses['STD_FULL_ENGLISH'] # TODO: parse

        # 選課系統_總覽.json (total_overview)
        self.select_system_open = total_overview['sys_open']
        self.chose_list = total_overview['take_course_get'] # TODO: parse
        self.register_list = total_overview['register_get'] # TODO: parse
        self.track_list = total_overview['track_get'] # TODO: parse

        # 歷年修課與狀態表.html (course_properties)
        course_properties = BeautifulSoup(course_properties, 'html.parser')
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
            course_name, course_properties = self.__extract_properties(course)
            self.course_properties_mapping[course_name] = course_properties
    
    def parse(self):
        # self.historical_course_list
        if self.historical_course_list == []:
            self.historical_course_list = {}
        else:
            temp_dict = {}
            i = 0
            for course_dict in self.historical_course_list:
                # extract course properties again
                """
                MyMentor的資料(self.historical_course_list)不會記錄Myself認列的全英文課程
                因此要再check過一遍，如'(就)(P)(英)人生哲學'
                在self.read()中"## extract properties"只會抓出MyMentor紀錄的'(就)(P)'
                Myself紀錄的歷屆修課之課名key: 'CURS_NM_C_S_A'會是'(英)人生哲學'
                因此還要重新parse過並將新的屬性加入，如果parse完發現mapping沒紀錄過(理論上這是不會發生的)就直接加入
                """
                course_name, course_properties = self.__extract_properties(course_dict['CURS_NM_C_S_A'].strip())
                if course_name in self.course_properties_mapping:
                    if course_properties: # to prevent empty properties cover the old properties
                        for course_property in course_properties:
                            if course_property not in self.course_properties_mapping[course_name]:
                                self.course_properties_mapping[course_name].append(course_property)
                else: # to prevent new course that not in mapping
                    self.course_properties_mapping[course_name] = course_properties
                # add infos
                temp_dict[course_name] = {
                    '課程代碼': course_dict['OP_CODE_A'].strip(), # ex. 'CS111E'
                    '學分數': str(course_dict['OP_CREDIT_A']), # ex. '3'
                    '課程性質': self.course_properties_mapping[course_name], # ex. ['程', '跨']
                    '期程': course_dict['OP_QUALITY_A'].strip(), # ex. '半'
                    '修畢學期': course_dict['PASS_YEARTERM'].strip(), # ex. '1121'
                    '分數': course_dict['SCORE_FNAL'].strip(), # ex. '83'
                    '學分性質': '', # ex. '學系選修'
                    '修課狀態': '正在修習' if course_dict['PASS_YEARTERM'] == self.cur_semester else '已修習',
                    '課程所屬學程性質': { # ex. {'主修學程一': '', '主修學程二': '', '副修學程': ''}
                        '主修學程一': '',
                        '主修學程二': '',
                        '副修學程': ''
                    },
                    '天人物我類別': '', # ex. ''
                    '資工四大類類別': [], # ex. []
                    '審查備註': { # ex. {'主修學程一': '', '主修學程二': '', '副修學程': ''}
                        '主修學程一': '',
                        '主修學程二': '',
                        '副修學程': ''
                    }
                }
                if temp_dict[course_name]['修課狀態'] == '正在修習':
                    self.current_credits = str(int(self.current_credits) + course_dict['OP_CREDIT_A'])
                else:
                    self.pass_credits = str(int(self.pass_credits) + course_dict['OP_CREDIT_A'])
                # judge type by the above infos (基本知能/通識基礎必修...)
                # 基本知能
                ## 注意'實用英文'的括號為全型，學校課名命名規則就是沒有規則
                if any(course_name in name for name in self.basic_rules['基本知能']) or \
                    any(name in course_name for name in self.basic_rules['基本知能']) or \
                        'GR' in temp_dict[course_name]['課程代碼'] or \
                            course_name in ['體育一', '體育二', '體育三', '體育四', '體育五', '體育六']: # 'GR': 體育興趣, 舊制體育
                    temp_dict[course_name]['學分性質'] = '基本知能'
                # 通識基礎必修
                ## '自然科學與人工智慧'屬於'自然科學與人工智慧導論'，但'人工智慧導論'是小大一暑期先修課程為自由學分
                elif course_name in [name for four_type in self.basic_rules['通識基礎必修'] for type_name in four_type \
                    for name in self.basic_rules['通識基礎必修'][type_name]] or \
                        course_name == '自然科學與人工智慧':
                    temp_dict[course_name]['天人物我類別'] = self.religion_mapping[course_dict['P_KIND'].strip()] # 2 ~ 5
                    temp_dict[course_name]['學分性質'] = '通識基礎必修'
                # 通識延伸選修
                ## 基本上是'GE'開頭，但'CO'開頭的也有可能，不過我沒加
                elif 'GE' in temp_dict[course_name]['課程代碼']:
                    temp_dict[course_name]['天人物我類別'] = self.religion_mapping[course_dict['P_KIND'].strip()] # 6 ~ 9
                    temp_dict[course_name]['學分性質'] = '通識延伸選修'
                # 學系必修
                ## 需要雙向比對, ex. course_name = '機率與統計' -in-> name = '機率與統計(一)'; ex. course_name = '電子學(一)' <-in- name = '電子學'
                elif any(course_name in name for name in self.basic_rules['學系必修']) or \
                    any(name in course_name for name in self.basic_rules['學系必修']):
                    temp_dict[course_name]['學分性質'] = '學系必修'
                else:
                    # 學系選修
                    types = ['必修', '核心', '選修']
                    order = ['主修學程一', '主修學程二', '副修學程']
                    four_type_of_programs_mapping = {
                        program: list(self.credit_details['資工'][program]['選修']['認列四大類'].keys()) \
                            for program in ['資訊硬體學程', '資訊軟體學程', '資訊應用學程']
                    }
                    ## 查詢課程是否為11個學程的必修/核心/選修
                    for major in order:
                        major_info = self.majors[major]
                        for cur_type in types:
                            courses = self.credit_details[major_info['對應xlsx名']][major_info['學程名稱']][cur_type]
                            if not (major_info['對應xlsx名'] == '資工' and cur_type == '選修'):
                                if course_name in courses['課程']:
                                    temp_dict[course_name]['學分性質'] = '學系選修'
                                    temp_dict[course_name]['課程所屬學程性質'][major] = cur_type
                                    temp_dict[course_name]['審查備註'][major] = \
                                        self.credit_details[major_info['對應xlsx名']][major_info['學程名稱']][cur_type]['課程'][course_name]['審查備註']
                                    break
                            else:
                                # 只query此資工學程認列的選修四大類
                                for four_type in self.credit_details[major_info['對應xlsx名']][major_info['學程名稱']][cur_type]['認列四大類']:
                                    course_dict = self.credit_details[major_info['對應xlsx名']]['四大類'][four_type]['課程']
                                    # 如果課名有在四大類但不是資工(CS)或校際TAICA聯盟(ST)開課就會篩掉
                                    if course_name in course_dict and \
                                        ('CS' in temp_dict[course_name]['課程代碼'] or \
                                            'ST' in temp_dict[course_name]['課程代碼']):
                                        temp_dict[course_name]['學分性質'] = '學系選修'
                                        temp_dict[course_name]['課程所屬學程性質'][major] = cur_type
                                        temp_dict[course_name]['資工四大類類別'].append(four_type)
                                        temp_dict[course_name]['最終認定所屬主修學程'] = ''
                                        temp_dict[course_name]['審查備註'][major] = self.credit_details[major_info['對應xlsx名']]['四大類']['審查備註']
                    # 電資學系選修: 'UP'
                    if temp_dict[course_name]['學分性質'] == '' and \
                        'UP' in temp_dict[course_name]['課程代碼'] and \
                            '環境服務學習' not in course_name:
                        temp_dict[course_name]['學分性質'] = '學系選修'
                    elif temp_dict[course_name]['學分性質'] == '':
                        # 自由選修
                        ## 輔雙跨就微PBL, 磨課師(CO), 專業自主學習
                        ## TODO: 不確定輔雙要怎麼判斷
                        if bool(set(['輔', '雙', '跨', '就', '微', 'P']) & set(temp_dict[course_name]['課程性質'])) or \
                            'CO' in temp_dict[course_name]['課程代碼'] or course_name == '專業自主學習':
                            temp_dict[course_name]['學分性質'] = '自由選修'
                        # 其他選修
                        ##
                        else:
                            temp_dict[course_name]['學分性質'] = '其他選修'
            self.historical_course_list = temp_dict
        
        # self.sys_eng_courses
        if self.sys_eng_courses == []:
            self.sys_eng_course_pass = {}
        else:
            temp_dict = {}
            """
            for course_dict in self.sys_eng_courses:
                temp_dict[course_dict['CURS_NM_C_S'].strip()] = {
                    '課程代碼': course_dict['OP_CODE'].strip(),
                    '學分數': course_dict['OP_CREDIT'].strip(),
                    '修畢學期': course_dict['YEAR_TERM'].strip(),
                    '分數': course_dict['SCORE_FNAL'].strip()
                }
            """
            self.sys_eng_courses = temp_dict

        # self.chose_list
        if self.chose_list == []:
            self.chose_list = {}
        else:
            temp_dict = {}
            for course_dict in self.chose_list:
                temp_dict[course_dict['CNAME'].strip()] = {
                    '課程代碼': course_dict['OP_CODE'].strip() if 'OP_CODE' in course_dict else '',
                    '學分數': course_dict['OP_CREDIT'].strip() if 'OP_CREDIT' in course_dict else '',
                    '期程': course_dict['OP_QUALITY'].strip() if 'OP_QUALITY' in course_dict else '',
                    '上課時間': [substr for substr in course_dict['OP_TIME_123'].split() if substr] if 'OP_TIME_123' in course_dict else [],
                    '上課地點': [substr for substr in course_dict['OP_RM_NAME_123'].split() if substr] if 'OP_RM_NAME_123' in course_dict else [],
                    '教授': course_dict['TEACHER'].strip() if 'TEACHER' in course_dict else '',
                    '必選修': course_dict['OP_STDY'].strip() if 'OP_STDY' in course_dict else '',
                    '開課學系': course_dict['DEPT_NAME'].strip() if 'DEPT_NAME' in course_dict else '',
                }
            self.chose_list = temp_dict
        
        # self.register_list
        if self.register_list == []:
            self.register_list = {}
        else:
            pass
        
        # self.track_list
        if self.track_list == []:
            self.track_list = {}
        else:
            temp_dict = {}
            """
            for track_dict in self.track_list:
                temp_dict[track_dict['CNAME'].strip()] = {
                    '課程代碼': track_dict['OP_CODE'].strip(),
                    '學分數': track_dict['OP_CREDIT'].strip(),
                    '上課時間': [substr for substr in track_dict['OP_TIME_123'].split() if substr],
                    '上課地點': track_dict['OP_RM_NAME_1'].strip() if 'OP_RM_NAME_1' in track_dict else '',
                    '教授': track_dict['TEACHER'].strip() if 'TEACHER' in track_dict else '',
                    '必選修': track_dict['OP_STDY'].strip(),
                    '開課學系': track_dict['DEPT_NAME'].strip()
                }
            """
            self.track_list = temp_dict
    
    def sort_historical_courses(self):
        # sort by self.order
        sorted_courses = {credit_type: [] for credit_type in self.order}
        for course, course_dict in self.historical_course_list.items():
            credit_type = course_dict['學分性質']
            sorted_courses[credit_type].append((course, course_dict))
        # sort by credit type (in the order of self.order)
        for credit_type in self.order:
            # calculate sub_total_credits
            self.sub_total_credits[credit_type] = str(sum([int(course_dict['學分數']) for course, course_dict in sorted_courses[credit_type]]))
            # sort
            match(credit_type):
                case '基本知能':
                    course_order = ['英文(一)', '英文(二)', '實用英文（一）', '實用英文（二）', '英語聽講(一)', '英語聽講(二)', \
                        '體育一', '體育二', '體育三', '體育四', '體育五', '體育六']
                    sorted_courses[credit_type] = sorted(sorted_courses[credit_type], \
                        key = lambda x: (course_order.index(x[0]) if x[0] in course_order else float('inf'), x[1]['修畢學期']))
                case '通識基礎必修':
                    course_order = [key for _, course_dict in self.basic_rules['通識基礎必修'].items() for key in course_dict]
                    sorted_courses[credit_type] = sorted(sorted_courses[credit_type], \
                        key = lambda x: (course_order.index('自然科學與人工智慧導論' if x[0] == '自然科學與人工智慧' else x[0] \
                            ) if x[0] in course_order or x[0] == '自然科學與人工智慧' else float('inf'), x[1]['修畢學期']))
                case '通識延伸選修':
                    course_order = ['天', '人', '物', '我']
                    sorted_courses[credit_type] = sorted(sorted_courses[credit_type], \
                        key = lambda x: (course_order.index(x[1]['天人物我類別']) if x[1]['天人物我類別'] in course_order else float('inf'), x[1]['修畢學期']))
                case '學系必修':
                    course_order = [key for key in self.basic_rules['學系必修']]
                    sorted_courses[credit_type] = sorted(sorted_courses[credit_type], \
                        key = lambda x: (course_order.index('機率與統計' if x[0] == '機率與統計(一)' else \
                            '電路實驗(一)' if x[0] == '電路實驗' else '電子實驗(一)' if x[0] == '電子實驗' else x[0]) \
                                if x[0] in course_order or x[0] == '機率與統計(一)' or x[0] == '電路實驗' or x[0] == '電子實驗' \
                                    else float('inf'), x[1]['修畢學期']))
                case '學系選修':
                    course_order = [('主修學程一', '必修'), ('主修學程二', '必修'), ('主修學程一', '核心'), \
                        ('主修學程二', '核心'), ('主修學程一', '選修'), ('主修學程二', '選修'), \
                            ('副修學程', '必修'), ('副修學程', '核心'), ('副修學程', '選修'),
                                ('主修學程一', ''), ('主修學程二', ''), ('副修學程', '')]
                    sorted_courses[credit_type] = sorted(sorted_courses[credit_type], \
                        key = lambda x: ((lambda key, value: (course_order.index((key, value)) \
                            if (key, value) in course_order and x[1]['課程所屬學程性質'] != {'主修學程一': '', '主修學程二': '', '副修學程': ''} \
                                else float('inf')))(list(x[1]['課程所屬學程性質'].keys())[0], x[1]['課程所屬學程性質'][list(x[1]['課程所屬學程性質'].keys())[0]]), \
                                    x[1]['修畢學期']))
                case '自由選修':
                    course_order = ['輔', '雙', '跨', '就', '微', 'P']
                    sorted_courses[credit_type] = sorted(sorted_courses[credit_type], \
                        key = lambda x: (
                            # 1. '課程性質' != [] and 任一性質 in course_order -> 按min_index排序
                            min((course_order.index(n) for n in x[1]['課程性質'] if n in course_order), default = float('inf')),
                            # 2. '專業自主學習' 排在以上順序的後面
                            0 if x[0] == '專業自主學習' else 1,
                            # 3. 課程性質 == [] -> 排在後面
                            len(x[1]['課程性質']),
                            # 4. '修畢學期'
                            x[1]['修畢學期']))
                case _:
                    course_order = ['國防軍訓-國防科技', '國防軍訓-國防政策', '國防軍訓-國際情勢', '國防軍訓-防衛動員', '國防軍訓-全民國防', \
                        '環境服務學習（一）', '環境服務學習（二）']
                    sorted_courses[credit_type] = sorted(sorted_courses[credit_type], \
                        key = lambda x: (course_order.index(x[0]) if x[0] in course_order else float('inf'), x[1]['修畢學期']))
        self.sorted_historical_courses = sorted_courses

    # TODO: 根據學程判斷並增加未修的學系必修與學系選修
    def set_unfinished_courses(self):
        basic_mapping = {
            '基本知能': {
                '英文(一)': False,
                '英文(二)': False,
                '實用英文（一）': False,
                '實用英文（二）': False,
                '英語聽講(一)': False,
                '英語聽講(二)': False,
                '體育一': False
            },
            '通識基礎必修': {
                '宗教哲學': False,
                '人生哲學': False,
                '台灣政治與民主': False,
                '法律與現代生活': False,
                '當代人權議題與挑戰': False,
                '生活社會學': False,
                '全球化大議題': False,
                '經濟學的世界': False,
                '區域文明史': False,
                '文化思想史': False,
                '運算思維與程式設計': False,
                '自然科學與人工智慧導論': False, # 自然科學與人工智慧
                '文學經典閱讀': False,
                '語文與修辭': False
            },
            '學系必修': {
                '微積分(上)': False,
                '微積分(下)': False,
                '普通物理(一)': False,
                '普通物理(二)': False,
                '普通物理實驗(一)': False,
                '普通物理實驗(二)': False,
                '計算機概論(一)': False,
                '計算機概論(二)': False,
                '線性代數': False,
                '機率與統計': False, # 機率與統計(一)
                '電子學(一)': False,
                '電子實驗(一)': False, # 電子實驗
                '電路學(一)': False,
                '電路實驗(一)': False, # 電路實驗
                '專題製作(一)': False,
                '專題製作(二)': False
            },
            '通識延伸選修': {
                '工程倫理': False # 需為電資學院開課，但資料不足無法判斷
            }
        }
        free_pe_courses = [] # 除了體育一之外的體育課, len 要 >= 3
        free_four_religion_types = { # 通識延伸選修
            '天': '0',
            '人': '0',
            '物': '0',
            '我': '0'
        }

        # fetch program courses
        major_status = {}
        for major in ['主修學程一', '主修學程二', '副修學程']:
            major_status[major] = {}
            for cur_type in ['必修', '核心', '選修']:
                major_status[major][cur_type] = {}
                if not(self.majors[major]['對應xlsx名'] == '資工' and cur_type == '選修'):
                    major_status[major][cur_type] = {
                        course: False for course in self.credit_details[self.majors[major]['對應xlsx名']] \
                            [self.majors[major]['學程名稱']][cur_type]['課程']
                    }
                else:
                    major_status[major][cur_type] = {
                        course: False for four_type in self.credit_details['資工'][self.majors[major]['學程名稱']][cur_type]['認列四大類'] \
                            for course in self.credit_details['資工']['四大類'][four_type]['課程'] # key必為唯一所以不用檢查重複
                    }

        # calculate
        for credit_type, courses in self.sorted_historical_courses.items():
            for course, course_dict in courses:
                match(credit_type):
                    case '基本知能':
                        if course in basic_mapping[credit_type]:
                            basic_mapping[credit_type][course] = True
                        elif 'GR' in course_dict['課程代碼'] or \
                            course in ['體育二', '體育三', '體育四', '體育五', '體育六']:
                            free_pe_courses.append(course)
                    case '通識基礎必修':
                        if course in basic_mapping[credit_type]:
                            basic_mapping[credit_type][course] = True
                        elif course == '自然科學與人工智慧':
                            basic_mapping[credit_type]['自然科學與人工智慧導論'] = True
                    case '學系必修':
                        if course in basic_mapping[credit_type]:
                            basic_mapping[credit_type][course] = True
                        elif course == '機率與統計(一)':
                            basic_mapping[credit_type]['機率與統計'] = True
                        elif course == '電子實驗':
                            basic_mapping[credit_type]['電子實驗(一)'] = True
                        elif course == '電路實驗':
                            basic_mapping[credit_type]['電路實驗(一)'] = True
                    case '學系選修':
                        for major in ['主修學程一', '主修學程二', '副修學程']:
                            for cur_type in ['必修', '核心', '選修']:
                                if course in major_status[major][cur_type]:
                                    major_status[major][cur_type][course] = True
                    case '通識延伸選修':
                        if course in basic_mapping[credit_type]:
                            basic_mapping[credit_type][course] = True
                        else:
                            free_four_religion_types[course_dict['天人物我類別']] = \
                                str(int(free_four_religion_types[course_dict['天人物我類別']]) + \
                                    int(course_dict['學分數']))
                    case '自由選修':
                        pass
                    case _:
                        pass
        
        # judge and append unfinished courses
        for credit_type in ['基本知能', '通識基礎必修', '通識延伸選修', '學系必修', '學系選修', '自由選修']:
            if credit_type == '基本知能':
                for course, is_finished in basic_mapping[credit_type].items():
                    if not is_finished:
                        self.unfinished_courses[credit_type].append([course] + [''] * 6 + ['未修習'] + [''] * 10)
                if len(free_pe_courses) < 3:
                    chinese_num_mapping = { 1: '一', 2: '二', 3: '三' }
                    for i in range(3 - len(free_pe_courses)):
                        self.unfinished_courses[credit_type].append([f'體育興趣{chinese_num_mapping[i + 1]}'] + [''] * 6 + ['未修習'] + [''] * 10)
            elif credit_type == '通識基礎必修':
                four_types = ['天', '人', '物', '我']
                has_citizen = False
                has_history = False
                course_four_type_mapping = { course: '' for course in basic_mapping[credit_type] }
                for course, is_finished in basic_mapping[credit_type].items():
                    for four_type in four_types:
                        if course in self.basic_rules[credit_type][four_type]:
                            course_four_type_mapping[course] = four_type
                            if four_type == '人' and is_finished:
                                if self.basic_rules[credit_type]['人'][course]['性質'] == '公民':
                                    has_citizen = True
                                else:
                                    has_history = True
                            break
                for course, is_finished in basic_mapping[credit_type].items():
                    if not is_finished:
                        if course_four_type_mapping[course] == '人':
                            if (self.basic_rules[credit_type]['人'][course]['性質'] == '公民' and has_citizen) or \
                                (self.basic_rules[credit_type]['人'][course]['性質'] == '歷史' and has_history):
                                continue
                        self.unfinished_courses[credit_type].append([course] + [''] * 6 + ['未修習', f] + [''] * 9)
            elif credit_type == '通識延伸選修':
                # 確認天人物我最低學分數
                for four_type, num in free_four_religion_types.items():
                    if int(num) < self.basic_rules[credit_type][four_type]['最低應修學分數']:
                        remaining_credits = str(self.basic_rules[credit_type][four_type]['最低應修學分數'] - int(num))
                        course_name = ''
                        orc = '' # 其它備註 other review comments
                        if four_type == '人' and not basic_mapping[credit_type]['工程倫理']:
                            course_name = '工程倫理'
                            orc = '需為電資學院指定'
                        self.unfinished_courses[credit_type].append([course_name, '', remaining_credits] + [''] * 4 + ['未修習'] + [''] * 8 + [orc, ''])
                # 確認畢業應修最低學分數
                if int(self.sub_total_credits[credit_type]) < self.basic_rules['畢業應修最低學分數'][credit_type]:
                    remaining_credits = str(self.basic_rules['畢業應修最低學分數'][credit_type] - int(self.sub_total_credits[credit_type]))
                    self.unfinished_courses[credit_type].append(['', '', remaining_credits] + [''] * 4 + ['未修習'] + [''] * 10)
            elif credit_type == '學系必修':
                for course, is_finished in basic_mapping[credit_type].items():
                    if not is_finished:
                        self.unfinished_courses[credit_type].append([course] + [''] * 6 + ['未修習'] + [''] * 10)
            elif credit_type == '學系選修':
                # set 資工 first
                without_same_courses = set()
                # 雙資工: 必修+核心全修, 選修有條件
                if self.majors['主修學程一']['對應xlsx名'] == '資工' and self.majors['主修學程二']['對應xlsx名'] == '資工':
                    must_and_course_msgs = []
                    four_type_msgs = []
                    has_judged_four_type = False
                    for major in ['主修學程一', '主修學程二']:
                        for cur_type in ['必修', '核心', '選修']:
                            for course, is_finished in major_status[major][cur_type].items():
                                if not is_finished and course not in without_same_courses:
                                    # record to avoid repeating same course
                                    without_same_courses.add(course)
                                    credit_and_type_mapping = {
                                        '學分數': '',
                                        '主修學程一': {}, # '必核選', '審查備註'
                                        '主修學程二': {},
                                        '副修學程': {}
                                    }
                                    if cur_type != '選修':
                                        # find it's type of major1, major2, sub_major
                                        for temp_major in ['主修學程一', '主修學程二', '副修學程']:
                                            for temp_type in ['必修', '核心']:
                                                major_name = self.majors[temp_major]['學程名稱']
                                                if major_name in self.credit_details['資工'] and \
                                                    course in self.credit_details['資工'][major_name][temp_type]['課程']:
                                                    if credit_and_type_mapping['學分數'] == '':
                                                        credit_and_type_mapping['學分數'] = self.credit_details['資工'][major_name][temp_type]['課程'][course]['學分數']
                                                    credit_and_type_mapping[temp_major]['必核選'] = temp_type
                                                    credit_and_type_mapping[temp_major]['審查備註'] = self.credit_details['資工'][major_name][temp_type]['課程'][course]['審查備註']
                                                    break
                                                else:
                                                    credit_and_type_mapping['學分數'] = ''
                                                    credit_and_type_mapping[temp_major]['必核選'] = ''
                                                    credit_and_type_mapping[temp_major]['審查備註'] = ''
                                        must_and_course_msgs.append([course, '', credit_and_type_mapping['學分數']] + [''] * 4 + \
                                            ['未修習', '', credit_and_type_mapping['主修學程一']['必核選'], \
                                                credit_and_type_mapping['主修學程二']['必核選'], \
                                                    credit_and_type_mapping['副修學程']['必核選'], '', '', \
                                                        credit_and_type_mapping['主修學程一']['審查備註'], \
                                                            credit_and_type_mapping['主修學程二']['審查備註'], \
                                                                credit_and_type_mapping['副修學程']['審查備註'], ''])
                                    elif not has_judged_four_type:
                                        has_judged_four_type = True
                                        # find 四大類
                                        major1_name = self.majors['主修學程一']['學程名稱']
                                        major2_name = self.majors['主修學程二']['學程名稱']
                                        major1_four_type = list(self.credit_details['資工'][major1_name]['選修']['認列四大類'].keys())
                                        major2_four_type = list(self.credit_details['資工'][major2_name]['選修']['認列四大類'].keys())
                                        
                                        # get four-type courses of two majors
                                        major1_courses = {}
                                        major2_courses = {}
                                        other_courses = {}
                                        for c_set in self.sorted_historical_courses[credit_type]: # c_set[0]: course name, c_set[1]: course dict
                                            if c_set[1]['資工四大類類別'] != []:
                                                condi1 = any(four_type in major1_four_type for four_type in c_set[1]['資工四大類類別'])
                                                condi2 = any(four_type in major2_four_type for four_type in c_set[1]['資工四大類類別'])
                                                if condi1 or condi2:
                                                    if condi1:
                                                        major1_courses[c_set[0]] = {
                                                            '學分數': int(c_set[1]['學分數']),
                                                            '所屬四大類類別': c_set[1]['資工四大類類別'],
                                                        }
                                                    if condi2:
                                                        major2_courses[c_set[0]] = {
                                                            '學分數': int(c_set[1]['學分數']),
                                                            '所屬四大類類別': c_set[1]['資工四大類類別'] }
                                                else:
                                                    other_courses[c_set[0]] = {
                                                        '學分數': int(c_set[1]['學分數']),
                                                        '所屬四大類類別': c_set[1]['資工四大類類別'] }
                                        
                                        # set order
                                        order = []
                                        if len(major1_courses) <= len(major2_courses):
                                            order = [{
                                                '課程': major1_courses,
                                                '學程名稱': major1_name,
                                                '認列四大類': major1_four_type
                                            }, {
                                                '課程': major2_courses,
                                                '學程名稱': major2_name,
                                                '認列四大類': major2_four_type
                                            }, {
                                                '課程': other_courses,
                                                '學程名稱': '其它',
                                                '認列四大類': []
                                            }]
                                        else:
                                            order = [{
                                                '課程': major2_courses,
                                                '學程名稱': major2_name,
                                                '認列四大類': major2_four_type
                                            }, {
                                                '課程': major1_courses,
                                                '學程名稱': major1_name,
                                                '認列四大類': major1_four_type
                                            }, {
                                                '課程': other_courses,
                                                '學程名稱': '其它',
                                                '認列四大類': []
                                            }]
                                        
                                        # set credits and records
                                        single_lowest_credit = int(self.credit_details['資工']['最低應修學分數']['雙資工']['選修各學程'])
                                        total_lowest_credit = int(self.credit_details['資工']['最低應修學分數']['雙資工']['選修總共'])
                                        single_major_credits = {
                                            major1_name: 0,
                                            major2_name: 0,
                                            '其它': 0
                                        }
                                        ## remain = set()
                                        program_of_course = {}

                                        # judge
                                        for stage in [0, 1, 2, 3, 4]:
                                            for idx, l in enumerate(order):
                                                if stage != 0 and l['學程名稱'] not in [major1_name, major2_name]:
                                                    continue
                                                for course_name, course_dict in l['課程'].items():
                                                    if course_name not in program_of_course:
                                                        # 優先選只認列一個四大類的課程
                                                        condi_only_one_four_type = len(course_dict['所屬四大類類別']) == 1
                                                        # 單一主修學程 < 6學分
                                                        condi_single_lower_than_6 = single_major_credits[l['學程名稱']] < 6
                                                        # 兩主修學程共 < 15學分
                                                        condi_total_lower_than_15 = single_major_credits[major1_name] + single_major_credits[major2_name] < 15
                                                        # stage 0 (只針對認列一個四大類的課程) 遇到非兩個主修認列的四大類要加入其它 
                                                        # 因為這個階段出現的課程必然只有認列一個四大類
                                                        # 當此四大類不在兩主修認列的四大類中就要丟到其它
                                                        if stage == 0 and condi_only_one_four_type and l['學程名稱'] not in [major1_name, major2_name]:
                                                            single_major_credits[l['學程名稱']] += course_dict['學分數']
                                                            program_of_course[course_name] = l['學程名稱'] # '其它'
                                                            continue
                                                        # 正常流程
                                                        if (stage == 0 and condi_only_one_four_type and condi_single_lower_than_6) or \
                                                            (stage == 1 and condi_single_lower_than_6) or \
                                                                (stage == 2 and condi_only_one_four_type and condi_total_lower_than_15) or \
                                                                    (stage == 3 and condi_total_lower_than_15) or \
                                                                        (stage == 4):
                                                            single_major_credits[l['學程名稱']] += course_dict['學分數']
                                                            program_of_course[course_name] = l['學程名稱']
                                                            # if stage == 4: # 可用於判斷是否能用作自由選修
                                                            #     remain.add(course_name)
                                        
                                        # write back the final four type
                                        for c_set in self.sorted_historical_courses[credit_type]: # c_set[0]: course name, c_set[1]: course dict
                                            if c_set[1]['資工四大類類別'] != []:
                                                c_set[1]['最終認定所屬主修學程'] = program_of_course[c_set[0]] if program_of_course[c_set[0]] != '其它' else ''
                                        
                                        # write back the still-need credit msgs
                                        accumulated_credit = 0
                                        if single_major_credits[major1_name] < single_lowest_credit:
                                            need = single_lowest_credit - single_major_credits[major1_name]
                                            accumulated_credit += need
                                            four_type_msgs.append(['', '', need] + [''] * 4 + ['未修習', '', '選修', '', ''] + [' / '.join([p for p in major1_four_type if major1_four_type != []]), major1_name] + [''] * 4)
                                        if single_major_credits[major2_name] < single_lowest_credit:
                                            need = single_lowest_credit - single_major_credits[major2_name]
                                            accumulated_credit += need
                                            four_type_msgs.append(['', '', need] + [''] * 4 + ['未修習', '', '', '選修', ''] + [' / '.join([p for p in major2_four_type if major2_four_type != []]), major2_name] + [''] * 4)
                                        if single_major_credits[major1_name] + single_major_credits[major2_name] < total_lowest_credit:
                                            remain_credit = total_lowest_credit - single_major_credits[major1_name] - single_major_credits[major2_name] - accumulated_credit
                                            all_four_type = major1_four_type + major2_four_type
                                            four_type_msgs.append(['', '', remain_credit] + [''] * 4 + ['未修習', '', '選修', '選修', ''] + [' / '.join([p for p in all_four_type if all_four_type != []]), f'{major1_name} / {major2_name}'] + [''] * 4)
                        # 單資工: 必修全修, 核心有條件
                    # append 必修/核心 first, then 選修
                    for msg_list in [must_and_course_msgs, four_type_msgs]:
                        for msg in msg_list:
                            self.unfinished_courses[credit_type].append(msg)
                #elif self.majors[major]['對應xlsx名'] == '資工':
                #    pass
                # judge program of majors
                # 雙資工不用管副修
                # 單資工的資工學程不用管選修
                # 其它
                # TODO
                ## 非資工的必修/核心不能跨學程重複認列
                ## 工程數學(一)大一未選學程時預設為必修，但只有通訊/電子/電機底下學程才是必修
                ## 因此如果是主修的兩個學程中有此門課才要放到學系選修
                ## 不然就是按照課程所屬課程性質
                pass
            else: # 自由選修
                if int(self.sub_total_credits[credit_type]) < self.basic_rules['畢業應修最低學分數'][credit_type]:
                    remaining_credits = str(self.basic_rules['畢業應修最低學分數'][credit_type] - int(self.sub_total_credits[credit_type]))
                    self.unfinished_courses[credit_type].append(['', '', remaining_credits] + [''] * 4 + ['未修習'] + [''] * 10)
        #print(self.unfinished_courses)
    
    # TODO: 智慧偵測並分配自由選修
    # 會需要改動self.sub_total_credits等
    # 可能砍掉不做這個
    def detect_and_distribute_free_elective_courses(self):
        pass
    
    def generate_future_courses(self):
        for day in ['週一', '週二', '週三', '週四', '週五', '週六', '週日']:
            self.future_courses[day] = {
                'A (07:10 ~ 08:00)': '',
                '1 (08:10 ~ 09:00)': '',
                '2 (09:10 ~ 10:00)': '',
                '3 (10:10 ~ 11:00)': '',
                '4 (11:10 ~ 12:00)': '',
                'B (12:10 ~ 13:00)': '',
                '5 (13:10 ~ 14:00)': '',
                '6 (14:10 ~ 15:00)': '',
                '7 (15:10 ~ 16:00)': '',
                '8 (16:10 ~ 17:00)': '',
                'C (17:05 ~ 17:55)': '',
                'D (18:00 ~ 18:50)': '',
                'E (19:55 ~ 19:45)': '',
                'F (19:50 ~ 20:40)': '',
                'G (20:45 ~ 21:35)': ''
            }
        day_mapping = {
            '1': '週一',
            '2': '週二',
            '3': '週三',
            '4': '週四',
            '5': '週五',
            '6': '週六',
            '7': '週日'
        }
        time_slot_mapping = {
            'A': 'A (07:10 ~ 08:00)',
            '1': '1 (08:10 ~ 09:00)',
            '2': '2 (09:10 ~ 10:00)',
            '3': '3 (10:10 ~ 11:00)',
            '4': '4 (11:10 ~ 12:00)',
            'B': 'B (12:10 ~ 13:00)',
            '5': '5 (13:10 ~ 14:00)',
            '6': '6 (14:10 ~ 15:00)',
            '7': '7 (15:10 ~ 16:00)',
            '8': '8 (16:10 ~ 17:00)',
            'C': 'C (17:05 ~ 17:55)',
            'D': 'D (18:00 ~ 18:50)',
            'E': 'E (19:55 ~ 19:45)',
            'F': 'F (19:50 ~ 20:40)',
            'G': 'G (20:45 ~ 21:35)'
        }
        online_courses = []
        for course, course_dict in self.chose_list.items():
            if course_dict['上課時間'] != []:
                for take_time, take_place in zip(course_dict['上課時間'], course_dict['上課地點']):
                    single_day = take_time.split('-')
                    for time_slot in single_day[1]:
                        self.future_courses[day_mapping[single_day[0]]][time_slot_mapping[time_slot]] = f"{course_dict['課程代碼']} - {course}，{take_place} ({course_dict['教授']}，{course_dict['學分數']}學分)"
            else:
                online_courses.append(f"{course_dict['課程代碼']} - {course} ({course_dict['教授']}，{course_dict['學分數']}學分)")
        self.future_courses['非同步遠距'] = online_courses

    def print_sorted_historical_courses(self):
        print(f'總共修習{len(self.historical_course_list)}門課程，已修過{self.pass_credits}學分，正在修習{self.current_credits}學分')
        print(f"{'-' * 100}")
        for i, credit_type in enumerate(self.order, start = 1):
            print(f'{i}. {credit_type}: {len(self.sorted_historical_courses[credit_type])}門課程，共計{self.sub_total_credits[credit_type]}學分')
            print(f"{'-' * 100}")
            for j, (course, course_dict) in enumerate(self.sorted_historical_courses[credit_type], start = 1):
                print(f" {j}. {course}:")
                print(f" \t課程代碼: {course_dict['課程代碼']}")
                print(f" \t學分數: {course_dict['學分數']}學分")
                print(f" \t期程: {course_dict['期程']}")
                print(f" \t性質: {course_dict['課程性質']}")
                print(f" \t修畢學期: {course_dict['修畢學期']}")
                print(f" \t分數: {course_dict['分數']}")
                print(f" \t必修/核心/選修: {course_dict['課程所屬學程性質']}")
                print(f" \t天人物我類別: {course_dict['天人物我類別']}")
                print(f" \t資工四大類類別: {course_dict['資工四大類類別']}")
                print(f" \t審查備註: {course_dict.get('審查備註', '無')}")
            print(f"{'-' * 100}")
            print()
    
    def write_sorted_historical_courses(self):
        # json
        with open('./Generated/歷年修課.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.sorted_historical_courses, indent = 4, ensure_ascii = False))
        
        # txt
        with open('./Generated/歷年修課.txt', 'w', encoding='utf-8') as file:
            file.write(f'總共修習{len(self.historical_course_list)}門課程，已修過{self.pass_credits}學分，正在修習{self.current_credits}學分\n')
            file.write(f"{'-' * 100}\n")
            for i, credit_type in enumerate(self.order, start = 1):
                file.write(f'{i}. {credit_type}: {len(self.sorted_historical_courses[credit_type])}門課程，共計{self.sub_total_credits[credit_type]}學分\n')
                file.write(f"{'-' * 100}\n")
                
                for j, (course, course_dict) in enumerate(self.sorted_historical_courses[credit_type], start=1):
                    file.write(f" {j}. {course}:\n")
                    file.write(f" \t課程代碼: {course_dict['課程代碼']}\n")
                    file.write(f" \t學分數: {course_dict['學分數']}學分\n")
                    file.write(f" \t期程: {course_dict['期程']}\n")
                    file.write(f" \t性質: {course_dict['課程性質']}\n")
                    file.write(f" \t修畢學期: {course_dict['修畢學期']}\n")
                    file.write(f" \t分數: {course_dict['分數']}\n")
                    file.write(f" \t必修/核心/選修: {course_dict['課程所屬學程性質']}\n")
                    file.write(f" \t天人物我類別: {course_dict['天人物我類別']}\n")
                    file.write(f" \t資工四大類類別: {course_dict['資工四大類類別']}\n")
                    file.write(f" \t審查備註: {course_dict.get('審查備註', '無')}\n")
                
                file.write(f"{'-' * 100}\n\n")