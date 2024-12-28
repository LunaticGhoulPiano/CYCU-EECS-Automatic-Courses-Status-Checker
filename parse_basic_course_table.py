# -*- coding: utf-8 -*-
import os
import json
import requests
import pdfplumber
from dotenv import load_dotenv, set_key

ENV_PATH = '.env'

def table_ocr(path, file_name, enroll_year):
    json_dict = []
    with pdfplumber.open(file_name) as pdf:
        for page in pdf.pages:
            temp_dict = {
                'text': page.extract_text(),
                'table': page.extract_table()
            }
            json_dict.append(temp_dict)
    with open(f'{path}/OCR_Tables_and_Rules_{enroll_year}.json', 'w', encoding = 'utf-8') as f:
        f.write(json.dumps(json_dict, indent = 4, ensure_ascii = False))

# TODO: set the rules manually
def table_manual(path, file_name, enroll_year):
    pass

# TODO: get ChatGPT token and send the rules to ChatGPT
def table_TaiwanLLM(path, file_name, enroll_year):
    api_key = os.getenv('TAIWAN_LLM_API_KEY')
    if not api_key:
        api_key = input('請輸入Taiwan LLM API Key: ')
        set_key(ENV_PATH, 'TAIWAN_LLM_API_KEY', api_key)

def parse_basic_course_table(enroll_year):
    if os.path.exists('./PDF'):
        file_names = os.listdir('./PDF')
        if not file_names:
            print('> 查無PDF檔案!')
            return
        file_name = [file_name for file_name in file_names if enroll_year in file_name]
        if not file_name:
            print('> 查無對應入學年度之應修科目表！')
            return
        else:
            path = './Basic_Course_Tables_and_Rules'
            os.makedirs(path, exist_ok = True)
            # OCR
            print(f'> 正在轉換\"{file_name[0]}\"...')
            table_ocr(path, f'./PDF/{file_name[0]}', enroll_year)
            # ChatGPT
            if input('> 是否要用Taiwan LLM整理自動設定修課規則(Y/N)？ ') == 'Y':
                table_TaiwanLLM(path, f'./PDF/{file_name[0]}', enroll_year)
            # manual setting
            if input('> 是否要手動設定修課規則(Y/N)? ') == 'Y':
                table_manual(path, f'./PDF/{file_name[0]}', enroll_year)
    else:
        print('> 查無\"PDF\"資料夾！')
        return