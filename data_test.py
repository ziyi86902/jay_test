# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:04:47 2025

@author: user
"""

import pymysql
import csv
import time
import random

def ensure_table_exists(connection, table_name):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        ts DATETIME,
        L2C3W10W_WWTS_PH_1102_PV FLOAT,
        L2C3W10W_WWTS_PH_1103_PV FLOAT,
        L2C3W10W_WWTS_PH_1015_PV FLOAT,
        L2C3W10W_WWTS_FIQ_1015_PV FLOAT,
        L2C3W10W_WWTS_PH_1101_PV FLOAT,
        L2C3W10W_WWTS_FIQ_1101_PV FLOAT,
        L2C3W10W_WWTS_PH_1004_PV FLOAT,
        L2C3W10W_WWTS_FIQ_1001_PV FLOAT,
        L2C3WB1W_WWTS_FIQ_1006_PV FLOAT,
        L2_BRWW_PH_525B_PV FLOAT,
        L2_BRWW_FIQ_525_PV FLOAT,
        L2C3W10W_WWTS_FIQ_1102B_PV FLOAT,
        L2C3W10W_WWTS_FIQ_1102A_PV FLOAT
    );
    """
    with connection.cursor() as cursor:
        cursor.execute(create_table_query)
        connection.commit()
        print(f"表 {table_name} 確保存在！")

def read_csv_data(file_path):
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    
    # 移除 DateTime 欄位
    for row in data:
        if 'DateTime' in row:
            del row['DateTime']
    
    return data


def insert_random_data_from_csv(host, port, user, password, database, table_name, csv_file_path, interval_seconds):
    try:
        # 建立資料庫連接
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        print("連接成功！")
        
        # 確保表存在
        ensure_table_exists(connection, table_name)
        
        # 讀取 CSV 數據
        csv_data = read_csv_data(csv_file_path)
        if not csv_data:
            print("CSV 檔案無數據，請檢查檔案內容！")
            return
        
        print(f"已從 CSV 讀取 {len(csv_data)} 行數據。")

        # 初始化 ID 值
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT MAX(ID) FROM {table_name}")
            result = cursor.fetchone()
            current_id = result[0] + 1 if result and result[0] is not None else 1

        print(f"起始 ID 為：{current_id}")
        
        while True:
            # 隨機選取一列數據
            selected_row = random.choice(csv_data)
            
            # 創建新字典，將 ID 和 ts 放在最前面
            ordered_row = {
                'ID': current_id,
                'ts': time.strftime('%Y-%m-%d %H:%M:%S'),
                **selected_row  # 保留原有的資料
            }
            
            # 插入資料
            with connection.cursor() as cursor:
                query = f"""
                INSERT INTO {table_name} (ID, ts, F2_FBC_FIQ_03_PV, F2_FBC_HF_21_PV, F2_FBC_pHIT_21_PV, F2_FBC_pHIT_21B_PV,
                                          F2_FBC_HF_22B_PV, F2_FBC_FIQ_25B_PV, F2_FBC_HF_23_PV, F2_FBC_ORP_21_PV,
                                          F2_FBC_FIQ_08_PV, F2_FBC_P_25B_INV_Hz_PV)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    ordered_row["ID"], ordered_row["ts"],
                    float(ordered_row["F2_FBC_FIQ_03_PV"]), float(ordered_row["F2_FBC_HF_21_PV"]),
                    float(ordered_row["F2_FBC_pHIT_21_PV"]), float(ordered_row["F2_FBC_pHIT_21B_PV"]),
                    float(ordered_row["F2_FBC_HF_22B_PV"]), float(ordered_row["F2_FBC_FIQ_25B_PV"]),
                    float(ordered_row["F2_FBC_HF_23_PV"]), float(ordered_row["F2_FBC_ORP_21_PV"]),
                    float(ordered_row["F2_FBC_FIQ_08_PV"]), float(ordered_row["F2_FBC_P_25B_INV_Hz_PV"])
                ))
                connection.commit()
                print(f"插入成功：{ordered_row}")
                
                current_id += 1

            time.sleep(interval_seconds)

    except pymysql.MySQLError as e:
        print(f"資料庫錯誤：{e}")
    except KeyboardInterrupt:
        print("\n進程已被中斷。")
    finally:
        if connection:
            connection.close()
            print("資料庫連接已關閉。")

# 使用範例
if __name__ == "__main__":
    host = "192.168.50.84"
    port = 3306
    user = "sa"
    password = "0000"
    database = "demo"
    table_name = "demo_PH_1102_pred"
    csv_file_path = "PH_1102.csv"  # 替換為你的 CSV 檔案路徑
    interval_seconds = 5

    insert_random_data_from_csv(host, port, user, password, database, table_name, csv_file_path, interval_seconds)