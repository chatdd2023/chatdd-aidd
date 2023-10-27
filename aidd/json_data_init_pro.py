import json
# import pymysql
from db.mysqlhelper import MySqLHelper
import common.logger


# 读取蛋白质json文件 uniprot_accession.json ，将其插入到数据库表 chatdd_target_protein_info
with open('F:\\work\\data\\uniprot_accession.json', 'r') as file:
    data = json.load(file)



    # 如果数据是一个字典，可以这样迭代

    count = 0;

    if isinstance(data, dict):
        for key, value in data.items():
            #print(f"{key}: {value}")
            for key2, value2 in value.items():
                if (key2 == 'Name'):         #
                    # print(f"{value}")
                    val_name = value2
                if (key2 == 'Entry_Name'):   #
                    # print(f"{value}")
                    val_entry_name = {value2}
                if (key2 == 'Sequence'):     #
                    # print(f"{value}")
                    val_sequence = {value2}



                    if val_name and val_entry_name and val_sequence :
                        mysqlhelper = MySqLHelper()
                        result = mysqlhelper.insertone(
                            "insert into chatdd_target_protein_info(name, entry_name, sequence) values( % s, % s, % s)",
                            (val_name, val_entry_name, val_sequence))
                        # print("result====",result)
                        count += 1
                        # print("count:", count)

    print("count:", count)

