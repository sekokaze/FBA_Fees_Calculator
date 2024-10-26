import main_calculator as mc

# 打印输出
def print_actural_data():
    data = mc.main_calculate_gui("",type="manual_input")
    storage_fee_dict = data[1]
    original_product_dict = data[0]
    
    print(storage_fee_dict)

    print(f'''
    尺寸：{storage_fee_dict['length']}x{storage_fee_dict['width']}x{storage_fee_dict['height']} inches, 
    {original_product_dict['length']}x{original_product_dict['width']}x{original_product_dict['height']} cm
    重量：{storage_fee_dict['weight']} {storage_fee_dict['weight_unit']},{original_product_dict['weight']} kg
    体积重：{storage_fee_dict['volumn_weight']} {storage_fee_dict['weight_unit']}
    计费重量：{storage_fee_dict['actual_weight']} {storage_fee_dict['weight_unit']}
    体积：{storage_fee_dict['product_volume']} {storage_fee_dict['volume_unit']}
    属于{storage_fee_dict['size_type']}
    亚马逊派送费：${storage_fee_dict['delivery_fee']}
    1-9月仓储费：${storage_fee_dict['1-9_Storage_Fee']}
    10-12月仓储费：${storage_fee_dict['10-12_Storage_Fee']}''')