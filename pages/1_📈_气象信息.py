import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from openai import OpenAI
from deepseek_r1 import DeepSeekChatApp
# 设置matplotlib的默认字体和显示设置
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = ['FangSong']
pd.set_option('display.float_format', lambda x: '%.2f' % x)

# 设置网页信息 
st.set_page_config(page_title="数据大屏", page_icon=":bar_chart:", layout="wide")

# 定义列名映射
columns_dic_cfs = {
    'pwat':'一小时内总降水(包括雨和雪)',
    'dlwrf': '下行长波辐照通量',
    'u10': '地表10米风速U分量',
    'v10': '地表10米风速V分量',
    't2m@C': '地面2米气温',
}
columns_rename_cfs = {
    't2m': '地面2米气温',
    'ws10m': '地面10米风速'
}

columns_dic_icon = {
    'nswrf_top': '模型顶层净短波辐射通量',
    'ws10m': '地面10米风速',
    't2m@C': '地面2米气温',
    'tp':'一小时内总降水(包括雨和雪)',
}
columns_rename_icon = {
    't2m': '地面2米气温',
    'd2m': '地面2米露点温度'
}

# 定义API请求的数据类型和位置
# NOAA-CFS-6h
data_type_cfs = 'cfs_h6_surface'
# DWD-ICON
data_type_icon = 'icon_surface'

# 定义地名和对应的经纬度
locations = {
    "宁夏马家滩": {"lon": 106.6, "lat": 37.4},
    "四川成都": {"lon": 104.06, "lat": 30.67},
    "浙江杭州": {"lon": 120.15, "lat": 30.25},
    "青海西宁": {"lon": 101.77, "lat": 36.62},
    "甘肃兰州": {"lon": 103.82, "lat": 36.06},
    "新疆乌鲁木齐": {"lon": 87.62, "lat": 43.82},
}


def rs_to_df(rs, columns_dic, columns_rename):
    """将API响应转换为DataFrame"""
    if rs.json()['data'] is None:
        print(f'未发布气象数据~')
        df = pd.DataFrame(0, index=range(1), columns=['时间'])
        df['时间'] = ['23:00']
        df = df.reset_index(drop=True)
    else:
        data = rs.json()['data']
        values = data['data'][0]['values']
        timestamp = data['timestamp']
        df = pd.DataFrame(values, index=timestamp)
        df.columns = data['mete_var']
        df.rename(columns=columns_dic, inplace=True)
        df.rename(columns=columns_rename, inplace=True)
    return df

def drawqx(ax1, df, title, radiation_col='下行长波辐照通量'):
    """绘制气象数据图表"""
    if radiation_col not in df.columns:
        print(f"警告：列 '{radiation_col}' 不存在。可用列名: {df.columns}")
        return
    
    x_values = np.arange(len(df.index))
    x_labels = df.index.astype(str)
    
    # 绘制条形图（辐射量）
    bar = ax1.bar(x_values, df[radiation_col], color='lightblue', label='辐射量')
    ax1.set_ylabel('辐射量（w/m^2）', color='lightblue')
    
    # 创建第二个Y轴
    ax2 = ax1.twinx()
    
    # 绘制折线图（风速）
    if '地面10米风速' in df.columns:
        line1, = ax2.plot(x_values, df['地面10米风速'].to_numpy(), color='red', label='风速')
    
    # 绘制折线图（气温）
    if '地面2米气温' in df.columns:
        line2, = ax2.plot(x_values, df['地面2米气温'].to_numpy(), color='green', label='气温')
    
    # 绘制折线图（降水）
    if '一小时内总降水(包括雨和雪)' in df.columns:
        line3, = ax2.plot(x_values, df['一小时内总降水(包括雨和雪)'].to_numpy(), color='blue', label='可降水量')
    
    # 设置右侧Y轴标签
    ax2.set_ylabel('风速、气温（米/秒、℃） | 降水（mm）', color='red')
    
    # 设置X轴刻度和标签
    ax1.set_xticks(x_values)
    ax1.set_xticklabels(x_labels, fontsize=14, rotation=70)
    ax1.grid()
    
    # 显示图例
    handles = [bar]
    if 'line1' in locals():
        handles.append(line1)
    if 'line2' in locals():
        handles.append(line2)
    if 'line3' in locals():
        handles.append(line3)
    ax1.legend(handles=handles, loc='upper left')
    
    # 设置标题
    ax1.set_title(title, fontsize=18, c='r')

