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
target_file_path = 'D:\\WorkProject\\Pharmolix\\uniprot_with_hgnc_1130.json'
#target_file_path = '/share-vepfs/zhangjh-data/uniprot_with_hgnc_1130.json'

with open(target_file_path, 'r') as file:
    data = json.load(file)
    target_count = 0
    uid_count = 0
    insert_count_table1 = 0
    insert_count_table2 = 0

    for uniprot_id, properties in data.items():
        names = properties['Name'] #需要注意：Name节点是一个list
        symbol_hgnc = properties['symbol_hgnc'] #需要注意：symbol_hgnc节点是一个list
        all_names = names + symbol_hgnc
        entry_name = properties['Entry_Name']
        sequence = properties['Sequence']
        if len(sequence) > 2048:
            print(f"WARN: target {names} / with uniprot id: {uniprot_id} has sequence greater than 2048: {len(sequence)}")
        uid_count += 1
        for name in all_names:
            if name and entry_name and sequence:
                target_count += 1
                # 打印一下中间结果
                if target_count % 10000 == 0:
                    print(f"processed {target_count} target items...")
                # result = mysqlhelper.insertone(
                #     "insert into chatdd_target_protein_hgnc (name, entry_name, uniprot_id) values(%s, %s, %s)",
                #     (name, entry_name, uniprot_id))

                if True:
                    insert_count_table1 +=1
                    if insert_count_table1 % 1000 == 0:
                        print(f"insert_count_table1 inserted {insert_count_table1} items...")

        # result = mysqlhelper.insertone(
        #     "insert into chatdd_target_sequence_hgnc (uniprot_id,sequence) values(%s, %s)",
        #     (uniprot_id,sequence[:2048]))
        if True:
            insert_count_table2 += 1
            if insert_count_table2 % 1000 == 0:
                print(f"insert_count_table2 inserted {insert_count_table2} items...")

print(f"total inserted target/protein count: {insert_count_table1}; total target items in file: {target_count}")
print(f"total inserted target/protein count: {insert_count_table2}; total target items in file: {uid_count}")

