import json
# import pymysql
from db.mysqlhelper import MySqLHelper
import common.logger

# 读取蛋白质json文件 uniprot_accession.json ，将其插入到数据库表 chatdd_target_protein_info
# ...


# 读取药物json文件 drug_syn_smiles.json ，将其插入到数据库表 chatdd_drug_molecule_info
with open('F:\\work\\data\\drug_syn_smiles.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

    count = 0;

    if isinstance(data, dict):
        for key2, value in data.items():
            if (value['smiles'] != []) :
                # print(value['smiles'])
                smiles = value['smiles']
                mysqlhelper = MySqLHelper()
                for name in value['synonyms'] :
                    result = mysqlhelper.insertone(
                        "insert into chatdd_drug_molecule_info(name, smiles) values( % s,  % s)",
                        (name, smiles))
                    # print("result====", result)
                    count += 1
                    print("count:", count)
