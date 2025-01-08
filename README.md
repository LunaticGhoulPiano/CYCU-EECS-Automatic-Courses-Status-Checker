# CYCU-EECS-Automatic-Courses-Status-Checker

## 目前功能：
- 到[CYCU Myself](https://myself.cycu.edu.tw/)爬取選課系統資料與歷年修課至```CYCU-Myself```資料夾
- 到[修課須知&應修科目表](https://bseecs.cycu.edu.tw/%e5%ad%b8%e7%94%9f%e5%ad%b8%e7%bf%92/%e6%87%89%e4%bf%ae%e7%a7%91%e7%9b%ae%e8%a1%a8%e5%8f%8a%e4%bf%ae%e8%aa%b2%e9%a0%88%e7%9f%a5/)下載課程地圖、注意事項與應修科目表至```PDF```資料夾
- 到[學程課程規範](https://bseecs.cycu.edu.tw/%e5%ad%b8%e7%94%9f%e5%ad%b8%e7%bf%92/%e5%ad%b8%e7%a8%8b%e8%aa%b2%e7%a8%8b%e8%a6%8f%e5%8a%83/)下載學程表至```Program```資料夾
- 根據入學年度（以是否有在[官網提供的應修科目表](https://bseecs.cycu.edu.tw/%e5%ad%b8%e7%94%9f%e5%ad%b8%e7%bf%92/%e6%87%89%e4%bf%ae%e7%a7%91%e7%9b%ae%e8%a1%a8%e5%8f%8a%e4%bf%ae%e8%aa%b2%e9%a0%88%e7%9f%a5/)中為準）自動產生畢業條件到```./Generated/{入學年度}_基本畢業條件.json```
- 根據以上資料自動產生電資學院四大系十一大學程之詳細資料到```./Generated/各學程之必修_核心_選修總表.json```
- 到[MyMentor](https://cmap.cycu.edu.tw:8443/MyMentor/index.do)自動爬取```檢視自我學習狀況-歷年修課清單一覽表```到```./Generated/歷年修課與狀態表.html```

## TODOs:
- 處理檔案已存在要不要覆蓋的問題（應該只有```./Generated```中的檔案要考慮）
- 完成```generate_info.py```，根據```student_info.py```產生修課狀態表（及預排課表）
- 抓線上表單選課作業（optional）
- 使用pyinstaller打包成可執行檔發行Release (Windows / macOS / Linux)
- 找同學/學弟妹測試系統

## 檔案架構：
```
.CYCU-EECS-Automatic-Courses-Status-Checker
├──.env（自動產生）
├──.gitignore
├──LICENSE
├──README.md
├──requirements.txt
├──main.py
├──get_student_data.py
├──get_files.py
├──generate_basic_course_table.py
├──generate_info.py
├──student_info.py
├──CYCU-Myself（自動產生）
│ ├──歷年修課.json
│ ├──選課系統_基本資料.json
│ ├──選課系統_總覽.json
│ └──歷年修課與狀態表.html
├──Generated（自動產生）
│ ├──{入學年度}_基本畢業條件.json
│ └──各學程之必修_核心_選修總表.json
│──PDF（自動產生）
│ ├──電資學士班應修科目表課程地圖.pdf
│ ├──電機資訊學院學士班修課注意事項.pdf
│ └──{根據你的學號(入學年度)下載的對應}應修科目表.pdf
└──Program（自動產生）
  ├──工業系-中原大學工業與系統工程學系學程規畫表.xlsx
  ├──通訊學程-中原大學電子與電機工程學系共同規畫通訊學程.xlsx
  ├──資工系-中原大學資訊工程學系學程規畫表-{當前的版本}.xlsx
  ├──電子系-中原大學電子工程學系學程規畫表.xlsx
  └──電機系-中原大學電機工程學系學程規畫表.xlsx
```

## 執行
- Python：
    1. git clone到你的電腦：
        ```
        git clone https://github.com/LunaticGhoulPiano/CYCU-EECS-Automatic-Courses-Status-Checker.git
        ```
    2. 安裝所需libraries：
        - Windows:
            ```
            python -m pip install -r requirements.txt
            ```
        - macOS / Linux:
            ```
            python3 -m pip install -r requirements.txt
            ```
    3. 安裝```playwright```所需瀏覽器（本次使用Chromium）：
        - Windows:
            ```
            python -m playwright install
            ```
        - macOS / Linux:
            ```
            python3 -m playwright install
            ```
    4. 執行：
        - Windows:
            ```
            python main.py
            ```
        - macOS / Linux:
            ```
            python3 main.py
            ```

## 備註
- ```> 正在取得MyMentor資料...```會跑比較久，因為要透過Playwright模擬與瀏覽器的交互行為
- $${\color{red}修課規則是以電機資訊學院學士班官網最新的資料設定的，請以你自身入學時下載的應修科目表與學程表為準。}$$