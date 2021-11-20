# Industry_Academy_Rebuild(重建筆記- 讓自己重新學習 以及 警惕自己不再重蹈覆轍)
  Day1 重新安裝環境、重建資料庫、Django由2.1升級成3.0
    資料庫選用->由 MySQL 改成 SQLite (非主從式架構(Client–server model)，而是被整合在使用者程式中。)

# 常用指令
  建立migration資料檔
    python manage.py makemigrations (+ 資料夾檔案 --> 指定migration)
  資料庫同步
    python manage.py migrate (+ 資料夾檔案--> 指定同步)

# 採雷小記
  RateLimitMixin 在 Django3.0 已經無法使用，要考慮其他登入安全措施
