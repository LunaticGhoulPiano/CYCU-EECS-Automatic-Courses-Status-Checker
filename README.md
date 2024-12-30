# CYCU-EECS-Automatic-Courses-Status-Checker

## 身為電資學院的學生，你應該不至於不會跑Python吧？我就不提供執行檔了。
## 修課規則是以電機資訊學院學士班官網最新的資料設定的，請以你自身入學時下載的硬修科目表與學程表為準。

### 目前功能：
- 到[CYCU Myself](https://myself.cycu.edu.tw/)爬取選課系統資料與歷年修課至```CYCU-Myself```資料夾
- 到[修課須知&應修科目表](https://bseecs.cycu.edu.tw/%e5%ad%b8%e7%94%9f%e5%ad%b8%e7%bf%92/%e6%87%89%e4%bf%ae%e7%a7%91%e7%9b%ae%e8%a1%a8%e5%8f%8a%e4%bf%ae%e8%aa%b2%e9%a0%88%e7%9f%a5/)下載課程地圖、注意事項與應修科目表至```PDF```資料夾
- 到[學程課程規範](https://bseecs.cycu.edu.tw/%e5%ad%b8%e7%94%9f%e5%ad%b8%e7%bf%92/%e5%ad%b8%e7%a8%8b%e8%aa%b2%e7%a8%8b%e8%a6%8f%e5%8a%83/)下載學程表至```Program```資料夾
- 根據入學年度（以是否有在[官網提供的應修科目表](https://bseecs.cycu.edu.tw/%e5%ad%b8%e7%94%9f%e5%ad%b8%e7%bf%92/%e6%87%89%e4%bf%ae%e7%a7%91%e7%9b%ae%e8%a1%a8%e5%8f%8a%e4%bf%ae%e8%aa%b2%e9%a0%88%e7%9f%a5/)中為準）自動產生畢業條件到```Generated```資料夾

### TODO:
- 處理檔案已存在要不要覆蓋的問題（應該只有```./Generated```中的檔案要考慮）
- 完成```generate_basic_course_table.get_program_info()```，將各學程的必修/核心/選修寫入```./Generated/{入學年度}_基本畢業條件.json```
- 完成```generate_status_table.py```：
    - 根據歷屆修課與畢業規則產生修課狀態Excel表
- 完成```generate_future_course_table.py```:
    - 根據選課系統的修課清單（與追蹤清單？）等產生預排課表
- 抓線上表單選課作業（optional）
- 打包成可執行檔發行Release (Windows / macOS / Linux)

### 檔案架構：
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
├──generate_basic_course_table.py
├──generate_status_table.py
├──generate_future_course_table.py
├──CYCU-Myself（自動產生）
│ ├──歷年修課.json
│ ├──選課系統_追蹤清單.json
│ ├──選課系統_基本資料.json
│ └──選課系統_總覽.json
├──Generated（自動產生）
│ └──{入學年度}_基本畢業條件.json
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

### 其它
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