import json
from pathlib import *
import glob

# def get_dict_from_json(file_path):
#     with open(file_path, 'r',encoding='utf-8') as json_file:
#         dict_file = json.load(json_file)
#         return dict_file


def get_dict_from_json(directory, prefix, year):
    # 创建Path对象指向目录
    directory_path = Path(directory)
    # print(directory_path)
    # 构造期望的文件名模式
    file_pattern = f"{prefix}-{year}.json"
    # print(file_pattern)
    # 在目录中搜索匹配的文件
    matching_files = list(directory_path.glob(file_pattern))
    
    # 可以根据需要处理找到的文件
    if not matching_files:
        print(f"没有找到匹配的文件：{file_pattern}")
        return None
    
    # 如果存在多个匹配的文件，您需要决定如何处理它们
    # 这个例子中只读取找到的第一个文件
    file_path = matching_files[0]
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data





# 转换尺寸
def convert_unit(num,bunit,aunit):
    if bunit.upper() == aunit.upper():
        return float('%.2f' % (float(num)))

    if bunit.upper() == 'CM' and aunit.upper() == 'INCH':
        new_num = float('%.2f' % (float(num)/2.54))
    elif bunit.upper() == 'INCH' and aunit.upper() == 'CM':
        new_num = float('%.2f' % (float(num)*2.54))
    elif bunit.upper() == 'KG' and aunit.upper() == 'LB':
        new_num = float('%.2f' % (float(num)*2.2046226))
    elif bunit.upper() == 'LB' and aunit.upper() == 'KG':
        new_num = float('%.2f' % (float(num)/2.2046226))
    elif bunit.upper() == 'ON' and aunit.upper() == 'LB':
        new_num = float('%.2f' % (float(num)/16))        

    return new_num


# 比较两个运费列表大小
def compare_list(test_list,compare_list):
    count = 0
    na_count = 0
    for a, b in zip(test_list, compare_list):
        if b == "NA":
            na_count +=1
            continue
        else:
            if a > b:
                return "NEXT"
            else:
                count +=1
    total_count = count + na_count
    if total_count == 5:
        return "THIS"


# 确定运费和包裹区间
def get_delivery_fee(delivery_fee_dict,actual_weight):
    for pound,fee in delivery_fee_dict.items():
        if pound == "base":
            delivery_fee = delivery_fee_dict
            return delivery_fee
        #先判断在哪个计费区间
        else:
            pound_index = float(pound)

            if actual_weight > pound_index:
                continue
            else:
                delivery_fee = fee
                return delivery_fee