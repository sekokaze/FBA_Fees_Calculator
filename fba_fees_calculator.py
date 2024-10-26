import math
from pathlib import *

# 导入函数工具
import fun_tools



# 判断属于哪个类型
def define_product_size(product_dict,country,product_type,size_span):
    country_weight_unit = size_span[country]["Weight_Unit"]
    country_size_unit = size_span[country]["Size_Unit"]

    length = fun_tools.convert_unit(product_dict['length'],product_dict['size_unit'],country_size_unit)
    width = fun_tools.convert_unit(product_dict['width'],product_dict['size_unit'],country_size_unit)
    height = fun_tools.convert_unit(product_dict['height'],product_dict['size_unit'],country_size_unit)
    weight = fun_tools.convert_unit(product_dict['weight'],product_dict['weight_unit'],country_weight_unit)
    
    size_list = [length,width,height]
    size_list.sort(reverse=True)
    size_list.append(weight)
    lng = float('%.2f' % ((size_list[1]+size_list[2])*2+size_list[0]))
    size_list.append(lng)
    # 比较现有产品与标准的差别确定属于哪个分段
    product_size_list = size_span[country]["Product_Size_List"]
    for product_size in product_size_list:
        # print(product_size)
        if product_type not in list(size_span[country].keys()):
            product_type = "Normal"
        size_index_dict = size_span[country][product_type][product_size]
        size_index_list = [size_index_dict['L-side'],size_index_dict['M-side'],size_index_dict['S-side'],size_index_dict['weight'],size_index_dict['L+G']]
        
        size_sign = fun_tools.compare_list(size_list,size_index_list)
        if size_sign == "THIS":
            actual_product_size = product_size
            break
        elif size_sign == "NEXT":
            continue
    
    product_t_dict = {}
    product_t_dict['size_type'] = actual_product_size
    product_t_dict['length'] = length
    product_t_dict['width'] = width
    product_t_dict['height'] = height
    product_t_dict['size_unit'] = country_size_unit
    product_t_dict['weight'] = weight
    product_t_dict['weight_unit'] = country_weight_unit
    
    return product_t_dict


# 根据分段来计算对应的费用
def cal_delivery_fee(product_dict,country,product_type,size_span,delivery_dict):
    size_type = product_dict['size_type']
    # print(size_type)
    # size_type_re = re.compile(r'_Oversize')
    # size_type_result = size_type_re.search(size_type)
    if size_type in size_span[country]["Minimum_Volume"]:
        if product_dict['width'] < 2:
            product_dict['width'] = 2
        if product_dict['height'] < 2:
            product_dict['height'] = 2

    volume_weight = float('%.2f' % ((product_dict['length'] * product_dict['width'] * product_dict['height'])/size_span[country]["volume_weight"]))
    product_dict['volume_weight'] = volume_weight
    if size_type in size_span[country]["Judge_Actural_Weight"]:
        actual_weight = product_dict['weight']
    else:
        if volume_weight <= product_dict['weight']:
            actual_weight = product_dict['weight']
        else:
            actual_weight = volume_weight
    product_dict['actual_weight'] = actual_weight

    # 计算实际运费
    # 获取对应的运费分段
    delivery_dict_act = delivery_dict[country][product_type][size_type]

    delivery_fee = fun_tools.get_delivery_fee(delivery_dict_act,actual_weight)
    # print(delivery_fee)
    # 判断是否是字典，计算字典内的运费
    if isinstance(delivery_fee,dict):
        delivery_fee_act = float('%.2f' % (delivery_fee["base"]+delivery_fee["plus"]*math.ceil((actual_weight-delivery_fee["fpound"])/delivery_fee["plus_measure"])))
    else:
        delivery_fee_act = delivery_fee
    product_dict["delivery_fee"] = delivery_fee_act
    # print(delivery_fee_act)
    
    return product_dict








# 计算仓储费
def cal_storage_fee(product_dict,country,product_type,size_span,storage_dict):
    product_volume = float('%.4f' % ((product_dict['length'] * product_dict['width'] * product_dict['height'])/size_span[country]["Volume_Size"]))
    product_size_type = product_dict['size_type']
    # oversize_type_re = re.compile(r'_Oversize')
    # # storage_dict = {}
    
    # re_size = oversize_type_re.search(product_size_type)
    if product_size_type in size_span[country]["Standard_Size"]:
        size_type = 'Standard_Size'
    else:
        size_type = 'Oversize'

    if product_type not in list(storage_dict[country].keys()):
        product_type = "Normal"

    fee_dict = storage_dict[country][product_type][size_type]

    normal_storage_fee = float('%.4f' % (fee_dict["9"]*product_volume))
    high_storage_fee = float('%.4f' % (fee_dict["12"]*product_volume))
    
    product_dict['product_volume'] = product_volume
    product_dict['volume_unit'] = size_span[country]["Volume_Unit"]
    product_dict['1-9_Storage_Fee'] = normal_storage_fee
    product_dict['10-12_Storage_Fee'] = high_storage_fee
    
    return product_dict


def main_calculator():
    pass








if __name__ == "__main__":
    pass