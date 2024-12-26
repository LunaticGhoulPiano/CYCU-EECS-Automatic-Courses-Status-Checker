# CYCU-EECS-Automatic-Courses-Status-Checker
- 目前功能：
    - 到CYCU Myself爬取選課系統資料與歷年修課

- TODO:
    - 根據歷屆修課產生修課狀態Excel表
    - 根據選課系統的修課清單產生預排課表
    - 抓線上表單選課作業（optional）

- 爬取到的檔案架構：
```
CYCU-Myself
|-歷年修課.json
|-選課系統_追蹤清單.json
|-選課系統_基本資料.json
|-選課系統_總覽.json
```

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