# CYCU-EECS-Automatic-Courses-Status-Checker

## 目前功能：
- 到[CYCU Myself](https://myself.cycu.edu.tw/)爬取選課系統資料與歷年修課至```CYCU-Myself```資料夾
- 到[修課須知&應修科目表](https://bseecs.cycu.edu.tw/%e5%ad%b8%e7%94%9f%e5%ad%b8%e7%bf%92/%e6%87%89%e4%bf%ae%e7%a7%91%e7%9b%ae%e8%a1%a8%e5%8f%8a%e4%bf%ae%e8%aa%b2%e9%a0%88%e7%9f%a5/)下載課程地圖、注意事項與應修科目表至```PDF```資料夾
- 到[學程課程規範](https://bseecs.cycu.edu.tw/%e5%ad%b8%e7%94%9f%e5%ad%b8%e7%bf%92/%e5%ad%b8%e7%a8%8b%e8%aa%b2%e7%a8%8b%e8%a6%8f%e5%8a%83/)下載學程表至```Program```資料夾
- 根據入學年度（以是否有在[官網提供的應修科目表](https://bseecs.cycu.edu.tw/%e5%ad%b8%e7%94%9f%e5%ad%b8%e7%bf%92/%e6%87%89%e4%bf%ae%e7%a7%91%e7%9b%ae%e8%a1%a8%e5%8f%8a%e4%bf%ae%e8%aa%b2%e9%a0%88%e7%9f%a5/)中為準）自動產生畢業條件到```./Generated/{入學年度}_基本畢業條件.json```
- 根據以上資料自動產生電資學院四大系十一大學程之詳細資料到```./Generated/各學程之必修_核心_選修總表.json```
- 到[MyMentor](https://cmap.cycu.edu.tw:8443/MyMentor/index.do)自動爬取```檢視自我學習狀況-歷年修課清單一覽表```到```./CYCU-MySelf/歷年修課與狀態表.html```

## TODOs:
1. 智慧分配自由選修
2. 判斷學系選修還沒修到的必修/核心/選修課
3. 將雙資工的對應所需四大類及數量寫入到總表.xlsx的worksheet0(generate_info.py: ```generate()```的```head.append()```處)
4. 按照選課系統已選上課程產生預排課表並寫入到總表.xlsx的worksheet 1
5. 將主修學程一、主修學程二、副修學程的必修/核心/選修寫入到總表.xlsx的worksheet 2 ~ 4
6. 使用pyinstaller打包成可執行檔發行Release (Windows / macOS / Linux)
7. 其它:
    - 搞清楚```student_info.parse()```中的以下問題：
        1. 解決工程數學(一)的問題：
            - 是否為學系必修（應修科目表沒寫，但大一下時系所自動排課）
            - 電子系、電機系與通訊學程的"學程選修-必修"
        2. 系統程式113入學前為：
            - 資訊硬體學程：核心
            - 資訊軟體學程：必修
            - 資訊應用學程：核心
        3. 輔系、雙主修的判斷
    - 處理檔案已存在要不要覆蓋的問題（應該只有```./Generated```中的檔案要考慮）
    - 抓線上表單選課作業（optional）
    - 找同學/學弟妹測試系統

## 檔案架構與說明：
```
.CYCU-EECS-Automatic-Courses-Status-Checker
├──.env（自動產生）   <-------------------------------------------------- 保存你的itouch帳號密碼
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
├──CYCU-Myself（自動產生）   <-------------------------------- CYCU-Myself + MyMentor的原始資料
│ ├──歷年修課.json
│ ├──選課系統_基本資料.json
│ ├──選課系統_總覽.json
│ └──歷年修課與狀態表.html   <-------------- 只有這個從MyMentor抓的，其餘都從CYCU_Myself爬取
├──Generated（自動產生）   <---------------------------------------------------------- 處理結果
│ ├──{入學年度}_基本畢業條件.json   <------ 將{入學年度}應修科目表.pdf轉換成json檔
│ ├──各學程之必修_核心_選修總表.json   <--- 將./Program中的所有學程規劃表整合成json檔
│ ├──歷年修課.json   <-------------------- 單純方便日後使用
│ ├──歷年修課.txt   <--------------------- 單純方便使用者直接看
│ └──總表.xlsx   <------------------------ 最重要的輸出檔案
│──PDF（自動產生）   <------------------------------------------------------------ 修課相關檔案
│ ├──電資學士班應修科目表課程地圖.pdf
│ ├──電機資訊學院學士班修課注意事項.pdf
│ └──{根據你的學號(入學年度)下載的對應}應修科目表.pdf
└──Program（自動產生）   <------------------------------------------- 四大系11個學程的學程規劃表
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
- 由於學程表的不工整性，只要系助理改動格式parser就會出錯(```generate_basic_course_table.py```)。
- 不保證絕對的正確性，請再自行確認過修課狀態表。
- 外系的使用者抓完MyMentor的資料後就可以停了，只有```./CYCU-Myself```內的資料對你們而言才是可用的。