import json
# import pymysql
from db.mysqlhelper import MySqLHelper
import common.logger

# 读取蛋白质json文件 uniprot_accession.json ，将其插入到数据库表 chatdd_target_protein_info
# ...


# 读取药物json文件 drug_syn_smiles.json ，将其插入到数据库表 chatdd_drug_molecule_info
with open('F:\\work\\data\\drug_syn_smiles.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    # 如果数据是一个列表，可以这样迭代
    # if isinstance(data, list):
    #     for item in data:
    #         print(item)
    #         # 如果你想进一步迭代每个元素中的数据，可以在这里添加代码

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
                    print("result====", result)
                    count += 1
                    print("count:", count)
            # print(f"{key}: {value}")
            #
            # for key2, value2 in value2.items():
            #     if (key2 == 'name'):  # [' ']
            #         # tmp = {value}
            #         print(f"{value2}")
            #         val_name2 = value2
            #     if (key2 == 'Entry_Name'):  #
            #         print(f"{value}")
            #         val_entry_name = {value}
            #     if (key == 'Sequence'):  #
            #         print(f"{value}")
            #         val_sequence = {value}




