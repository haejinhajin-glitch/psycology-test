import streamlit as st
import plotly.express as px
import pandas as pd

# 1. 페이지 설정 및 반응형 최적화
st.set_page_config(page_title="말랑말랑 일상 선택 테스트", page_icon="🧸", layout="centered")

# 2. 아기자기하고 귀여운 파스텔톤 일상 UI 디자인 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght=400;500;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    
    /* 전체 배경에 부드러운 감성 더하기 */
    .stApp {
        background-color: #FDFBF7;
    }
    
    /* 귀여운 둥근 카드 스타일 */
    .card-container {
        background-color: #ffffff;
        padding: 35px;
        border-radius: 28px;
        box-shadow: 0px 10px 25px rgba(229, 220, 203, 0.4);
        margin-bottom: 25px;
        border: 2px solid #F3EFE0;
    }
    
    /* 타이틀 및 폰트 스타일 */
    .main-title {
        font-size: 2.6rem;
        font-weight: 700;
        text-align: center;
        color: #4A3E3D;
        margin-bottom: 8px;
    }
    .sub-title {
        font-size: 1.3rem;
        text-align: center;
        color: #8A7E72;
        margin-bottom: 35px;
        font-weight: 500;
    }
    
    /* 말랑말랑 배지 스타일 */
    .q-badge {
        background-color: #FFF0F5;
        color: #FF6B8B;
        padding: 6px 16px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.1rem;
        display: inline-block;
        margin-bottom: 18px;
        border: 1px dashed #FFB6C1;
    }
    .q-text {
        font-size: 1.45rem;
        font-weight: 700;
        color: #4A3E3D;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    
    /* 캐릭터 결과 컨테이너 */
    .type-container {
        background-color: #FAFAFA;
        padding: 30px;
        border-radius: 24px;
        border: 2px solid #E2E8F0;
        margin-bottom: 25px;
    }
    .character-avatar {
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 10px;
