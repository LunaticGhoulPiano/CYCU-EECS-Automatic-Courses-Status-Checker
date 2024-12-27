# -*- coding: utf-8 -*-
import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from fake_useragent import UserAgent

BASIC_COURSE_TABLE_URL = 'https://bseecs.cycu.edu.tw/%e5%ad%b8%e7%94%9f%e5%ad%b8%e7%bf%92/%e6%87%89%e4%bf%ae%e7%a7%91%e7%9b%ae%e8%a1%a8%e5%8f%8a%e4%bf%ae%e8%aa%b2%e9%a0%88%e7%9f%a5/'
PROGRAM_URL = 'https://bseecs.cycu.edu.tw/%e5%ad%b8%e7%94%9f%e5%ad%b8%e7%bf%92/%e5%ad%b8%e7%a8%8b%e8%aa%b2%e7%a8%8b%e8%a6%8f%e5%8a%83/'

def download(enroll_year):
    # get basic course table html
    try:
        response = requests.get(BASIC_COURSE_TABLE_URL, headers = {'User-Agent': UserAgent().random, 'Connection': 'keep-alive'})
        response.raise_for_status() # ensure response is 200
    except requests.exceptions.RequestException as e:
        print('> 網頁獲取失敗：')
        print(e)
        return
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # find pdf links
    links = soup.find_all('a', href = True)
    links = [link for link in links if link['href'].endswith('.pdf')]
    if not links:
        print('> 查無應修科目表等相關檔案！')
        return
    links = [urljoin(BASIC_COURSE_TABLE_URL, link['href']) for link in links if link['href'].endswith('.pdf')]
    file_names = [urlparse(link).path.split('/')[-1] for link in links]
    mapping = {file_name: link for file_name, link in zip(file_names, links) 
               if ('修課注意事項' in file_name or '課程地圖' in file_name or enroll_year in file_name)}
    
    # check enroll year
    if not [file_name for file_name in file_names if enroll_year in file_name]:
        print('> 查無對應入學年度之應修科目表！')
        return

    # download pdfs
    dir_name = './PDF'
    os.makedirs(dir_name, exist_ok = True)
    print('> 正在下載應修科目表等相關檔案...')
    for file_name, link in mapping.items():
        try:
            #time.sleep(0.3) # anti-anti-spidering
            response = requests.get(link, headers = {'User-Agent': UserAgent().random, 'Connection': 'keep-alive'})
            response.raise_for_status() # ensure response is 200
        except requests.exceptions.RequestException as e:
            print(f'> {file_name}下載失敗：{e}')
            return
        with open(f'{dir_name}/{file_name}', 'wb') as f:
            f.write(response.content)

    # get program html
    try:
        response = requests.get(PROGRAM_URL, headers = {'User-Agent': UserAgent().random, 'Connection': 'keep-alive'})
        response.raise_for_status() # ensure response is 200
    except requests.exceptions.RequestException as e:
        print('> 網頁獲取失敗：')
        print(e)
        return
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href = True)
    links = [link for link in links if link['href'].endswith('.xlsx')]
    if not links:
        print('> 查無相關學程表！')
        return
    links = [urljoin(PROGRAM_URL, link['href']) for link in links if link['href'].endswith('.xlsx')]
    file_names = [urlparse(link).path.split('/')[-1] for link in links]
    mapping = {file_name: link for file_name, link in zip(file_names, links)}

    # download EXCELs
    dir_name = './Program'
    os.makedirs(dir_name, exist_ok = True)
    print('> 正在下載學程表...')
    for file_name, link in mapping.items():
        try:
            #time.sleep(0.3) # anti-anti-spidering
            response = requests.get(link, headers = {'User-Agent': UserAgent().random, 'Connection': 'keep-alive'})
            response.raise_for_status() # ensure response is 200
        except requests.exceptions.RequestException as e:
            print(f'> {file_name}下載失敗：{e}')
            return
        with open(f'{dir_name}/{file_name}', 'wb') as f:
            f.write(response.content)

def get_files(enroll_year):
    download(enroll_year)