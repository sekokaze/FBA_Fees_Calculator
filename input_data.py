# 输入产品的信息
def get_dimension():
    name = input("请输入产品名称：")
    length = input("请输入长度：")
    width = input("请出入宽度：")
    height = input("请输入高度：")
    size_unit = input("请输入尺寸单位(CM/INCH)：")
    weight = input("请输入重量：")
    weight_unit = input("请输入重量单位(KG/LB)：")
    country = input("请计算的国家：")
    year = input("请输入计算的年份：")
    product_type = input("请计算的模式(NOR/CLO/HAD/SAL)：")
    product_dict = {'name':name,'length':length,'width':width,'height':height,'size_unit':size_unit,'weight':weight,'weight_unit':weight_unit,
                    'country':country,'year':year,'product_type':product_type}
    return product_dict