def get_time_comparison():
    """获取当前时间与12:00的关系，返回合适的日期和时间"""
    now = datetime.now()
    noon_today = now.replace(hour=23, minute=0, second=0, microsecond=0)
    previous_date_noon = (now - timedelta(days=1)).replace(hour=12, minute=0, second=0, microsecond=0) if now < noon_today else now.replace(hour=0, minute=0, second=0, microsecond=0)
    return previous_date_noon.strftime('%Y-%m-%d %H:%M:%S')

def qixiang_lishiguance(input_date, column_list, lon, lat, data_type):
    """从API获取气象数据"""
    url = f"https://api-pro-openet.terraqt.com/v1/{data_type}/point"
    headers = {
        'Content-Type': 'application/json',
        'token': 'jBDMwEmYmdDZlBDMwQWZwYGZxYGZ0gDN'
    }
    data = {
        'time': f'{input_date}',
        'lon': lon,
        'lat': lat,
        'mete_vars': column_list
    }

    response = requests.post(url, headers=headers, json=data)
    return response

def get_previous_day(date_str, days):
    """获取指定日期的前几天或后几天"""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    previous_date_obj = date_obj + timedelta(days=days)
    return previous_date_obj.strftime('%Y-%m-%d')

def fetch_and_plot_weather_data(ax1, df, target_date, group_by='month'):
    """获取并绘制指定日期的气象数据"""
    if group_by == 'month':
        df_target = df[pd.to_datetime(df.index).month == pd.to_datetime(target_date).month]
        date_df = df_target.groupby(pd.to_datetime(df_target.index).date).mean()
        title = f'{target_date.strftime("%Y-%m")} 气象数据'
    elif group_by == 'year':
        df_target = df[pd.to_datetime(df.index).year == pd.to_datetime(target_date).year]
        date_df = df_target.groupby(pd.to_datetime(df_target.index).month).mean()
        title = f'{target_date.strftime("%Y")} 气象数据'
    
    if not date_df.empty:
        drawqx(ax1, date_df, title)
    else:
        print(f'{target_date} 无可用数据')

def generate_prompt(name,date,df):
    prompt_lines = []
    
    # 添加数据概览
    prompt_lines.append(f"{name}{date}气象数据：")
    prompt_lines.append(df.to_string())
    prompt_lines.append("你是一个电力系统及气象学的专家，天气对新能源的影响以及新能源出力对电力系统的影响经验介绍，请用专业、严谨且友好的中文回答问题。")
    prompt_lines.append('回答控制在100字左右')
    for index, row in df.iterrows():

        
        # 新增判断条件：风速大于10m/s
        if '地面10米风速' in df.columns and row['地面10米风速'] > 10:
            prompt_lines.append(f"{index}时段风速较大（{row['地面10米风速']:.1f}m/s），请注意风电场发电效率。")
    print(prompt_lines)
    return "\n".join(prompt_lines)


