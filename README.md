# CYCU-EECS-Automatic-Courses-Status-Checker
- 目前功能：
    - 到[CYCU Myself](https://myself.cycu.edu.tw/)爬取選課系統資料與歷年修課(JSON)
    - 到[修課須知&應修科目表](https://bseecs.cycu.edu.tw/%e5%ad%b8%e7%94%9f%e5%ad%b8%e7%bf%92/%e6%87%89%e4%bf%ae%e7%a7%91%e7%9b%ae%e8%a1%a8%e5%8f%8a%e4%bf%ae%e8%aa%b2%e9%a0%88%e7%9f%a5/)下載課程地圖、注意事項與應修科目表(PDF)
    - 到[學程課程規範](https://bseecs.cycu.edu.tw/%e5%ad%b8%e7%94%9f%e5%ad%b8%e7%bf%92/%e5%ad%b8%e7%a8%8b%e8%aa%b2%e7%a8%8b%e8%a6%8f%e5%8a%83/)下載學程表(EXCEL)
    - 將應修科目表透過OCR轉換成每頁對應的文本與表格(JSON):
        - Json最外圈是list
        - 每個index對應每頁應修科目表的頁碼-1，如第一頁的index是0
        - 每頁的結構都是
            ```Json
            {
                "text": 每頁的文本<class 'str'>,
                "table": 每頁含有的表格<class 'list'>
            }
            ```
        - ```table```是2D list

- TODO:
    - 處理檔案已存在要不要覆蓋的問題
    - 完成```parse_basic_course_table.py```
        - ```table_manual()```: 手動設定
        - ```table_chatgpt()```: 透過ChatGPT API KEY讓ChatGPT整理出固定格式的規則
        - 是否需要Ollama？
    - 完成```generate_status_table.py```：
        - 根據歷屆修課與畢業規則產生修課狀態Excel表
    - 完成```generate_future_course_table.py```:
        - 根據選課系統的修課清單（與追蹤清單？）等產生預排課表
    - 抓線上表單選課作業（optional）
    - 打包成可執行檔發行Release (Windows / macOS / Linux)

- 檔案架構：
```
.
├──.env（自動產生）
├──.gitignore
├──LICENSE
├──README.md
├──requirements.txt
├──main.py
├──get_student_data.py
├──get_files.py
├──parse_basic_course_table.py
├──generate_status_table.py
├──generate_future_course_table.py
├──Basic_Course_Tables_and_Rules（自動產生）
│ └──OCR_Tables_and_Rules_{入學年度}.json
├──CYCU-Myself（自動產生）
│ ├──歷年修課.json
│ ├──選課系統_追蹤清單.json
│ ├──選課系統_基本資料.json
│ └──選課系統_總覽.json
│──PDF（自動產生）
│ ├──電資學士班應修科目表課程地圖.pdf
│ ├──電機資訊學院學士班修課注意事項.pdf
│ └──{根據你的學號(入學年度)下載的對應}應修科目表.pdf
│ └──選課系統_總覽.json
└──Program（自動產生）
  ├──工業系-中原大學工業與系統工程學系學程規畫表.xlsx
  ├──通訊學程-中原大學電子與電機工程學系共同規畫通訊學程.xlsx
  ├──資工系-中原大學資訊工程學系學程規畫表-{當前的版本}.xlsx
  ├──電子系-中原大學電子工程學系學程規畫表.xlsx
  └──電機系-中原大學電機工程學系學程規畫表.xlsx
```

- 安裝指令：
```pip install -r requirements.txt```

- ```選課系統_總覽.json```的欄位（整理中）：
    - 登記清單 register_get
    - 修課清單 take_course_get
    - st_info
    - CacheData
    - distinct_IP_IDCODE_alert
    - 學程 cross_type_get
    - 課程類別 op_type_get
    - 學系 department_get
    - 選課選項 selects
    - 課程類別(必/選) op_stdy_type_get
    - 目前選課階段-詳細 marqueeStr
    - 公告欄-系統操作說明 ann_type_get
    - 選課系統是否開放 sys_open
    - 介紹 explanations
    - 介面語言 lang
    - is_auth_ok
    - cacheKey_course_get
    - 目前選課階段 announcement
    - 目前選課階段-標題 announcement_td
    - buttons
    - general_op_type_get
    - 追蹤清單 track_get
    - dataFrom
    - dept_div
    - labels
    - make_up_get
    - alerts
    - sys_control_get
    - dept_bln_get
    - col_checkbox