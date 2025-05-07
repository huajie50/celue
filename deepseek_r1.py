import streamlit as st
import os

# 设置页面标题和布局
st.set_page_config(page_title="文件上传界面", layout="centered")

# 页面标题
st.title("🌟 文件上传界面")

# 描述信息
st.markdown("""
欢迎使用文件上传工具！  
您可以从客户端上传文件，或者从服务器选择文件上传。
""")

# 上传文件的功能
uploaded_file = st.file_uploader("选择一个文件进行上传", type=["txt", "csv", "xlsx", "png", "jpg", "pdf"])

if uploaded_file is not None:
    # 显示上传的文件名
    st.success(f"文件 `{uploaded_file.name}` 上传成功！")
    # 保存文件到服务器
    with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.info("文件已保存到服务器的 `uploads` 文件夹中。")

# 服务器端文件选择功能
st.markdown("### 或者从服务器选择文件上传：")
server_files = os.listdir("uploads") if os.path.exists("uploads") else []
if server_files:
    selected_file = st.selectbox("选择一个文件", server_files)
    if st.button("上传选中的文件"):
        st.success(f"文件 `{selected_file}` 已成功上传！")
else:
    st.warning("服务器上没有可用的文件。")

# 美化界面
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
</style>
