# 定义两个数组
array1 = [1, 2, 3, 4, 5]
array2 = [4, 5, 6, 7, 8]

# 将数组转换为集合
set1 = set(array1)
set2 = set(array2)

# 找出两个集合的交集
intersection = set1 & set2

# 将交集转换为一个dict，其中每个元素的值都被设为1，不在交集中的元素值设为0
result_dict = {item: 1 if item in intersection else 0 for item in array1 + array2}

# 输出结果字典
print(result_dict)