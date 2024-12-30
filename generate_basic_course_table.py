# -*- coding: utf-8 -*-
import os
import json
import openpyxl

class DuplicateProgramError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

def generate_table(path, enroll_year):
    # set basic types of graduate credits
    graduate_credits = {
        '基本知能': 6,
        '通識基礎必修': 14,
        '學系必修': 66,
        '學系選修': 14,
        '通識延伸選修':12,
        '自由選修': 14,
        '其他選修': 0
    }
    if enroll_year == '108':
        graduate_credits['學系選修'] = 16
        graduate_credits['通識延伸選修'] = 14
        graduate_credits['自由選修'] = 12
    elif enroll_year == '109':
        graduate_credits['通識延伸選修'] = 14
    json_dict = { '畢業應修最低學分數': graduate_credits }
    
    # set courses and properties of each basic type of graduate credit
    for key in graduate_credits:
        temp_dict = {}
        if key == '基本知能':
            temp_dict = {
                '英文(一)': {
                    '期程': '半',
                    '學分數': 1,
                    '修習時間': f'{enroll_year}1 / 大一上'
                },
                '英文(二)': {
                    '期程': '半',
                    '學分數': 1,
                    '修習時間': f'{enroll_year}2 / 大一下'
                },
                '實用英文(一)': {
                    '期程': '半',
                    '學分數': 1,
                    '修習時間': f'{int(enroll_year)+1}1 / 大二上' # not sure
                },
                '實用英文(二)': {
                    '期程': '半',
                    '學分數': 1,
                    '修習時間': f'{int(enroll_year)+1}2 / 大二下' # not sure
                },
                '英語聽講(一)': {
                    '期程': '半',
                    '學分數': 1,
                    '修習時間': f'{enroll_year}1 / 大一上'
                },
                '英語聽講(二)': {
                    '期程': '半',
                    '學分數': 1,
                    '修習時間': f'{enroll_year}2 / 大一下'
                },
                '體育一': {
                    '期程': '半',
                    '學分數': 1,
                    '修習時間': f'{enroll_year}1 / 大一上'
                },
                '體育興趣一': {
                    '期程': '半',
                    '學分數': 0,
                    '修習時間': None
                },
                '體育興趣二': {
                    '期程': '半',
                    '學分數': 0,
                    '修習時間': None
                },
                '體育興趣三': {
                    '期程': '半',
                    '學分數': 0,
                    '修習時間': None
                }
            }
        elif key == '通識基礎必修':
            temp_dict = {
                '天': {
                    '宗教哲學': {
                        '期程': '半',
                        '學分數': 2,
                        '修習時間': None,
                        '性質': '宗哲'
                    },
                    '人生哲學': {
                        '期程': '半',
                        '學分數': 2,
                        '修習時間': None,
                        '性質': '人哲'
                    }
                },
                '人': {
                    '台灣政治與民主': {
                        '期程': '半',
                        '學分數': 2,
                        '修習時間': None,
                        '性質': '公民'
                    },
                    '法律與現代生活': {
                        '期程': '半',
                        '學分數': 2,
                        '修習時間': None,
                        '性質': '公民'
                    },
                    '當代人權議題與挑戰': {
                        '期程': '半',
                        '學分數': 2,
                        '修習時間': None,
                        '性質': '公民'
                    },
                    '生活社會學': {
                        '期程': '半',
                        '學分數': 2,
                        '修習時間': None,
                        '性質': '公民'
                    },
                    '全球化大議題': {
                        '期程': '半',
                        '學分數': 2,
                        '修習時間': None,
                        '性質': '公民'
                    },
                    '經濟學的世界': {
                        '期程': '半',
                        '學分數': 2,
                        '修習時間': None,
                        '性質': '公民'
                    },
                    '區域文明史': {
                        '期程': '半',
                        '學分數': 2,
                        '修習時間': None,
                        '性質': '歷史'
                    },
                    '文化思想史': {
                        '期程': '半',
                        '學分數': 2,
                        '修習時間': None,
                        '性質': '歷史'
                    }
                },
                '物': {
                    '運算思維與程式設計': {
                        '期程': '半',
                        '學分數': 2,
                        '修習時間': f'{enroll_year}1 / 大一上',
                    },
                    '自然科學與人工智慧導論': {
                        '期程': '半',
                        '學分數': 2,
                        '修習時間': f'{enroll_year}2 / 大一下',
                    }
                },
                '我': {
                    '文學經典閱讀': {
                        '期程': '半',
                        '學分數': 2,
                        '修習時間': f'{enroll_year}1 / 大一上',
                    },
                    '語文與修辭': {
                        '期程': '半',
                        '學分數': 2,
                        '修習時間': f'{enroll_year}2 / 大一下',
                    }
                }
            }
        elif key == '學系必修':
            temp_dict = {
                '微積分(上)': {
                    '期程': '半',
                    '學分數': 3,
                    '修習時間': f'{enroll_year}1 / 大一上',
                    '擋修科目': None,
                    '續修條件': None
                },
                '微積分(下)': {
                    '期程': '半',
                    '學分數': 3,
                    '修習時間': f'{enroll_year}2 / 大一下',
                    '擋修科目': '微積分(上)',
                    '續修條件': '曾修'
                },
                '普通物理(一)': {
                    '期程': '半',
                    '學分數': 3,
                    '修習時間': f'{enroll_year}1 / 大一上',
                    '擋修科目': None,
                    '續修條件': None
                },
                '普通物理(二)': {
                    '期程': '半',
                    '學分數': 3,
                    '修習時間': f'{enroll_year}2 / 大一下',
                    '擋修科目': '普通物理(一)',
                    '續修條件': '曾修'
                },
                '普通物理實驗(一)': {
                    '期程': '半',
                    '學分數': 1,
                    '修習時間': f'{enroll_year}1 / 大一上', # may be postponed
                    '擋修科目': None,
                    '續修條件': None
                },
                '普通物理實驗(二)': {
                    '期程': '半',
                    '學分數': 1,
                    '修習時間': f'{enroll_year}2 / 大一下', # may be postponed
                    '擋修科目': None,
                    '續修條件': None
                },
                '計算機概論(一)': {
                    '期程': '半',
                    '學分數': 3,
                    '修習時間': f'{enroll_year}1 / 大一上',
                    '擋修科目': None,
                    '續修條件': None
                },
                '計算機概論(二)': {
                    '期程': '半',
                    '學分數': 3,
                    '修習時間': f'{enroll_year}2 / 大一下',
                    '擋修科目': '計算機概論(一)',
                    '續修條件': '曾修'
                },
                '線性代數': {
                    '期程': '半',
                    '學分數': 3,
                    '修習時間': f'{enroll_year}1 / 大一上',
                    '擋修科目': None,
                    '續修條件': None
                },
                '機率與統計': {
                    '期程': '半',
                    '學分數': 3,
                    '修習時間': f'{int(enroll_year)+1}2 / 大二上',
                    '擋修科目': None,
                    '續修條件': None
                },
                '電子學(一)': {
                    '期程': '半',
                    '學分數': 3,
                    '修習時間': f'{int(enroll_year)+1}1 / 大二上',
                    '擋修科目': None,
                    '續修條件': None
                },
                '電子實驗(一)': {
                    '期程': '半',
                    '學分數': 1,
                    '修習時間': f'{int(enroll_year)+1}2 / 大二下', # not sure
                    '擋修科目': None,
                    '續修條件': None
                },
                '電路學(一)': {
                    '期程': '半',
                    '學分數': 3,
                    '修習時間': f'{int(enroll_year)+1}1 / 大二上',
                    '擋修科目': None,
                    '續修條件': None
                },
                '電路實驗(一):': {
                    '期程': '半',
                    '學分數': 1,
                    '修習時間': f'{int(enroll_year)+1}1 / 大二上', # not sure
                    '擋修科目': None,
                    '續修條件': None
                },
                '專題製作(一)': {
                    '期程': '半',
                    '學分數': 1,
                    '修習時間': f'{int(enroll_year)+2}2 / 大三下',
                    '擋修科目': None,
                    '續修條件': None
                },
                '專題製作(二)': {
                    '期程': '半',
                    '學分數': 1,
                    '修習時間': f'{int(enroll_year)+3}1 / 大四上',
                    '擋修科目': None,
                    '續修條件': None
                }
            }
        elif key == '學系選修':
            programs = {
                '生產管理學程': {
                    '所屬學系': '工業與系統工程學系',
                    '必修': None,
                    '核心': None,
                    '選修': None
                },
                '品質管理學程': {
                    '所屬學系': '工業與系統工程學系',
                    '必修': None,
                    '核心': None,
                    '選修': None
                },
                '經營管理學程': {
                    '所屬學系': '工業與系統工程學系',
                    '必修': None,
                    '核心': None,
                    '選修': None
                },
                '半導體學程': {
                    '所屬學系': '電子工程學系',
                    '必修': None,
                    '核心': None,
                    '選修': None
                },
                '電路設計學程': {
                    '所屬學系': '電子工程學系',
                    '必修': None,
                    '核心': None,
                    '選修': None
                },
                '電力學程': {
                    '所屬學系': '電機工程學系',
                    '必修': None,
                    '核心': None,
                    '選修': None
                },
                '控制學程': {
                    '所屬學系': '電機工程學系',
                    '必修': None,
                    '核心': None,
                    '選修': None
                },
                '通訊學程': {
                    '所屬學系': ['電子工程學系', '電機工程學系'],
                    '必修': None,
                    '核心': None,
                    '選修': None
                },
                '資訊硬體學程': {
                    '所屬學系': '資訊工程學系',
                    '必修': None,
                    '核心': None,
                    '選修': None
                },
                '資訊軟體學程': {
                    '所屬學系': '資訊工程學系',
                    '必修': None,
                    '核心': None,
                    '選修': None
                },
                '資訊應用學程': {
                    '所屬學系': '資訊工程學系',
                    '必修': None,
                    '核心': None,
                    '選修': None
                }
            }
            print(' 本系共有以下學程:')
            mapping = {}
            for idx, program in enumerate(programs):
                print(f'  {idx+1}. {program} - 所屬學系: {programs[program]["所屬學系"]}')
                mapping[str(idx+1)] = program
            cache = []
            for program in ['主修學程一', '主修學程二', '副修學程']:
                while True:
                    try:
                        p = mapping[input(f'> 請輸入{program}的編號 (如\"1\"表示生產管理學程): ')]
                        if p in cache:
                            raise DuplicateProgramError('  學程重複，請重新輸入。')
                        else:
                            temp_dict[program] = p
                            temp_dict[f'{program}所屬學系'] = programs[p]['所屬學系']
                            cache.append(p)
                        break
                    except DuplicateProgramError as e:
                        print(e)
                    except KeyError:
                        print('  無此編號，請重新輸入。')
        elif key == '通識延伸選修':
            temp_dict = {
                '天': { '最低應修學分數': 2 },
                '人': {
                    '最低應修學分數': 2,
                    '電資學院指定必修課程': '工程倫理'
                },
                '物': { '最低應修學分數': 2 },
                '我': { '最低應修學分數': 2 }
            }
        elif key == '自由選修': 
            temp_dict = {
                '最多認列學分數': {
                    '輔系': None,
                    '雙主修': None,
                    '跨領域學分學程': None,
                    '就業學程': None,
                    '微型學程（他系）': None,
                    'PBL課程': None,
                    '磨課師(MOCCs)微學分學程': 6,
                    '專業自主學習學分': 2
                }
            }
        json_dict[key] = temp_dict
    
    # set english ability
    json_dict['英文畢業門檻']: {
        '測驗': {
            '全民英檢 GEPT': '中級初試',
            '多益測驗 TOEIC': 550,
            '托福 TOEFL - 紙筆型態 ITP': 450,
            '托福 TOEFL - 網路型態 IBT': 47,
            '雅思測驗 IELTS': 4.0,
            '劍橋大學英語能力認證分級測驗 (Cambridge Main Suite)': 'Preliminary English Test (PET)',
            '劍橋大學國際商務英語能力測驗 (BULATS)': 'ALTE Level 2'
        },
        '全英語專業課程': {
            '最低修習課程數': 2,
            '不認列的課程': ['英文(一)', '英文(二)', '英語聽講(一)', '英語聽講(二)', '實用英文(一)',\
                '實用英文(二)', '商學院商業英語會話(一)', '商學院商業英語會話(二)', '英語檢定技巧']
        }
    }

    # program rules
    json_dict['學程規定']: {
        '學程性質': {
            '主修學程必修': {
                '科目重複或不足之替代學程性質': ['其它主修學程核心', '副修學程不同必修', '副修學程不同核心'],
                '科目重複或不足替代後畢業學分仍不足之替代學程性質': ['電資學院各系專業課程']
            },
            '主修學程核心': {
                '科目重複或不足之替代學程性質': ['其它主修學程核心', '副修學程不同必修', '副修學程不同核心'],
                '科目重複或不足替代後畢業學分仍不足之替代學程性質': ['電資學院各系專業課程'],
                '科目多修抵免學分認列學程性質': ['同一學程選修']
            },
            '主修學程選修': {
                '科目重複之替代學程性質': ['副修學程不同必修', '副修學程不同選修', '副修學程核心']
            },
            '副修學程必修': {},
            '副修學程核心': {
                '科目多修抵免學分認列學程性質': ['同一學程選修']
            },
            '副修學程選修': {}
        }
    }
    json_dict['電資學院跨領域學分學程最低得修習之本院開設專業課程學分數']: 3
    json_dict['國外或香港澳門地區']: {
        '畢業年級相當國內高中二年級之同級同類學校畢業生': {
            '規定之修業年限內最少應增加之應修畢業學分數': 12
        },
        '進入大學前學歷相當國內高中二年級之同級同校學生': {
            '應修課程之學分（不列入大學畢業學分）': {
                '通識課程學分數': 6,
                '基礎理工數學': 6
            }
        }
    }

    with open(f'{path}/{enroll_year}_基本畢業條件.json', 'w', encoding = 'utf-8') as f:
        f.write(json.dumps(json_dict, indent = 4, ensure_ascii = False))

# TODO: read xlsx files from './Program' and generate corresponding 必修/核心/選修 into json file
def get_program_info(path, enroll_year):
    # load json
    json_dict = json.load(open(f'{path}/{enroll_year}_基本畢業條件.json', 'r', encoding = 'utf-8'))
    print(json_dict['學系選修'])
    # read xlsx
    program_dirs = os.listdir('./Program')
    for program_dir in program_dirs:
        pass

    # write json
    pass

def generate_basic_course_table(enroll_year):
    path = './Generated'
    os.makedirs(path, exist_ok = True)
    # manual setting
    print('> 正在產生修課規定:')
    generate_table(path, enroll_year)
    get_program_info(path, enroll_year)

generate_basic_course_table('110')