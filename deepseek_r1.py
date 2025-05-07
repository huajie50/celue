import streamlit as st
from openai import OpenAI
import json
import pandas as pd
from sqlalchemy import create_engine
from datetime import timedelta,datetime

class Yanx:
    def __init__(self):
        self.zjrl = {
            '灵武电厂#1机': 600,
            '灵武电厂#2机': 600,
            '大坝电厂#1机': 330,
            '大坝电厂#4机': 330,
            '大坝电厂#3机': 330,
            '大坝电厂#2机': 330,
            '中卫热电厂#1机': 350,
            '中卫热电厂#2机': 350,
            '吴忠朔方热电厂#1机': 350,
            '吴忠朔方热电厂#2机': 350,
            '六盘山热电厂#1机': 330,
            '六盘山热电厂#2机': 330,
            '国华宁东电厂#1机': 330,
            '国华宁东电厂#2机': 330,
            '马莲台电厂#1机': 330,
            '马莲台电厂#2机': 330,
            '石嘴山一电厂#1机': 350,
            '石嘴山一电厂#2机': 330,
            '石嘴山二电厂#1机': 330,
            '石嘴山二电厂#4机': 330,
            '石嘴山二电厂#3机': 330,
            '石嘴山二电厂#2机': 330,
            '西夏热电厂#1机': 200,
            '西夏热电厂#2机': 200,
            '大武口热电厂#1机': 330,
            '大武口热电厂#2机': 330,
            '西夏热电二期电厂#3机': 350,
            '西夏热电二期电厂#4机': 350,
            '中宁二电厂#1机': 330,
            '中宁二电厂#2机': 330,
            '尚德电厂#1机': 660,
            '尚德电厂#2机': 660,
            '青铝自备电厂#1机': 330,
            '青铝自备电厂#2机': 330,        
            '西部热电厂#1机': 150,
            '西部热电厂#2机': 150,        
            '英力特热电厂#1机': 330,
            '英力特热电厂#2机': 330,        
            '临河红柳湾电厂#1机': 350,
            '临河红柳湾电厂#2机': 350,
            '青铜峡水电厂#1机': 28,
            '青铜峡水电厂#9机': 28,
            '青铜峡水电厂#8机': 28,
            '青铜峡水电厂#7机': 28,
            '青铜峡水电厂#6机': 28,
            '青铜峡水电厂#5机': 28,
            '青铜峡水电厂#4机': 28,
            '青铜峡水电厂#3机': 28,
            '青铜峡水电厂#2机': 28,
            '沙坡头水电厂#1机': 28,
            '沙坡头水电厂#6机': 28,
            '沙坡头水电厂#5机': 28,
            '沙坡头水电厂#4机': 28,
            '沙坡头水电厂#3机': 28,
            '沙坡头水电厂#2机': 28,
            '哈纳斯热电一厂#1机': 32,
            '哈纳斯热电一厂#2机': 32,
            '哈纳斯热电二厂#1机': 111,
            '哈纳斯热电二厂#4机': 111,
            '哈纳斯热电二厂#3机': 111,
            '哈纳斯热电二厂#2机': 111,
        }

        self.rongl_all = ['中卫热电厂#1机', '中卫热电厂#2机', '吴忠朔方热电厂#1机', '吴忠朔方热电厂#2机', '英力特热电厂#1机',
            '英力特热电厂#2机', '六盘山热电厂#1机', '六盘山热电厂#2机', '临河红柳湾电厂#1机', '临河红柳湾电厂#2机',
            '国华宁东电厂#1机', '国华宁东电厂#2机', '灵武电厂#1机', '灵武电厂#2机', '大坝电厂#1机', '大坝电厂#4机',
            '大坝电厂#3机', '大坝电厂#2机', '马莲台电厂#1机', '马莲台电厂#2机', '石嘴山一电厂#1机', '石嘴山一电厂#2机',
            '石嘴山二电厂#1机', '石嘴山二电厂#4机', '石嘴山二电厂#3机', '石嘴山二电厂#2机', '西夏热电厂#1机',
            '西夏热电厂#2机', '大武口热电厂#1机', '大武口热电厂#2机', '哈纳斯热电二厂#1机', '哈纳斯热电二厂#4机',
            '哈纳斯热电二厂#3机', '哈纳斯热电二厂#2机', '西夏热电二期电厂#3机', '西夏热电二期电厂#4机', '中宁二电厂#1机',
            '中宁二电厂#2机', '哈纳斯热电一厂#1机', '哈纳斯热电一厂#2机', '青铜峡水电厂#1机', '青铜峡水电厂#9机',
            '青铜峡水电厂#8机', '青铜峡水电厂#7机', '青铜峡水电厂#6机', '青铜峡水电厂#5机', '青铜峡水电厂#4机',
            '青铜峡水电厂#3机', '青铜峡水电厂#2机', '沙坡头水电厂#1机', '沙坡头水电厂#6机', '沙坡头水电厂#5机',
            '沙坡头水电厂#4机', '沙坡头水电厂#3机', '沙坡头水电厂#2机', '西部热电厂#1机', '西部热电厂#2机',
            '青铝自备电厂#1机', '青铝自备电厂#2机', '尚德电厂#1机', '尚德电厂#2机'] 
        self.guoneng =  ['中卫热电厂#1机', '中卫热电厂#2机', 
                    '国华宁东电厂#1机', '国华宁东电厂#2机',
                    '灵武电厂#1机', '灵武电厂#2机', '大坝电厂#1机', '大坝电厂#4机','大坝电厂#3机', '大坝电厂#2机','石嘴山一电厂#1机', '石嘴山一电厂#2机','石嘴山二电厂#1机', '石嘴山二电厂#4机', '石嘴山二电厂#3机', '石嘴山二电厂#2机',
                    '大武口热电厂#1机', '大武口热电厂#2机', '尚德电厂#1机', '尚德电厂#2机']
        self.feiguoneng = ['中宁二电厂#1机', '中宁二电厂#2机','吴忠朔方热电厂#1机', '吴忠朔方热电厂#2机','六盘山热电厂#1机', '六盘山热电厂#2机', '马莲台电厂#1机', '马莲台电厂#2机','西夏热电厂#1机', '西夏热电厂#2机','西夏热电二期电厂#3机', '西夏热电二期电厂#4机' ]
        self.zibei = ['英力特热电厂#1机','英力特热电厂#2机', '临河红柳湾电厂#1机', '临河红柳湾电厂#2机', '青铝自备电厂#1机', '青铝自备电厂#2机', '西部热电厂#1机', '西部热电厂#2机']
        self.shuidian = ['青铜峡水电厂#1机', '青铜峡水电厂#9机', '青铜峡水电厂#8机', '青铜峡水电厂#7机', '青铜峡水电厂#6机', '青铜峡水电厂#5机', '青铜峡水电厂#4机', '青铜峡水电厂#3机', '青铜峡水电厂#2机', 
                    '沙坡头水电厂#1机', '沙坡头水电厂#6机', '沙坡头水电厂#5机', '沙坡头水电厂#4机', '沙坡头水电厂#3机', '沙坡头水电厂#2机']
        self.ranqi = ['哈纳斯热电一厂#1机', '哈纳斯热电一厂#2机','哈纳斯热电二厂#1机', '哈纳斯热电二厂#4机','哈纳斯热电二厂#3机', '哈纳斯热电二厂#2机']

        self.bianji = self.ranqi + self.shuidian + self.zibei

        # 火电装机容量是多少？ 缺少1.鸳鸯湖电厂、2.大坝三期电厂、
        self.huodian = self.guoneng  + self.zibei + self.feiguoneng        

        # 此函数用于调用装机容量

    def load_and_process_data(self, dbname, sheetname, start_date, end_date):
        """加载并处理运行状态数据"""
        df = self.read_table1(dbname, sheetname, start_date, end_date)
        df['时间'] = pd.to_datetime(df['时间'])
        
        # 时间调整逻辑
        df['时间'] = df['时间'] - pd.Timedelta(minutes=15)
        df['时间'] = df['时间'].apply(lambda x: x + pd.Timedelta(minutes=1) if x.minute == 44 else x)
        
        df.index = pd.to_datetime(df['时间'])
        df = df.drop(columns=['时间']).fillna(0)
        
        # 替换机组状态值为装机容量
        for jizuname in self.zjrl:
            df[jizuname] = df[jizuname].replace(1, self.zjrl[jizuname])        
        return df        
        
    def time_45(self,df):
        df['时间'] = pd.to_datetime(df['时间'])
        df['时间'] = df['时间'] - pd.Timedelta(minutes=15)
        df['时间'] = df['时间'].apply(lambda x: x + pd.Timedelta(minutes=1) if x.minute == 44 else x)
        return df.set_index('时间', drop=True)
    def df_gs(self, df, str_gs):
        """
        筛选包含特定字符串的列
        
        参数:
            df: 要筛选的DataFrame
            str_gs: 要筛选的字符串
            
        返回:
            包含特定字符串的列的DataFrame
        """
        list_dw = []
        for city in df.columns:
            if str_gs in city:
                list_dw.append(city)
        return df[list_dw]
    
    def read_table(self, dbname, Sheetname):
        """
        从数据库读取整个表格
        
        参数:
            dbname: 数据库名称
            Sheetname: 表名称
            
        返回:
            包含表格数据的DataFrame
        """
        engine = create_engine(f'mysql+pymysql://root:123456@localhost:3306/{dbname}')
        conn = engine.connect()
        query = f"SELECT * FROM {Sheetname}"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    
    def read_table1(self, dbname, Sheetname, start_time, end_time):
        """
        从数据库读取表格数据，并根据时间范围筛选数据
        
        参数:
            dbname: 数据库名称
            Sheetname: 表名称
            start_time: 起始时间（字符串格式，例如 '2025-01-01'）
            end_time: 结束时间（字符串格式，例如 '2025-01-15'）
            
        返回:
            包含时间范围内数据的DataFrame
        """
        engine = create_engine(f'mysql+pymysql://root:123456@localhost:3306/{dbname}')
        conn = engine.connect()
        query = f"""
            SELECT * FROM {Sheetname}
            WHERE 时间 >= '{start_time}' AND 时间 <= '{end_time} 23:59:59'
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df



class DeepSeekChatApp:
    def __init__(self, api_url, api_key, model_name):
        """
        初始化 DeepSeekChatApp 类。
        
        :param api_url: API 地址
        :param api_key: API 密钥
        :param model_name: 模型名称
        """
        self.api_url = api_url
        self.api_key = api_key
        self.model_name = model_name
        self.client = OpenAI(base_url=api_url, api_key=api_key)
        self.chat_history = []
        self.system_prompt = "你作为国能宁夏能源销售有限公司的AI对话小助手，具备电力系统分析、经济学原理和电力市场运作机制的专业知识。你熟悉电力市场的定价机制、交易模式以及市场供需关系对电力价格的影响，同时掌握气象条件对电网电力供应平衡的影响，并能提供精准的专业分析和建议。你需维护公司形象，体现官网的严谨性，积极帮助同事解决关于售电、售煤、售热等相关问题，提供准确、高效的支持。请用专业、严谨且友好的中文回答问题。"

    def set_system_prompt(self, prompt):
        """
        设置系统提示词，用于指导 AI 的回答。
        
        :param prompt: 系统提示词内容
        """
        self.system_prompt = prompt

    def initialize_session_state(self):
        """
        初始化 Streamlit 的会话状态（chat_history）。
        """
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

    def display_header(self):
        """
        显示 Streamlit 页面的标题和描述。
        """
        st.title("国能宁夏能源销售有限公司")
        st.subheader("接入集团 DeepSeek R1 模型，助力智慧协作与创新")
        st.write("欢迎使用公司内网的 DeepSeek R1 智能助手！在这里，我们可以团结协作，共享共创，共同推动公司发展。")

    def get_user_input(self):
        """
        获取用户输入的问题。
        
        :return: 用户输入的文本
        """
        return st.text_area("请输入您的问题：", height=100)

    def send_message(self, user_input):
        """
        发送用户消息并获取 AI 回复。
        
        :param user_input: 用户输入的文本
        """
        if user_input.strip():
            # 将用户消息添加到历史记录
            st.session_state["chat_history"].append({
                "role": "user",
                "content": user_input
            })

            # 构建包含系统提示词和历史对话的消息
            messages = [
                {
                    "role": "system",
                    "content": self.system_prompt
                }
            ]
            messages.extend([{"role": msg["role"], "content": msg["content"]} for msg in st.session_state["chat_history"]])

            try:
                # 调用 DeepSeek R1 模型
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    stream=True,
                    temperature=0.3,
                    max_tokens=2000
                )
            except Exception as e:
                st.error(f"Error connecting to API: {e}")
                st.error(f"请检查 API 地址 `{self.api_url}` 的合法性，或稍后重试。")
                st.stop()

            # 处理流式响应
            full_response = ""
            reasoning_content = ""
            response_placeholder = st.empty()

            for chunk in response:
                if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
                    reasoning_content += chunk.choices[0].delta.reasoning_content
                    response_placeholder.markdown(f"""
                    <div style="border-left: 4px solid #4CAF50; padding: 1rem; margin: 1rem 0; background-color: #f8f9fa; border-radius: 5px;">
                        <div style="color: #2c3e50; font-weight: bold; margin-bottom: 0.5rem;">🤔 思考过程</div>
                        <div style="color: #34495e;">{reasoning_content}</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(f"""
                    <div style="border-left: 4px solid #4CAF50; padding: 1rem; margin: 1rem 0; background-color: #f8f9fa; border-radius: 5px;">
                        <div style="color: #2c3e50; font-weight: bold; margin-bottom: 0.5rem;">🤖 AI 回答</div>
                        <div style="color: #34495e;">{full_response}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # 将 AI 回复和思维过程添加到历史记录
            st.session_state["chat_history"].append({
                "role": "assistant",
                "content": full_response,
                "reasoning": reasoning_content
            })

    def display_chat_history(self):
        """
        显示历史对话记录。
        """
        st.header("历史对话")
        with st.expander("点击查看历史对话"):
            for message in st.session_state["chat_history"]:
                if message["role"] == "user":
                    st.write(f"**用户：** {message['content']}")
                else:
                    st.write(f"**助手：** {message['content']}")
                    if "reasoning" in message and message["reasoning"].strip():
                        st.write(f"**思考过程：** {message['reasoning']}")

    def clear_chat_history(self):
        """
        清空历史对话记录。
        """
        st.session_state["chat_history"] = []
        st.success("历史对话已清空！")

    def save_chat_history(self):
        """
        保存历史对话记录到文件。
        """
        with open("chat_history.json", "w") as f:
            json.dump(st.session_state["chat_history"], f)
        st.success("历史对话已保存！")









# Streamlit 应用入口
def main():
    st.set_page_config(
        page_title="国能宁夏能源销售有限公司 - DeepSeek R1 智能助手",
        page_icon="💡",
        layout="wide",
        initial_sidebar_state="auto"
    )

    api_url = "http://ds-r1.ceic.com:3000/v1"
    api_key = "sk-XYSmatdb9JBMpnJB0b87540e236c4eB2A20bD32f0eE6547c"
    model_name = "deepseek-ai/DeepSeek-R1"

    # 创建 DeepSeekChatApp 实例
    chat_app = DeepSeekChatApp(api_url, api_key, model_name)

    # 设置自定义提示词（后端直接设置）
    custom_prompt = ""
    chat_app.set_system_prompt(custom_prompt)

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