# from pywebio.platform.flask import webio_view
from pywebio import start_server,pin
# from flask import Flask
from pywebio.input import *
from pywebio.output import *
from pathlib import Path
import webbrowser
import time
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import json


import main_calculator as mc
import fun_tools

filepath = Path(__file__).parent


# 更新处理值
type_dict = {"一般产品":"NOR","一般产品-低价":"NOR-LOW","服装":"CLO","服装-低价":"CLO-LOW","危险品":"HAD","危险品-低价":"HAD-LOW",
             "旺季一般产品":"PEK","多渠道派送费-一般产品":"MTC"}

# 配置文件清理日志记录器
cleanup_logger = logging.getLogger('cleanup_logger')
cleanup_logger.setLevel(logging.INFO)
cleanup_handler = logging.FileHandler(filepath / 'asset_cleanup.log')
cleanup_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
cleanup_logger.addHandler(cleanup_handler)


history_results= []



def main():
    # 使用 PyWebIO 获取输入

    # 显示历史结果的区域，初始化为空
    with put_column():
        put_html('<b>计算结果:</b><div id="history"></div>').style('margin-bottom: 10px;')
        put_scrollable([], height=100, keep_bottom=True,scope='history')


    with put_column():

        while True:
            product_info = input_group("FBA_Fee_Calculator",[
            input("请输入产品名称",name='name',type=TEXT),
            input("请输入长度：",name='length',type=FLOAT),
            input("请出入宽度：",name='width',type=FLOAT),
            input("请输入高度：",name='height',type=FLOAT),
            select("请输入尺寸单位(CM/INCH)", options=['CM', 'INCH'],value='CM',name='size_unit'),
            input("请输入重量：",name='weight',type=FLOAT),
            select("请输入重量单位(KG/LB)", options=['KG', 'LB'],value='KG',name='weight_unit'),
            select("请计算的国家：", options=['US', 'CA'],value='US',name='country'),
            select("请输入计算的年份：", options=['2023', '2024'],value='2024',name='year'),
            select("请计算的模式", options=["一般产品","一般产品-低价","服装","服装-低价","危险品","危险品-低价","旺季一般产品","多渠道派送费-一般产品"],value='一般产品',name='product_type'),
            actions(name='actions', buttons=['提交', '重置','上传文件','下载模板','历史记录'])
            ])


            if product_info['actions'] == '提交':
                # 处理数据并更新历史结果
                product_info['product_type'] = type_dict[product_info['product_type']]
                processed_data = mc.main_calculate_gui(product_info)
                update_history(processed_data)


            elif product_info['actions'] == '重置':
                clear('history')  # 清空历史结果

            elif product_info['actions'] == '上传文件':
                excel_file = file_upload('选择一个文件：',accept="xlsx/*")
                timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
                filename = timestamp + "-" + excel_file['filename']
                store_path = filepath/ 'asset'/ filename
                
                with open(store_path, 'wb') as f:
                    f.write(excel_file['content'])
                processed_data = mc.main_calculate_gui_bulk(store_path)
                content = open(store_path, 'rb').read()
                put_file(filename,content,'已处理文件下载')
                cleanup_logger.info(f'{filename} created!!')
                # webbrowser.open_new_tab('file://' / store_path)
            elif product_info['actions'] == '下载模板':
                templates_file = "template.xlsx"
                content = open(filepath / templates_file, 'rb').read()
                put_file('templates.xlsx',content,'模板下载')


            elif product_info['actions'] == '历史记录':
                history_page()
        

