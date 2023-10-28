'''
正式环境执行：
python -m aidd.json_data_init_pro --env=prod
测试环境执行：
python -m aidd.json_data_init_pro --env=dev
'''
import json
from aidd.db.mysqlhelper import MySqLHelper


# 读取蛋白质json文件 uniprot_accession.json ，将其插入到数据库表 chatdd_target_protein_info
mysqlhelper = MySqLHelper()
# target_file_path = '/Users/tielei/Documents/project/pharmolix/aidd_data_processing/uniprot_accession_part.json'
target_file_path = '/root/tielei/code/chatdd-aidd/files/uniprot_accession.json'
with open(target_file_path, 'r') as file:
    data = json.load(file)
    target_count = 0
    insert_count = 0

    for uniprot_id, properties in data.items():
        names = properties['Name'] #需要注意：Name节点是一个list
        entry_name = properties['Entry_Name']
        sequence = properties['Sequence']
        if len(sequence) > 2048:
            print(f"WARN: target {names} / with uniprot id: {uniprot_id} has sequence greater than 2048: {len(sequence)}")

        for name in names:
            if name and entry_name and sequence:
                target_count += 1
                # 打印一下中间结果
                if target_count % 10000 == 0:
                    print(f"processed {target_count} target items...")
                result = mysqlhelper.insertone(
                    "insert into chatdd_target_protein_info (name, entry_name, sequence) values(%s, %s, %s)",
                    (name, entry_name, sequence[:2048]))
                if result:
                    insert_count +=1

print(f"total inserted target/protein count: {insert_count}; total target items in file: {target_count}")

