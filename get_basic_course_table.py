import os
import requests
import ocrmypdf
from bs4 import BeautifulSoup  

URL = 'https://bseecs.cycu.edu.tw/%e5%ad%b8%e7%94%9f%e5%ad%b8%e7%bf%92/%e6%87%89%e4%bf%ae%e7%a7%91%e7%9b%ae%e8%a1%a8%e5%8f%8a%e4%bf%ae%e8%aa%b2%e9%a0%88%e7%9f%a5/'

def download(enroll_year):
    pass

def get_basic_course_table(enroll_year):
    download(enroll_year)