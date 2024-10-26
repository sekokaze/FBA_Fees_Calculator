# FBA_Fees_Calculator

FBA_Fees_Calculator 是一个用于计算亚马逊 FBA 费用的工具。该工具提供了一个用户界面，允许用户输入产品信息，并根据亚马逊的费用结构计算出相应的费用。

## 一、功能

- 提供一个用户界面，允许用户输入产品信息。
- 根据用户输入的产品信息，计算出相应的 FBA 费用。
  - 可以计算美国和加拿大的 FBA 费用。
  - 有多种不同的模式，包括计算一般产品，危险品，服装，旺季派送费，多渠道派送费，低价派送费等。
- 支持多种产品类型和尺寸单位。（公制单位/美国英制单位）
- 提供历史记录功能，允许用户查看之前的计算结果。
- 支持上传文件和下载模板功能。

## 二、安装

1. 克隆仓库到本地：

    ```bash
    git clone https://github.com/sekokaze/FBA_Fees_Calculator.git
    ```

2. 安装依赖：

    ```bash
    cd FBA_Fees_Calculator
    pip install -r requirements.txt
    ```

## 三、使用方法

### 3.1 通过tk_main.py运行程序

    ```bash
    python tk_main.py
    ```

1. 打开程序后，在用户界面中输入产品信息。
2. 点击“提交”按钮，程序将根据输入的信息计算出相应的 FBA 费用。
3. 计算结果将显示在页面上，同时历史记录也会更新。
4. 用户可以通过“历史记录”按钮查看之前的计算结果。

### 3.2 通过web_main.py运行程序

    ```bash
    python web_main.py
    ```

1. 打开程序后，在用户界面中输入产品信息。
2. 点击“提交”按钮，程序将根据输入的信息计算出相应的 FBA 费用。
3. 计算结果将显示在页面上，同时历史记录也会更新。
4. 用户可以通过“历史记录”按钮查看之前的计算结果。
5. 用户可以通过“上传文件”按钮上传 Excel 文件进行批量计算。
6. 用户可以通过“下载模板”按钮下载 Excel 模板，用于批量计算。


## 四、贡献

欢迎贡献代码，你可以通过提交 Pull Request 或者 Issue 来参与项目。



