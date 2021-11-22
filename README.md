# Industry_Academy_Rebuild(重建筆記- 讓自己重新學習 以及 警惕自己不再重蹈覆轍)
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
# 常用指令
  建立migration資料檔   
    python manage.py makemigrations (+ 資料夾檔案 --> 指定migration)  
  資料庫同步  
    python manage.py migrate (+ 資料夾檔案--> 指定同步)  

# 採雷小記
  RateLimitMixin 在 Django3.0 已經無法使用，要考慮其他登入安全措施  
