# CYCU-EECS-Automatic-Courses-Status-Checker

## Demo video
https://youtu.be/SjwGFxUXUtc

## 目前功能：
- 到[CYCU Myself](https://myself.cycu.edu.tw/)爬取選課系統資料與歷年修課至```CYCU-Myself```資料夾
- 到[修課須知&應修科目表](https://bseecs.cycu.edu.tw/%e5%ad%b8%e7%94%9f%e5%ad%b8%e7%bf%92/%e6%87%89%e4%bf%ae%e7%a7%91%e7%9b%ae%e8%a1%a8%e5%8f%8a%e4%bf%ae%e8%aa%b2%e9%a0%88%e7%9f%a5/)下載課程地圖、注意事項與應修科目表至```PDF```資料夾
- 到[學程課程規範](https://bseecs.cycu.edu.tw/%e5%ad%b8%e7%94%9f%e5%ad%b8%e7%bf%92/%e5%ad%b8%e7%a8%8b%e8%aa%b2%e7%a8%8b%e8%a6%8f%e5%8a%83/)下載學程表至```Program```資料夾
- 根據入學年度（以是否有在[官網提供的應修科目表](https://bseecs.cycu.edu.tw/%e5%ad%b8%e7%94%9f%e5%ad%b8%e7%bf%92/%e6%87%89%e4%bf%ae%e7%a7%91%e7%9b%ae%e8%a1%a8%e5%8f%8a%e4%bf%ae%e8%aa%b2%e9%a0%88%e7%9f%a5/)中為準）自動產生畢業條件到```./Generated/{入學年度}_基本畢業條件.json```
- 根據以上資料自動產生電資學院四大系十一大學程之詳細資料到```./Generated/各學程之必修_核心_選修總表.json```
- 到[MyMentor](https://cmap.cycu.edu.tw:8443/MyMentor/index.do)自動爬取```檢視自我學習狀況-歷年修課清單一覽表```到```./CYCU-MySelf/歷年修課與狀態表.html```
- 產生```總表.xlsx```：
    - ```修課狀態表```:
        - 將修過的課程+正在修的課程+尚缺哪些課程繪製成一張大表
        - 目前未做：
            - 單資工學程的未完成課程
            - 非資工學程的未完成課程
            - 自由選修自動找可以用的課去補
    - ```預排課表```:
        - ```選課系統``` - ```修課清單```有資料才會產生此工作表
    - ```主副修學程規劃表```:
        - 將學程規劃表按照主修學程一、主修學程二與副修學程以更規整的格式呈現，避免了必須要同時開啟多個不同學系的學程規劃表再自行對照
        - 如果兩主修或副修有資工學程，會將認列的四大類寫在規劃表右側（同樣地不會寫入用不到的四大類）

## TODOs:
1. 智慧分配自由選修
2. 判斷單資工&非資工學程
4. 使用pyinstaller打包成可執行檔發行Release (Windows / macOS / Linux)
5. 其它:
    - 搞清楚```student_info.parse()```中的以下問題：
        - 輔系、雙主修的判斷
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
    1. 安裝好Python(本人使用3.11.7)
    2. git clone到你的電腦 or 點選```Code``` - ```Download ZIP```下載並解壓縮：
        ```
        git clone https://github.com/LunaticGhoulPiano/CYCU-EECS-Automatic-Courses-Status-Checker.git
        ```
    3. 安裝所需libraries：
        - Windows:
            ```
            python -m pip install -r requirements.txt
            ```
        - macOS / Linux:
            ```
            python3 -m pip install -r requirements.txt
            ```
    4. 安裝```playwright```所需瀏覽器（本次使用Chromium）：
        - Windows:
            ```
            python -m playwright install
            ```
        - macOS / Linux:
            ```
            python3 -m playwright install
            ```
    5. 執行：
        - Windows:
            ```
            python main.py
            ```
        - macOS / Linux:
            ```
            python3 main.py
            ```

## 資工選修四大類判斷
- 函數: ```student_info.py``` - ```set_unfinished_courses``` - ```elif credit_type == '學系選修'``` - ```elif not has_judged_four_type```，約第590行處
- 邏輯:
    - 總共跑5個stage
    - stage 0:
        - 只針對課程認列一種四大類的，當目前主修學程總學分 < 6且此課程對應的任一四大類屬於此學程的任一四大類就加入
            - ex. 目前正在判斷"資訊軟體學程"，此學程對應"網路與資訊安全"與"資訊系統(含資料庫)"
            - 而目前正在判斷的課程對應的四大類只有"網路與資訊安全"或"資訊系統(含資料庫)"任一才會被加入
            - 若目前正在判斷的課程對應的四大類有超過一種對應的四大類就會被跳過，因為只認列一種四大類的表示選擇較少，要優先
        - 並且當此stage出現課程對應的四大類不在兩個主修學程對應的任一四大類中就會跳過
            - 如主修"資訊軟體學程"+"資訊應用學程"，對應為"網路與資訊安全"+"資訊系統(含資料庫)"+"資訊科技應用"
            - 則當此門課程的四大類只有一個且不屬於這三種之一，表示完全不能用，加入"其它"
    - stage 1:
        - 當目前主修學程總學分 < 6且此課程對應的任一四大類屬於此學程的任一四大類就加入
    - stage 2:
        - 只針對課程認列一種四大類的，當兩主修學程學分總和 < 15且此課程對應的任一四大類屬於兩學程的任一四大類就加入
    - stage 3:
        - 當兩主修學程學分總和 < 15且此課程對應的任一四大類屬於兩學程的任一四大類就加入
    - stage 4:
        - 將剩餘的加入對應的主修學程/其它
- 可改善：
    - 優先選擇不可抵認自由選修的課程

## 非資工學程(TODO)
- 目前必修/核心的課程如果跨學程有相同課名不可兩邊互相抵認，要讓教授人工判斷
- 再按照修業辦法的規則抓其它課程去補

## 備註
- ```> 正在取得MyMentor資料...```會跑比較久，因為要透過Playwright模擬與瀏覽器的交互行為
- $${\color{red}修課規則是以電機資訊學院學士班官網最新的資料設定的，請以你自身入學時下載的應修科目表與學程表為準。}$$
- 由於學程表的不工整性，只要系助理改動格式parser就會出錯(```generate_basic_course_table.py```)。
- 不保證絕對的正確性，請再自行確認過修課狀態表。
- 外系的使用者抓完MyMentor的資料後就可以停了，只有```./CYCU-Myself```內的資料對你們而言才是可用的。