# 在Streamlit中直接生成总结
def main():
    st.title("未来天气预测")
    
    # 添加下拉选项框选择地名
    selected_location = st.selectbox("选择地区", list(locations.keys()))
    
    # 获取选择的经纬度
    lon = locations[selected_location]["lon"]
    lat = locations[selected_location]["lat"]
    st.write(f"选择的地区: {selected_location}, 经度: {lon}, 纬度: {lat}")
    
    # 添加输入框和查询按钮
    st.write("### 自定义经纬度查询")
    custom_lon = st.number_input("输入经度", value=lon, format="%.6f")
    custom_lat = st.number_input("输入纬度", value=lat, format="%.6f")
    
    if st.button("查询自定义经纬度的天气预测"):
        selected_location = f"自定义位置 ({custom_lon}, {custom_lat})"
        lon = custom_lon
        lat = custom_lat
    
    # 主程序
    today_date = get_time_comparison()
    st.write(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.write(f"启报时间: {today_date}")
    
    response_cfs = qixiang_lishiguance(today_date, list(columns_dic_cfs.keys()), lon, lat, data_type_cfs)
    df_cfs = rs_to_df(response_cfs, columns_dic_cfs, columns_rename_cfs)
    response_icon = qixiang_lishiguance(today_date, list(columns_dic_icon.keys()), lon, lat, data_type_icon)
    df_icon = rs_to_df(response_icon, columns_dic_icon, columns_rename_icon)
    
    # 计算地面10米风速
    df_cfs['ws10m'] = np.sqrt(np.square(df_cfs['地表10米风速U分量']) + np.square(df_cfs['地表10米风速V分量']))
    df_cfs.rename(columns=columns_dic_cfs, inplace=True)
    df_cfs.rename(columns=columns_rename_cfs, inplace=True)

    # 创建4行2列的子图
    fig, axes = plt.subplots(4, 2, figsize=(20, 20))

    # 设置总标题
    plt.suptitle(f'{selected_location} 未来天气预测', fontsize=30, y=1.02)

    # 绘制CFS接口的数据（放到右侧）
    for i, month_offset in enumerate(range(3)):  # 0: 当前月, 1: 下个月, 2: 下下个月
        target_date = datetime.now() + timedelta(days=30 * month_offset)
        fetch_and_plot_weather_data(axes[i, 1], df_cfs, target_date, group_by='month')

    target_date = datetime(2025, 1, 1)
    fetch_and_plot_weather_data(axes[3, 1], df_cfs, target_date, group_by='year')

    api_url = "http://ds-r1.ceic.com:3000/v1"
    api_key = "sk-XYSmatdb9JBMpnJB0b87540e236c4eB2A20bD32f0eE6547c"
    model_name = "deepseek-ai/DeepSeek-R1"

    # 创建 DeepSeekChatApp 实例
    chat_app = DeepSeekChatApp(api_url, api_key, model_name)

    for i, days in enumerate(range(4)):  # 0: 当天, 1: 明天, 2: 后天, 3: 大后天
        tomorrow = get_previous_day(datetime.now().strftime('%Y-%m-%d'), days)
        df_nextday = df_icon[pd.to_datetime(df_icon.index).date == pd.to_datetime(tomorrow).date()]
        if not df_nextday.empty:
            date_str = df_nextday.index[0][:10]
            date_df = df_nextday.groupby(pd.to_datetime(df_nextday.index).hour).mean()
            print(date_df)
            drawqx(axes[i, 0], date_df, f'{date_str} 气象数据', radiation_col='模型顶层净短波辐射通量')
            
            # 生成并设置提示词
            custom_prompt = generate_prompt(selected_location,date_str,date_df)
            chat_app.set_system_prompt(custom_prompt)
    plt.tight_layout()
    # 在 Streamlit 中显示图表
    st.pyplot(fig)





    # 设置自定义提示词（后端直接设置）
    # 在设置custom_prompt之前添加以下代码
    # custom_prompt = generate_prompt()
    # chat_app.set_system_prompt(custom_prompt)

    # 初始化会话状态并显示页面内容
    chat_app.initialize_session_state()
    chat_app.display_header()

    # 获取用户输入并发送消息
    user_input = chat_app.get_user_input()
    if st.button("发送", key="send_message"):
        chat_app.send_message(user_input)

    # 显示历史对话
    chat_app.display_chat_history()

    # 清空和保存历史对话
    if st.button("清空历史对话"):
        chat_app.clear_chat_history()

    if st.button("保存历史对话"):
        chat_app.save_chat_history()


if __name__ == "__main__":
    main()










