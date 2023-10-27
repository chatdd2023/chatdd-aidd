import json
# import pymysql
from db.mysqlhelper import MySqLHelper
import common.logger


# 读取蛋白质json文件 uniprot_accession.json ，将其插入到数据库表 chatdd_target_protein_info
with open('F:\\work\\data\\data_dev\\uniprot_accession.json', 'r') as file:
    data = json.load(file)



    # 如果数据是一个字典，可以这样迭代

    count = 0;
    
    if isinstance(data, dict):
        for key, value in data.items():
            #print(f"{key}: {value}")
            for key,value in value.items():
                if (key == 'Name'):         # [' ']
                    # tmp = {value}
                    print(f"{value}")
                    val_name = value
                if (key == 'Entry_Name'):   # 
                    print(f"{value}")
                    val_entry_name = {value}
                if (key == 'Sequence'):     # 
                    print(f"{value}")
                    val_sequence = {value}
                    

                    mysqlhelper=MySqLHelper()
                    if val_name and val_entry_name and val_sequence :
                        result = mysqlhelper.insertone(
                            "insert into chatdd_target_protein_info(name, entry_name, sequence) values( % s, % s, % s)",
                            (val_name, val_entry_name, val_sequence))
                        # print("result====",result)
                        count += 1
                        print("count:", count)



# 读取药物json文件 drug_syn_smiles.json ，将其插入到数据库表 chatdd_drug_molecule_info
with open('F:\\work\\data\\drug_syn_smiles.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

    # 如果数据是一个字典，可以这样迭代

    count = 0;

    if isinstance(data, dict):
        for key2, value in data.items():
            if (value['smiles'] != []) :
                print(value['smiles'])
                smiles = value['smiles']
                mysqlhelper = MySqLHelper()
                for name in value['synonyms'] :
                    result = mysqlhelper.insertone(
                        "insert into chatdd_drug_molecule_info(name, smiles) values( % s,  % s)",
                        (name, smiles))
                    # print("result====", result)
                    count += 1
                    print("count:", count)






