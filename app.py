import streamlit as st
import plotly.express as px
import pandas as pd

# 1. 페이지 설정 및 반응형 최적화
st.set_page_config(page_title="조별과제 잔혹사: 나의 팀플 성향 진단", page_icon="📝", layout="centered")

# 2. CSS 스타일 (폰트를 'Nanum Pen Script'로 변경하여 귀여운 느낌 강조)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&display=swap');
    
    * { 
        font-family: 'Nanum Pen Script', cursive !important; 
    }
    
    .stApp {
        background-color: #F4F7F9;
    }
    
    .card-container {
        background-color: #ffffff;
        padding: 35px;
        border-radius: 20px;
        box-shadow: 0px 8px 16px rgba(187, 143, 206, 0.15);
        margin-bottom: 30px;
        border: 1px solid #E8DAEF;
        line-height: 2.0;
    }
    
    .main-title {
        font-size: 2.6rem; /* 폰트 변경에 맞춰 크기 조정 */
        font-weight: bold;
        text-align: center;
        color: #6C3483;
        line-height: 1.8;
        margin-bottom: 12px;
    }
    
    .sub-title {
        font-size: 1.6rem;
        text-align: center;
        color: #7FB3D5;
        margin-bottom: 35px;
        font-weight: 500;
        line-height: 1.8;
    }
    
    .q-badge {
        background-color: #FEF9E7;
        color: #7D6608;
        padding: 6px 16px;
        border-radius: 30px;
        font-weight: bold;
        font-size: 1.4rem;
        display: inline-block;
        margin-bottom: 15px;
        border: 1px solid #F9E79F;
    }
    
    .q-text {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2C3E50;
        line-height: 1.9;
        margin-bottom: 20px;
    }
    
    div[data-testid="stRadio"] {
        margin-top: 15px !important;
    }
    
    div[data-testid="stRadio"] [data-testid="stWidgetLabel"] + div > div {
        margin-bottom: 16px !important;
        padding: 10px 14px !important;
        background-color: #ffffff;
        border-radius: 10px;
        border: 1px solid #EAECEE;
    }
    
    div[data-testid="stRadio"] label {
        font-size: 1.4rem !important;
        color: #2C3E50 !important;
        line-height: 1.8 !important;
        cursor: pointer;
    }
    
    .type-container {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #BB8FCE;
        margin-bottom: 25px;
        box-shadow: 0px 4px 12px rgba(187, 143, 206, 0.1);
        line-height: 1.9;
    }
    
    .character-avatar {
        font-size: 3rem;
        text-align: center;
        margin: 10px auto;
        width: 80px;
        height: 80px;
        background-color: #EBF5FB;
        border-radius: 50%;
        line-height: 80px;
    }
    
    .type-container h4 {
        font-size: 1.8rem !important;
        font-weight: bold;
        text-align: center;
        color: #5B2C6F;
        margin-top: 12px;
        margin-bottom: 18px;
    }
    
    .type-container p {
        font-size: 1.4rem !important;
        line-height: 1.9;
        color: #566573;
        margin-bottom: 10px;
    }
    
    div[data-testid="stMarkdownContainer"] > p {
        font-size: 1.4rem !important;
        color: #34495E;
        line-height: 1.9;
    }
    
    h3 {
        font-size: 2rem !important;
        color: #6C3483 !important;
        font-weight: bold !important;
        line-height: 1.8;
    }
    
    .solution-box {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 18px;
        border-left: 6px solid #BB8FCE;
        border-top: 1px solid #F4F6F7;
        border-right: 1px solid #F4F6F7;
        border-bottom: 1px solid #F4F6F7;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.02);
        line-height: 1.9;
    }
    .solution-title {
        font-size: 1.6rem;
        font-weight: bold;
        color: #5B2C6F;
        margin-bottom: 6px;
    }
    .solution-desc {
        font-size: 1.4rem !important;
        color: #5D6D7E;
        line-height: 1.9;
    }
    
    .stButton>button {
        border-radius: 12px !important;
        font-size: 1.4rem !important;
        padding: 8px 25px !important;
        background-color: #BB8FCE !important;
        color: white !important;
        border: none !important;
        box-shadow: 0px 4px 8px rgba(187, 143, 206, 0.3) !important;
        transition: all 0.15s ease;
    }
    .stButton>button:hover {
        background-color: #A569BD !important;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

