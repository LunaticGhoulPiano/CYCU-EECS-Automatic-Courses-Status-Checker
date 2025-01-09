# -*- coding: utf-8 -*-
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
        self.order = ['基本知能', '通識基礎必修', '通識延伸選修', '學系必修', '學系選修', '自由選修', '其他選修']
        self.historical_course_list = [] # 歷年修課清單
        self.sorted_historical_courses = [] # 按照self.order排序的歷年修課清單
        self.course_properties_mapping = {} # 歷年課程對應的屬性
        self.chose_list = [] # 已選上的課程清單
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
                    '修習時間': course_dict['PASS_YEARTERM'].strip(), # ex. '1121'
                    '分數': course_dict['SCORE_FNAL'].strip(), # ex. '83'
                    '學分性質': '', # ex. '學系選修'
                    '課程所屬學程性質': { # ex. {'主修學程一': '', '主修學程二': '', '副修學程': ''}
                        '主修學程一': '',
                        '主修學程二': '',
                        '副修學程': ''
                    },
                    '四大類類別': [], # ex. []
                    '審查備註': { # ex. {'主修學程一': '', '主修學程二': '', '副修學程': ''}
                        '主修學程一': '',
                        '主修學程二': '',
                        '副修學程': ''
                    }
                }
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
                    temp_dict[course_name]['學分性質'] = '通識基礎必修'
                # 通識延伸選修
                ## 基本上是'GE'開頭，但'CO'開頭的也有可能，不過我沒加
                elif 'GE' in temp_dict[course_name]['課程代碼']:
                    temp_dict[course_name]['學分性質'] = '通識延伸選修'
                # 學系必修
                ## 需要雙向比對, ex. course_name = '機率與統計' -in-> name = '機率與統計(一)'; ex. course_name = '電子學(一)' <-in- name = '電子學'
                elif any(course_name in name for name in self.basic_rules['學系必修']) or \
                    any(name in course_name for name in self.basic_rules['學系必修']):
                    temp_dict[course_name]['學分性質'] = '學系必修'
                    # TODO: 解決工程數學(一)是[電子/電機/通訊]學系必修，同時也是學系選修-必修的問題
                else:
                    # 學系選修
                    ## TODO: 系統程式113入學前為{'資訊硬體學程': '核心', '資訊軟體學程': '必修', '資訊應用學程': '核心'}
                    ## 要問怎麼判定
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
                                        temp_dict[course_name]['四大類類別'].append(four_type)
                                        temp_dict[course_name]['審查備註'][major] = self.credit_details[major_info['對應xlsx名']]['四大類']['審查備註']
                    if temp_dict[course_name]['學分性質'] == '':
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
            for course_dict in self.sys_eng_courses:
                temp_dict[course_dict['CURS_NM_C_S'].strip()] = {
                    '課程代碼': course_dict['OP_CODE'].strip(),
                    '學分數': course_dict['OP_CREDIT'].strip(),
                    '修習時間': course_dict['YEAR_TERM'].strip(),
                    '分數': course_dict['SCORE_FNAL'].strip()
                }
            self.sys_eng_courses = temp_dict

        # self.chose_list
        if self.chose_list == []:
            self.chose_list = {}
        else:
            temp_dict = {}
            for course_dict in self.chose_list:
                temp_dict[course_dict['CNAME'].strip()] = {
                    '課程代碼': course_dict['OP_CODE'].strip(),
                    '學分數': course_dict['OP_CREDIT'].strip(),
                    '期程': course_dict['OP_QUALITY'].strip(),
                    '上課時間': course_dict['OP_TIME_123'].strip(),
                    '上課地點': course_dict['OP_RM_NAME_123'].strip() if 'OP_RM_NAME_123' in course_dict else '',
                    '教授': course_dict['TEACHER'].strip(),
                    '必選修': course_dict['OP_STDY'].strip(),
                    '開課學系': course_dict['DEPT_NAME'].strip()
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
            for track_dict in self.track_list:
                temp_dict[track_dict['CNAME'].strip()] = {
                    '課程代碼': track_dict['OP_CODE'].strip(),
                    '學分數': track_dict['OP_CREDIT'].strip(),
                    '上課時間': track_dict['OP_TIME_123'].strip(),
                    '上課地點': track_dict['OP_RM_NAME_1'].strip() if 'OP_RM_NAME_1' in track_dict else '',
                    '教授': track_dict['TEACHER'].strip(),
                    '必選修': track_dict['OP_STDY'].strip(),
                    '開課學系': track_dict['DEPT_NAME'].strip()
                }
            self.track_list = temp_dict
    
    # TODO: 智慧偵測並分配自由選修
    def automatically_distribute_free_elective_courses(self):
        pass
    
    def sort_historical_courses(self):
        sorted_courses = {credit_type: [] for credit_type in self.order}
        for course, course_dict in self.historical_course_list.items():
            credit_type = course_dict['學分性質']
            sorted_courses[credit_type].append((course, course_dict))
        self.sort_historical_courses = sorted_courses

    def print_sorted_historical_courses(self):
        print(f'總共修習{len(self.historical_course_list)}門課程')
        print(f"-" * 100)
        for credit_type in self.order:
            print(f'{credit_type}: {len(self.sort_historical_courses[credit_type])}門課程')
            print(f"-" * 100)
            for i, (course, course_dict) in enumerate(self.sort_historical_courses[credit_type], start = 1):
                print(f"{i}. {course}:")
                print(f"\t課程代碼: {course_dict['課程代碼']}")
                print(f"\t學分數: {course_dict['學分數']}學分")
                print(f"\t期程: {course_dict['期程']}")
                print(f"\t性質: {course_dict['課程性質']}")
                print(f"\t修畢學期: {course_dict['修習時間']}")
                print(f"\t分數: {course_dict['分數']}")
                print(f"\t必修/核心/選修: {course_dict['課程所屬學程性質']}")
                print(f"\t四大類類別: {course_dict['四大類類別']}")
                print(f"\t審查備註: {course_dict.get('審查備註', '無')}")
            print(f"-" * 100)
            print()
    
    def write_sorted_historical_courses(self):
        with open('./Generated/歷年修課.txt', 'w', encoding='utf-8') as file:
            file.write(f'共修習{len(self.historical_course_list)}門課程\n')
            file.write(f"{'-' * 100}\n")
            for credit_type in self.order:
                file.write(f'{credit_type}: {len(self.sort_historical_courses[credit_type])}門課程\n')
                file.write(f"{'-' * 100}\n")
                
                for i, (course, course_dict) in enumerate(self.sort_historical_courses[credit_type], start=1):
                    file.write(f"{i}. {course}:\n")
                    file.write(f"\t課程代碼: {course_dict['課程代碼']}\n")
                    file.write(f"\t學分數: {course_dict['學分數']}學分\n")
                    file.write(f"\t期程: {course_dict['期程']}\n")
                    file.write(f"\t性質: {course_dict['課程性質']}\n")
                    file.write(f"\t修畢學期: {course_dict['修習時間']}\n")
                    file.write(f"\t分數: {course_dict['分數']}\n")
                    file.write(f"\t必修/核心/選修: {course_dict['課程所屬學程性質']}\n")
                    file.write(f"\t四大類類別: {course_dict['四大類類別']}\n")
                    file.write(f"\t審查備註: {course_dict.get('審查備註', '無')}\n")
                
                file.write(f"{'-' * 100}\n\n")