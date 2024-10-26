import pandas as pd
import os
from pathlib import * 

import input_data
import fba_fees_calculator
import output_result
import fun_tools



this_dir = Path(__file__).resolve().parent
json_path = this_dir / "json_file"



product_size_dict_key = ["weight","L-side","M-side","S-side","L+G"]
product_type_dict = {"NOR":'Normal','NOR-LOW':'Normal-Low','CLO':'Cloth','CLO-LOW':'Cloth-Low','HAD':'Hazard','HAD-LOW':'Hazard-Low',
                    'PEK':'Peak_Season','MTC':'Multi-Channel'}


# 主运行函数
def main_calculate_gui(product_dict,type="dict"):
    if type=="dict":
        original_product_dict = product_dict
    else:
        original_product_dict = input_data.get_dimension()

    # print(original_product_dict)
    country = original_product_dict['country'].upper()

    year = original_product_dict['year']

    # 读取产品尺寸分段json
    size_span = fun_tools.get_dict_from_json(json_path, 'size_span', year)

    # # 读取派送费文件
    delivery_dict = fun_tools.get_dict_from_json(json_path, 'delivery_fee', year)

    # # 读取FBA仓储费文件
    storage_dict = fun_tools.get_dict_from_json(json_path, 'storage_fee', year)

    # print(size_span)

    product_type = product_type_dict[original_product_dict['product_type'].upper()]
    
    target_product_dict = fba_fees_calculator.define_product_size(original_product_dict,country,product_type,size_span)

    target_product_dict_final = fba_fees_calculator.cal_delivery_fee(target_product_dict,country,product_type,size_span,delivery_dict)

    storage_fee_dict = fba_fees_calculator.cal_storage_fee(target_product_dict_final,country,product_type,size_span,storage_dict)

    data_list = [original_product_dict,storage_fee_dict]
    
    return data_list
    



# 使用TK批量导入
def main_calculate_gui_bulk(filepath):
    product_df = pd.read_excel(filepath)
    product_df.rename(columns={"产品名称":"name","产品长度":"length","产品宽度":"width","产品高度":"height",
                               "尺寸单位(cm/inch)":"size_unit","重量":"weight","重量单位(kg/lb)":"weight_unit","国家":"country","年份(2023/2024)":"year",
                               "计算模式(nor/clo/had/sal/pek/mtc)":"product_type"},inplace=True)
    # 将列名设置为字典的键
    product_df.columns = product_df.columns.str.replace(' ', '')
    dicts = product_df.to_dict(orient='records')
    for product in dicts:
        # print(product)
    # 计算运费
        fees = main_calculate_gui(product)
        original_product_dict = fees[0]
        storage_fee_dict = fees[1]
        # 把新增的列加入字典
        product['目标商城尺寸'] = f"{storage_fee_dict['length']}x{storage_fee_dict['width']}x{storage_fee_dict['height']} {storage_fee_dict['size_unit']}"
        product['目标商城重量'] = f"{storage_fee_dict['weight']} {storage_fee_dict['weight_unit']}"
        product['目标商城体积重'] = f"{storage_fee_dict['volume_weight']} {storage_fee_dict['weight_unit']}"
        product['目标商城计费重'] = f"{storage_fee_dict['actual_weight']} {storage_fee_dict['weight_unit']}"
        product['目标商城体积'] = f"{storage_fee_dict['product_volume']} {storage_fee_dict['volume_unit']}"
        product['目标商城商品尺寸'] = f"{storage_fee_dict['size_type']}"
        product['FBA派送费'] = f"{storage_fee_dict['delivery_fee']}"
        product['1-9月仓储费'] = f"{storage_fee_dict['1-9_Storage_Fee']}"
        product['10-12月仓储费'] = f"{storage_fee_dict['10-12_Storage_Fee']}"


    df = pd.DataFrame(dicts)
    # 保存为EXCEL
    if os.path.exists(filepath):
        with pd.ExcelWriter(filepath,mode='a',engine='openpyxl',if_sheet_exists='overlay') as writer:
            df.to_excel(writer, sheet_name='calculated',index=False)
    else:
        with pd.ExcelWriter(filepath) as writer:
            df.to_excel(writer, sheet_name='calculated',index=False)

    print(f"已输出EXCEL")


if __name__ == "__main__":
    main_calculate_gui(0,type="input")