# 得出结果 
def update_history(result):
    original_product_dict = result[0]
    storage_fee_dict = result[1]
    # 将新的结果添加到历史结果中，并更新显示

    new_size = f"{storage_fee_dict['length']}x{storage_fee_dict['width']}x{storage_fee_dict['height']}"
    original_size = f"{original_product_dict['length']}x{original_product_dict['width']}x{original_product_dict['height']}"

    flipped_dict = {value: key for key, value in type_dict.items()}

    final_data = {
                    "计算日期":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "产品名称":original_product_dict['name'],
                    "国家":original_product_dict['country'],
                    "模式":flipped_dict[original_product_dict['product_type']],
                    "年份":original_product_dict['year'],
                    f"尺寸({original_product_dict['size_unit']})":original_size,
                    f"尺寸({storage_fee_dict['size_unit']})":new_size, 
                    f"重量({original_product_dict['weight_unit']})":original_product_dict['weight'],
                    f"重量({storage_fee_dict['weight_unit']})":storage_fee_dict['weight'],
                    f"体积重{storage_fee_dict['weight_unit']}":storage_fee_dict['volume_weight'],
                    f"计费重量{storage_fee_dict['weight_unit']}":storage_fee_dict['actual_weight'],
                    f"体积{storage_fee_dict['volume_unit']}":storage_fee_dict['product_volume'],
                    "FBA尺寸":storage_fee_dict['size_type'],
                    "亚马逊派送费":f"${storage_fee_dict['delivery_fee']}",
                    "1-9月仓储费":f"${storage_fee_dict['1-9_Storage_Fee']}",
                    "10-12月仓储费":f"${storage_fee_dict['10-12_Storage_Fee']}"}

    keys = list(final_data.keys())
    values = list(final_data.values())


    table_data = [list(keys), list(values)]
    save_history_to_file(final_data)

    # 将历史结果转换为 HTML 并显示
    with use_scope('history', clear=True):
        put_table(table_data)
        # put_html(styled_html)


# 根据时间来判断是否删除服务器上asset的文件
def clean_assets_folder():
    assets_folder = filepath / 'asset'  # Assuming 'filepath' is a Path object as in your script
    current_time = datetime.now()

    for file in assets_folder.iterdir():
        # Extract timestamp from the filename
        try:
            timestamp_str = file.name.split("-")[0]
            file_time = datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
        except (ValueError, IndexError):
            cleanup_logger.warning(f"Filename {file.name} does not start with a valid timestamp.")
            continue

        # If the file is older than 24 hours, delete it
        if current_time - file_time > timedelta(hours=24):
            try:
                file.unlink()
                cleanup_logger.info(f"Deleted old file: {file.name}")
            except OSError as e:
                cleanup_logger.error(f"Error deleting file {file.name}: {e}")        

# 保存历史记录到文件
def save_history_to_file(processed_data):
    # processed_data["计算日期"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    history_file_name = filepath /'asset'/ f'{timestamp}-history.json'
    with open(history_file_name, 'w') as jsonfile:
        json.dump(processed_data, jsonfile)
    

# 读取历史文件
def read_all_history_records():
    history_path = filepath /'asset'
    history_files = history_path.glob('*-history.json')
    records = []
    for history_file in sorted(history_files):
        try:
            with open(history_file, 'r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
                records.append(data)
        except json.decoder.JSONDecodeError as err:
            print(f"JSON Decode Error: {err.msg} - Line {err.lineno} Column {err.colno}")
            return {} 

    return records


# 历史页面
def history_page():
    history_records = read_all_history_records()
    if not history_records:
        popup('历史记录', put_text("没有历史记录。"))
    else:
        headers = history_records[0].keys()  # 假设所有记录具有相同的字段
        table_data = [list(record.values()) for record in history_records]
        popup('历史记录', put_table([headers] + table_data),size='large')


# # 通过年份动态筛选模式
# def update_product_type_options(year):
#     if year == '2023':
#         product_type_options = ['NOR','NOR-LOW','CLO','HAD','PEK']
#     elif year == '2024':
#         product_type_options = ['NOR','NOR-LOW','CLO','CLO-LOW','HAD','HAD-LOW']
#     return product_type_options


# # Flask集成
# app = Flask(__name__)
# app.add_url_rule('/', 'webio_view', webio_view(main),
#                  methods=['GET', 'POST', 'OPTIONS'])

if __name__ == '__main__':
    # 删除24小时后的文件
    scheduler = BackgroundScheduler()
    scheduler.add_job(clean_assets_folder,'interval',hours=1)
    scheduler.start()
    # 使用PyWebIO的start_server方法运行
    start_server(main, port=5289)
    # 或者使用Flask运行
    # app.run(host='localhost', port=8080)
