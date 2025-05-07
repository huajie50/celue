import os
from datetime import datetime
import streamlit as st

# 省间现货策略文件夹路径，需根据实际情况修改
provincial_spot_strategy_path = '省间现货策略'

# 获取当前文件名称
current_file_name = os.path.basename(__file__)
# 提取关键字，这里简单假设文件名中有用信息从开始到 .py 前
target_keyword = os.path.splitext(current_file_name)[0]

# 获取省间现货策略文件夹下的所有文件夹
folders = [f for f in os.listdir(provincial_spot_strategy_path) if os.path.isdir(os.path.join(provincial_spot_strategy_path, f))]

# 初始化最近日期和对应的文件夹
latest_date = datetime.min
latest_folder = None

# 遍历所有文件夹，找到日期最近的文件夹
for folder in folders:
    try:
        # 修改日期解析格式为 %Y-%m-%d
        folder_date = datetime.strptime(folder, '%Y-%m-%d')
        if folder_date > latest_date:
            latest_date = folder_date
            latest_folder = folder
    except ValueError:
        # 若文件夹名无法转换为日期，则跳过
        continue

matched_files = []
if latest_folder:
    # 构建最近文件夹的完整路径
    latest_folder_path = os.path.join(provincial_spot_strategy_path, latest_folder)
    # 获取最近文件夹中所有文件的名称
    file_names = [f for f in os.listdir(latest_folder_path) if os.path.isfile(os.path.join(latest_folder_path, f))]

    # 查找包含目标关键字的文件
    matched_files = [file for file in file_names if target_keyword in file]

# Streamlit 页面部分
st.title("现货")

# 通过用户输入的方式进行身份验证
username = st.text_input("请输入用户名：")
password = st.text_input("请输入密码：", type="password")
if username == "3" and password == "3":
    # 身份验证成功
    st.success("身份验证成功！")
    try:
        # 显示并提供下载匹配的文件
        if matched_files:
            for file in matched_files:
                file_path = os.path.join(latest_folder_path, file)
                with open(file_path, "rb") as f:
                    file_data = f.read()
                st.write(file)
                st.download_button(
                    label=f"下载 {file}",
                    data=file_data,
                    file_name=file,
                    mime="application/octet-stream"
                )
        else:
            st.write(f"未找到包含 '{target_keyword}' 的文件。")
    except:
        st.error("无法获取数据")
else:
    st.warning("请输入正确的用户名和密码以查看文件。")


