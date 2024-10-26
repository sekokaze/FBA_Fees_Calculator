import main_calculator as asr
import tkinter as tk
from tkinter import messagebox, filedialog

# 创建窗口
root = tk.Tk()
root.title('FBA Fee Calculator')

# 创建输入框和标签(产品名称)
name_frame = tk.LabelFrame(root, text='Product Name')
name_frame.pack()
name_entry = tk.Entry(name_frame)
name_entry.pack()

# 创建输入框和标签(产品尺寸)
length_frame = tk.LabelFrame(root, text='Length')
length_frame.pack()
length_entry = tk.Entry(length_frame)
length_entry.pack()

width_frame = tk.LabelFrame(root, text='Width')
width_frame.pack()
width_entry = tk.Entry(width_frame)
width_entry.pack()

height_frame = tk.LabelFrame(root, text='Height')
height_frame.pack()
height_entry = tk.Entry(height_frame)
height_entry.pack()

# 长度单位
size_unit_frame = tk.LabelFrame(root, text='Size Unit')
size_unit_frame.pack()

size_unit_var = tk.StringVar(size_unit_frame)
size_unit_var.set('cm')
size_unit_radio_cm = tk.Radiobutton(size_unit_frame, text='cm', variable=size_unit_var, value='cm')
size_unit_radio_inch = tk.Radiobutton(size_unit_frame, text='inch', variable=size_unit_var, value='inch')

# 使用 grid 方法将单选按钮放在同一行
size_unit_radio_cm.grid(row=1,column=0)
size_unit_radio_inch.grid(row=1,column=1)

# 重量
weight_frame = tk.LabelFrame(root, text='Weight')
weight_entry = tk.Entry(weight_frame)
weight_frame.pack()
weight_entry.pack()

# 重量单位
weight_unit_frame = tk.LabelFrame(root, text='Weight Unit')
weight_unit_frame.pack()

weight_unit_var = tk.StringVar(weight_unit_frame)
weight_unit_var.set('kg')
weight_unit_radio_kg = tk.Radiobutton(weight_unit_frame, text='kg', variable=weight_unit_var, value='kg')
weight_unit_radio_lb = tk.Radiobutton(weight_unit_frame, text='lb', variable=weight_unit_var, value='lb')

weight_unit_radio_kg.grid(row=1,column=0)
weight_unit_radio_lb.grid(row=1,column=1)


country_label = tk.Label(root, text='Country')
country_var = tk.StringVar(root)
country_list = ['US', 'CA']
country_optionmenu = tk.OptionMenu(root, country_var, *country_list)
country_label.pack()
country_optionmenu.pack()


year_label = tk.Label(root,text="Year")
year_var = tk.StringVar(root)
year_list = ['2023','2024']
year_optionmenu = tk.OptionMenu(root,year_var, *year_list)
year_label.pack()
year_optionmenu.pack()



product_type_label = tk.Label(root, text='Product Type')
product_type_var = tk.StringVar(root)
product_type_dict = {"Normal":"NOR","Normal-Low":"NOR-LOW","Cloth":"CLO","Cloth-Low":"CLO-LOW","Harzad":"HAD","Harzad-Low":"HAD-LOW",
                     "Small & Light":"SAL","Peak Season":"PEK",'Multi-Channel':'MTC'}
product_type_var_optionmenu = tk.OptionMenu(root, product_type_var, *product_type_dict.keys())
product_type_label.pack()
product_type_var_optionmenu.pack()



# 在 calculate() 函数外部创建 Text widget 和滚动条
result_box = tk.Text(root, height=10, width=70)
result_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(root, command=result_box.yview)
result_box.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)






# 定义计算按钮的点击事件
def calculate():
    product_condiction_dict = {
        'name': name_entry.get(),
        'length': length_entry.get(),
        'width': width_entry.get(),
        'height': height_entry.get(),
        'size_unit': size_unit_var.get(),
        'weight': weight_entry.get(),
        'weight_unit': weight_unit_var.get(),
        'country': country_var.get(),
        'year': year_var.get(),
        'product_type': product_type_dict[product_type_var.get()]
    }
    
    # ... Call your functions here ...
    data_list = asr.main_calculate_gui(product_condiction_dict)
    storage_fee_dict = data_list[1]
    original_product_dict = data_list[0]
    
    # 显示结果
    print(storage_fee_dict)
    print(original_product_dict)

    result_text = f'''
    正在计算的产品是：{original_product_dict['name']},国家是：{original_product_dict['country']},
    年份是{original_product_dict['year']}，模式是{original_product_dict['product_type']}
    尺寸：{storage_fee_dict['length']}x{storage_fee_dict['width']}x{storage_fee_dict['height']} inches, 
    {original_product_dict['length']}x{original_product_dict['width']}x{original_product_dict['height']} cm
    重量：{storage_fee_dict['weight']} {storage_fee_dict['weight_unit']},{original_product_dict['weight']} kg
    体积重：{storage_fee_dict['volume_weight']} {storage_fee_dict['weight_unit']}
    计费重量：{storage_fee_dict['actual_weight']} {storage_fee_dict['weight_unit']}
    体积：{storage_fee_dict['product_volume']} {storage_fee_dict['volume_unit']}
    属于{storage_fee_dict['size_type']}
    亚马逊派送费：${storage_fee_dict['delivery_fee']}
    1-9月仓储费：${storage_fee_dict['1-9_Storage_Fee']}
    10-12月仓储费：${storage_fee_dict['10-12_Storage_Fee']}
    '''

    # 可选：添加分隔符
    separator = "\n" + "-" * 50 + "\n"
    result_box.insert(tk.END, separator)

    # 将新的结果插入到 Text widget
    result_box.insert(tk.END, result_text)
    
    # 自动滚动到 Text widget 的底部以显示最新的结果
    result_box.see(tk.END)


    
    # messagebox.showinfo(title='FBA Fee', message=f'''
    # 尺寸：{storage_fee_dict['length']}x{storage_fee_dict['width']}x{storage_fee_dict['height']} inches, 
    # {original_product_dict['length']}x{original_product_dict['width']}x{original_product_dict['height']} cm
    # 重量：{storage_fee_dict['weight']} {storage_fee_dict['weight_unit']},{original_product_dict['weight']} kg
    # 体积重：{storage_fee_dict['volume_weight']} {storage_fee_dict['weight_unit']}
    # 计费重量：{storage_fee_dict['actual_weight']} {storage_fee_dict['weight_unit']}
    # 体积：{storage_fee_dict['product_volume']} {storage_fee_dict['volume_unit']}
    # 属于{storage_fee_dict['size_type']}
    # 亚马逊派送费：${storage_fee_dict['delivery_fee']}
    # 1-9月仓储费：${storage_fee_dict['1-9_Storage_Fee']}
    # 10-12月仓储费：${storage_fee_dict['10-12_Storage_Fee']}''')

# 创建计算按钮
calculate_button = tk.Button(root, text='Calculate', command=calculate)
calculate_button.pack()


# 添加文件对话框
def open_file():
    filepaths = filedialog.askopenfilenames()
    for filepath in filepaths:
        asr.main_calculate_gui_bulk(filepath)

# 创建上传按钮
open_file_button = tk.Button(root, text='Upload Files', command=open_file)
open_file_button.pack()




# 运行主循环
root.mainloop()