import json
from aidd.db.redishelper import RedisHelper

# 读取药物json文件 drug_syn_smiles.json ，将其插入到数据库表 chatdd_drug_molecule_info
redishelper = RedisHelper()
drug_file_path = 'result_120.json'
with open(drug_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    count = 0
    for name, affinity_value in data.items():
        redishelper.set(name,affinity_value)
        count +=1
        print(count)

print(f"total inserted drug count: {count}")