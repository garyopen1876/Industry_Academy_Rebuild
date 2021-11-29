# Industry_Academy_Rebuild(重建筆記- 讓自己重新學習 以及 警惕自己不再重蹈覆轍)
# 功能流程
  ![function_process](https://user-images.githubusercontent.com/32414355/143917515-f6798986-ac6b-4249-ab1c-c5ba6c9d7237.png)  
# 作品部分一覽
![homepage](https://user-images.githubusercontent.com/32414355/143916119-3c9540b9-3ee5-4752-9954-6daa7483aac5.png)  
▲首頁  
![post](https://user-images.githubusercontent.com/32414355/143917369-1c617ddd-9bf0-43a2-955f-5bb723ac05f9.png)  
▲公佈欄詳細訊息  
![login](https://user-images.githubusercontent.com/32414355/143917752-963887cd-65e0-4f3d-9bdb-4c6885582ca3.png)
▲登入系統  
![student](https://user-images.githubusercontent.com/32414355/143918371-3068f783-e256-48f7-a2ba-e1707f4383c9.png)  
▲學生相關功能  
![company](https://user-images.githubusercontent.com/32414355/143918401-07c5c6d1-4b86-4638-a3e0-ba35725b5c2e.png)  
▲企業相關功能  
![manager](https://user-images.githubusercontent.com/32414355/143918430-16551ce2-058e-4ba8-a0f8-29fb24b6d531.png)  
▲助教相關功能  
# 演算法流程  
![algorithm_process](https://user-images.githubusercontent.com/32414355/143915798-2328ffd4-781f-46b3-a9c0-827f5a9b72b8.png)  
# 重建日誌
  Day1 重新安裝環境、重建資料庫、Django由2.1升級成3.0  
    資料庫選用->由 MySQL 改成 SQLite (非主從式架構(Client–server model)，而是被整合在使用者程式中。)
  
  Day2 將舊有class一一上傳(依序)  
    company -- 公司相關功能  
    manager -- 管理者(學校助教)相關功能  
    tutor -- 企業以及學校導師相關功能  
    student -- 學生相關功能  
    inter_ship -- 實習報告相關功能(預計增設功能)    
    match -- 媒合系統與其相關功能  
    
  Day3 開始修復部分破損的舊功能與添加新功能  
   修復大部分html的urls錯誤的問題  
   將web的message_board model移至  
   company_information編輯無法寫入資料庫的問題  
   新增company_contact_person的相關功能  
   
  Day4 將部分功能修正為較合適的狀態  
  header 依照使用者的不同提供不同的功能(介面隔離)  
  homepage 頁面美化  
  media部分資料上傳(其實不應該上傳的，但為了方便紀錄製作的相關檔案)  
  match系統的部分修正  
  
  Day5 安全性更新  
  將media和setting資料上傳加入gitignore  
  將部分view網址進行修改並放入setting之中  
  
# 常用指令
  建立migration資料檔   
    python manage.py makemigrations (+ 資料夾檔案 --> 指定migration)  
  資料庫同步  
    python manage.py migrate (+ 資料夾檔案--> 指定同步)  

# 提醒小記
  RateLimitMixin 在 Django3.0 已經無法使用，要考慮其他登入安全措施  
