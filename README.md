MySQL CSV Data Inserter

這個 Python 腳本用於從 CSV 檔案讀取數據，並定期將隨機選取的一行數據插入到 MySQL 資料庫中。

目錄

安裝需求

使用方式

程式邏輯

設定檔案說明

錯誤排除

安裝需求

請確保已安裝 Python 以及必要的套件。

pip install pymysql

使用方式

設定資料庫連線資訊

修改 host、port、user、password、database、table_name 變數，確保它們符合你的 MySQL 環境。

提供 CSV 檔案

修改 csv_file_path，將其設為你的 CSV 檔案路徑。

執行腳本

直接執行 Python 腳本：

python data_test.py

中斷程序

若要停止插入數據，請按下 Ctrl + C 來終止程序。

程式邏輯

連接 MySQL 資料庫，確保表格存在。

讀取 CSV 檔案，檢查欄位是否符合表格。

每隔 interval_seconds 秒，隨機選擇一行數據並插入 MySQL。

持續運行，直到手動停止。

設定檔案說明

請確保你的 MySQL 表格結構與 CSV 欄位一致。

MySQL 表格結構 (可參考 ensure_table_exists 方法)

CSV 欄位名稱必須匹配：

ts,L2C3W10W_WWTS_PH_1102_PV,L2C3W10W_WWTS_PH_1103_PV,...
2024-02-18 12:00:00,7.1,6.9,...

錯誤排除

1. 連接 MySQL 失敗

確保 MySQL 服務運行中。

檢查 host、port、user、password 是否正確。

2. CSV 欄位與資料庫不匹配

確保 CSV 檔案中的欄位名稱與資料庫表格名稱一致。

可在 read_csv_data 方法中加入 print(row.keys()) 來檢查讀取的欄位名稱。

3. 插入數據時發生錯誤

檢查是否有非數字值，或缺失數據。

可在 insert_random_data_from_csv 方法中加入 print(selected_row) 來查看插入的數據。