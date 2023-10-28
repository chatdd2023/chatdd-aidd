'''
正式环境执行：
python -m aidd.json_data_init_drug --env=prod
测试环境执行：
python -m aidd.json_data_init_drug --env=dev
'''
import json
from aidd.db.mysqlhelper import MySqLHelper

# 读取药物json文件 drug_syn_smiles.json ，将其插入到数据库表 chatdd_drug_molecule_info
mysqlhelper = MySqLHelper()
drug_file_path = '/Users/tielei/Documents/project/pharmolix/aidd_data_processing/drug_syn_smiles_part.json'
with open(drug_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    count = 0
    for drug_name, properties in data.items():
        if (properties['smiles'] != []) :
            smiles = properties['smiles']
            name_set = set(synonym for synonym in properties['synonyms'])
            name_set.add(drug_name)
            count += len(name_set)
            for name in name_set:
                result = mysqlhelper.insertone(
                    "insert into chatdd_drug_molecule_info (name, smiles) values(%s, %s)",
                    (name, smiles))

print(f"total inserted drug count: {count}")
