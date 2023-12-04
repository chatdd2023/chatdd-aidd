'''
正式环境执行：
python -m aidd.json_data_init_patents --env=prod
测试环境执行：
python -m aidd.json_data_init_patents --env=dev
'''
import json
from aidd.db.mysqlhelper import MySqLHelper


mysqlhelper = MySqLHelper()
drug_file_path = 'D:\\WorkProject\\Pharmolix\\chatdd-agent\\agent\\core\\drug_syn_smiles_patents_1127.json'
with open(drug_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    insert_count = 0
    target_count = 0

    val_summary = "NULL"

    for drug_name, properties in data.items():
        try:
            if (properties['patents'] != []) :
                name_set = set(synonym for synonym in properties['synonyms'])
                name_set.add(drug_name)

                if isinstance(properties['patents'], list):
                    target_count = target_count + len(name_set) * len(properties['patents'])

                if isinstance(properties['patents'], dict):
                    target_count = target_count + len(name_set)

                val_IUPAC_NAME = properties['IUPAC_NAME']
                if val_IUPAC_NAME !=[]:
                    if isinstance(val_IUPAC_NAME, str):
                        pass

                    else :
                        print(val_IUPAC_NAME)
                        raise ValueError
                else :
                    val_IUPAC_NAME ='NULL'


                for name in name_set:
                    # patents可能是一个列表，代表有多个patents信息，列表中每个元素都为一个字典
                    if isinstance(properties['patents'], list):
                        for patents_properties in properties['patents']:
                            val_number = patents_properties['number']
                            val_country = patents_properties['country']
                            val_approved = patents_properties['approved']
                            val_expires = patents_properties['expires']
                            val_pediatric = patents_properties['pediatric-extension']

                            result = mysqlhelper.insertone(
                                "insert into pharmolix_data_drugs_patents (drug_generic_name, patent_number, country, approved_date, expires_date, pediatric_extension, summary, IUPAC_NAME) values(%s, %s, %s, %s, %s, %s, %s, %s)",
                                (name, val_number, val_country, val_approved, val_expires, val_pediatric, val_summary,val_IUPAC_NAME))
                            if result:
                                insert_count += 1
                            if insert_count % 1000 == 0:
                                print(f"inserted {insert_count} items...")

                    # patents为一个字典，代表只有一条patent信息
                    elif isinstance(properties['patents'], dict):
                        val_number = properties['patents']['number']
                        val_country = properties['patents']['country']
                        val_approved = properties['patents']['approved']
                        val_expires = properties['patents']['expires']
                        val_pediatric = properties['patents']['pediatric-extension']
                        result = mysqlhelper.insertone(
                            "insert into pharmolix_data_drugs_patents (drug_generic_name, patent_number, country, approved_date, expires_date, pediatric_extension, summary, IUPAC_NAME) values(%s, %s, %s, %s, %s, %s, %s, %s)",
                            (name, val_number, val_country, val_approved, val_expires, val_pediatric, val_summary,val_IUPAC_NAME))
                        if result:
                            insert_count += 1
                        if insert_count % 1000 == 0:
                            print(f"inserted {insert_count} items...")
        except Exception as e:
            print(properties)
            raise e


print(f"total target count: {target_count}")
print(f"total inserted count: {insert_count}")
