# -*- coding: utf-8 -*-
import os
import ocrmypdf

# TODO: ocr pdf and store text
def pdf_ocr(file_name):
    pass

# TODO: get the graduate rules from the text of basic course table
def parse(enroll_year):
    pass

def parse_basic_course_table(enroll_year):
    if os.path.exists('./PDF'):
        file_names = os.listdir('./PDF')
        if not [file_name for file_name in file_names if enroll_year in file_name]:
            print('> 查無對應入學年度之應修科目表！')
            return
        if file_names:
            for file_name in file_names:
                print(f'> 正在轉換\"{file_name}\"...')
                pdf_ocr(file_name)
        else:
            print('> 查無PDF檔案！')
            return
    else:
        print('> 查無\"PDF\"資料夾！')
        return

    parse(enroll_year)