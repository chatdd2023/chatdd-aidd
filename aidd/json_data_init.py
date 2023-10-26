import json

with open('/Users/bo.li/Downloads/uniprot_accession.json', 'r') as file:
    data = json.load(file)
    # 如果数据是一个列表，可以这样迭代
    if isinstance(data, list):
        for item in data:
            print(item)
            # 如果你想进一步迭代每个元素中的数据，可以在这里添加代码

    # 如果数据是一个字典，可以这样迭代
    elif isinstance(data, dict):
        for key, value in data.items():
            #print(f"{key}: {value}")
            for key,value in value.items():
                print(f"{key}:{value}")
