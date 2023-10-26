import csv

with open('/Users/bo.li/Downloads/purchase_target_10000.tsv', 'r') as file:
    reader = csv.DictReader(file, delimiter='\t')
    for row in reader:
        print(row)  # 输出字典，其中键是标题行中的列名，值是相应的数据值
        

