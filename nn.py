import streamlit as st
import streamlit.components.v1 as components
import json
import pandas as pd

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="박민수의 프로필 발표",
    page_icon="👨‍💻",
    layout="wide"
)

# --- 스타일(CSS) 통합 관리 ---
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="st-"] { font-family: 'Noto Sans KR', sans-serif !important; }
        .stButton>button { border: 1px solid #e0e0e0; border-radius: 0.5rem; transition: all 0.2s; }
        .stButton>button:hover { border-color: #667eea; color: #667eea; }
    </style>
""", unsafe_allow_html=True)


# --- 데이터 관리를 위한 Session State ---
# 직업가치관 데이터
if 'job_values' not in st.session_state:
    st.session_state.job_values = {'경제적 보상': 5.0, '성취': 4.7, '직업안정': 4.6, '자기개발': 4.2, '일과 삶의 균형': 4.0, '자율성': 3.8, '변화지향': 3.2, '사회적 인정': 2.7, '사회적 공헌': 2.2}
# 직무역량 데이터
if 'competency_values' not in st.session_state:
    st.session_state.competency_values = {'논리력': 95, '창의성': 90, '목표지향성': 85, '책임감': 80, '협업능력': 60, '감정적 안정성': 55}
# 페이지별 차트 종류 저장
if 'job_chart_type' not in st.session_state: st.session_state.job_chart_type = '레이더 차트'
if 'competency_chart_type' not in st.session_state: st.session_state.competency_chart_type = '레이더 차트'


# --- HTML 콘텐츠 정의 ---

# 1번 슬라이드 (홈) - 투슬리스 GIF 포함됨
home_slide_html = """
<!DOCTYPE html><html lang="ko"><head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>박민수의 프로필 발표</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; padding: 0; font-family: 'Noto Sans KR', sans-serif; }
        .slide-container { width: 100%; height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); position: relative; display: flex; align-items: center; justify-content: center; padding: 2rem; box-sizing: border-box; overflow: hidden; }
        .floating-shapes { position: absolute; width: 100%; height: 100%; top: 0; left: 0; pointer-events: none; }
        .shape { position: absolute; border-radius: 50%; background: rgba(255, 255, 255, 0.08); animation: float 8s ease-in-out infinite; }
        .shape:nth-child(1) { width: 120px; height: 120px; top: 10%; left: 8%; animation-delay: 0s; }
        .shape:nth-child(2) { width: 180px; height: 180px; top: 20%; right: 12%; animation-delay: 3s; }
        .shape:nth-child(3) { width: 100px; height: 100px; bottom: 15%; left: 15%; animation-delay: 6s; }
        .shape:nth-child(4) { width: 140px; height: 140px; bottom: 25%; right: 20%; animation-delay: 4s; }
        @keyframes float { 0%, 100% { transform: translateY(0px) rotate(0deg); } 50% { transform: translateY(-30px) rotate(180deg); } }
        .main-content { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 30px; padding: 4rem 3rem; text-align: center; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1); transform: translateY(30px); opacity: 0; animation: slideUp 1s ease-out forwards; max-width: 800px; width: 100%; position: relative; z-index: 10; }
        @keyframes slideUp { to { transform: translateY(0); opacity: 1; } }
        .main-title { font-weight: 900; font-size: 5rem; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 2rem; animation: titlePulse 4s ease-in-out infinite; line-height: 1.1; }
        @keyframes titlePulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.02); } }
        .welcome-icon { font-size: 8rem; background: linear-gradient(135deg, #ff9a9e, #fecfef); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 2rem; opacity: 0; animation: bounceIn 1s ease-out 0.8s forwards; }
        @keyframes bounceIn { 0% { transform: scale(0); opacity: 0; } 50% { transform: scale(1.1); opacity: 1; } 100% { transform: scale(1); opacity: 1; } }
        
        /* --- 투슬리스 GIF를 위한 스타일 --- */
        .meme-gif-container {
            position: absolute;
            bottom: 20px;
            right: 20px;
            width: 200px; /* GIF 크기 조절 */
            height: auto;
            z-index: 1000; /* 다른 요소들 위에 보이도록 설정 */
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
    </style>
</head><body>
    <div class="slide-container">
        <div class="floating-shapes">
            <div class="shape"></div><div class="shape"></div><div class="shape"></div><div class="shape"></div>
        </div>
        <div class="main-content">
            <div class="welcome-icon"><i class="fas fa-user-graduate"></i></div>
            <h1 class="main-title">프로필 발표</h1>
        </div>
        
        <div class="meme-gif-container">
            <img src="https://media.tenor.com/M0b6-2420w0AAAAM/toothless-dancing-toothless.gif" alt="Toothless Dancing GIF">
        </div>
    </div>
</body></html>
"""

# 2번 슬라이드 (기본 소개)
intro_slide_html = """
<!DOCTYPE html><html lang="ko"><head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>박민수 - 기본 소개</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; padding: 0; font-family: 'Noto Sans KR', sans-serif; }
        .slide-container { width: 100%; height: 100vh; display: flex; align-items: center; justify-content: center; position: relative; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; box-sizing: border-box; }
        .main-title { color: #e9e7f5; font-weight: 700; font-size: 3.5rem; text-align: center; margin-bottom: 2rem; animation: titlePulse 5s ease-in-out infinite; text-shadow: 2px 2px 8px rgba(30, 27, 46, 0.5); }
        .content-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 20px; transform: translateY(30px); opacity: 0; animation: slideUp 0.8s ease-out forwards; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); padding: 1.5rem; height: 100%; }
        @keyframes slideUp { to { transform: translateY(0); opacity: 1; } }
        .profile-section { display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; margin-bottom: 2rem; }
        .bottom-section { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
        .info-item { display: flex; align-items: center; margin-bottom: 1rem; padding: 0.75rem; border-radius: 10px; transition: all 0.3s ease; background: rgba(102, 126, 234, 0.05); }
        .info-icon { background: linear-gradient(135deg, #84fab0, #8fd3f4); color: #374151; width: 35px; height: 35px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 1rem; font-size: 0.9rem; flex-shrink: 0; }
        .info-label { font-weight: 600; color: #6b7280; min-width: 80px; margin-right: 1rem; }
        .info-value { color: #374151; font-weight: 500; }
        .cert-badge { background: linear-gradient(135deg, #ff9a9e, #fecfef); color: #444; padding: 0.75rem 1.5rem; border-radius: 25px; font-weight: 600; margin: 0.5rem; display: inline-flex; align-items: center; box-shadow: 0 4px 15px rgba(255, 154, 158, 0.3); transition: all 0.3s ease; }
        .hobby-badge { background: linear-gradient(135deg, #a8edea, #fed6e3); color: #374151; padding: 0.75rem 1.25rem; border-radius: 20px; font-weight: 600; margin: 0.5rem; display: inline-flex; align-items: center; box-shadow: 0 3px 12px rgba(168, 237, 234, 0.3); transition: all 0.3s ease; }
        .education-item { background: rgba(132, 250, 176, 0.1); padding: 1rem; border-radius: 12px; border-left: 4px solid #84fab0; margin-bottom: 0.75rem; }
        .school-name { font-weight: 700; color: #374151; margin-bottom: 0.25rem; }
        .school-status { font-size: 0.9rem; color: #6b7280; }
        .section-title { color: #4a5568; font-weight: 700; font-size: 1.25rem; margin-bottom: 1rem; display: flex; align-items: center; }
        .icon-container { background: linear-gradient(135deg, #667eea, #764ba2); color: white; width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 0.75rem; }
    </style>
</head><body>
    <div class="slide-container">
        <div class="relative z-10" style="width:100%; max-width: 1200px;">
            <h1 class="main-title" style="margin-bottom: 1rem;">기본 소개</h1>
            <div class="profile-section">
                <div class="content-card">
                    <h2 class="section-title"><div class="icon-container"><i class="fas fa-user"></i></div>기본 정보</h2>
                    <div class="info-item"><div class="info-icon"><i class="fas fa-signature"></i></div><div class="info-label">이름</div><div class="info-value">박민수</div></div>
                    <div class="info-item"><div class="info-icon"><i class="fas fa-map-marker-alt"></i></div><div class="info-label">출생지</div><div class="info-value">충청남도 공주시</div></div>
                </div>
                <div class="content-card">
                    <h2 class="section-title"><div class="icon-container"><i class="fas fa-graduation-cap"></i></div>학력</h2>
                    <div class="education-item"><div class="school-name">공주영명고등학교</div><div class="school-status">졸업</div></div>
                    <div class="education-item"><div class="school-name">건양대학교(논산)</div><div class="school-status">재학 중</div></div>
                </div>
            </div>
            <div class="bottom-section">
                <div class="content-card">
                    <h2 class="section-title"><div class="icon-container"><i class="fas fa-certificate"></i></div>자격증</h2>
                    <div class="text-center">
                        <div class="cert-badge"><i class="fas fa-award mr-2"></i>한국사능력검정시험 1급</div>
                        <div class="cert-badge"><i class="fas fa-fire mr-2"></i>위험물기능사</div>
                    </div>
                </div>
                <div class="content-card">
                    <h2 class="section-title"><div class="icon-container"><i class="fas fa-gamepad"></i></div>취미 & 여가생활</h2>
                    <div class="text-center">
                        <div class="hobby-badge"><i class="fas fa-film mr-2"></i>영화 감상</div>
                        <div class="hobby-badge"><i class="fas fa-palette mr-2"></i>그림 그리기</div>
                        <div class="hobby-badge"><i class="fas fa-mountain mr-2"></i>클라이밍</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body></html>
"""

# 3번 슬라이드 (MBTI)
mbti_slide_body_html = """
<!DOCTYPE html><html lang="ko"><head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>박민수 - MBTI</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; padding: 0; font-family: 'Noto Sans KR', sans-serif; }
        .slide-container { width: 100%; height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); position: relative; padding: 2rem; box-sizing: border-box; display: flex; align-items: center; justify-content: center; }
        .main-title { font-weight: 700; font-size: 4.5rem; text-align: center; margin-bottom: 1.5rem; color: white; text-shadow: 2px 2px 8px rgba(30, 27, 46, 0.5); }
        .content-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(15px); border-radius: 20px; display: flex; flex-direction: column; padding: 1.5rem; animation: slideUp 0.8s ease-out forwards; opacity: 0; transform: translateY(30px); }
        @keyframes slideUp { to { transform: translateY(0); opacity: 1; } }
        .keyword-badge { background: linear-gradient(135deg, #ff9a9e, #fecfef); color: #444; padding: 0.75rem 1.5rem; border-radius: 25px; font-weight: 600; margin: 0.5rem; display: inline-flex; align-items: center; box-shadow: 0 4px 15px rgba(255, 154, 158, 0.3); }
        .mbti-component { background: linear-gradient(135deg, #a8edea, #fed6e3); padding: 1rem; border-radius: 15px; text-align: center; box-shadow: 0 4px 15px rgba(168, 237, 234, 0.3); height:100%; }
        .mbti-letter { font-size: 2.5rem; font-weight: 900; color: #4a5568; margin-bottom: 0.5rem; }
        .comparison-table { background: rgba(255, 255, 255, 0.9); border-radius: 15px; overflow: hidden; height: 100%; }
        .table-header { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 1rem; font-weight: 700; text-align: center; }
        .table-content { padding: 1.5rem; }
        .strength-item, .development-item { display: flex; align-items: center; margin-bottom: 0.75rem; padding: 0.5rem; border-radius: 8px; }
        .field-badge { background: linear-gradient(135deg, #84fab0, #8fd3f4); color: #444; padding: 0.75rem 1.25rem; border-radius: 20px; font-weight: 600; margin: 0.25rem; display: inline-block; box-shadow: 0 3px 12px rgba(132, 250, 176, 0.3); }
        .section-title { color: #4a5568; font-weight: 700; font-size: 1.25rem; margin-bottom: 1rem; display: flex; align-items: center; }
        .icon-container { background: linear-gradient(135deg, #667eea, #764ba2); color: white; width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 0.75rem; }
    </style>
</head><body>
    <div class="slide-container">
        <div class="relative z-10" style="width:100%; max-width: 1200px;">
            <h1 class="main-title">INTJ</h1>
            <div class="content-card p-6 mb-6">
                <h2 class="section-title"><div class="icon-container"><i class="fas fa-star"></i></div>핵심 키워드</h2>
                <div class="text-center">
                    <div class="keyword-badge"><i class="fas fa-lightbulb mr-2"></i>논리적</div><div class="keyword-badge"><i class="fas fa-chart-line mr-2"></i>전략적</div><div class="keyword-badge"><i class="fas fa-brain mr-2"></i>분석적</div><div class="keyword-badge"><i class="fas fa-bullseye mr-2"></i>목표지향적</div><div class="keyword-badge"><i class="fas fa-tools mr-2"></i>독창적</div>
                </div>
            </div>
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="content-card p-6">
                    <h2 class="section-title"><div class="icon-container"><i class="fas fa-puzzle-piece"></i></div>구성요소</h2>
                    <div class="grid grid-cols-2 gap-3">
                        <div class="mbti-component"><div class="mbti-letter">I</div><div class="text-sm font-semibold">내향형</div></div><div class="mbti-component"><div class="mbti-letter">N</div><div class="text-sm font-semibold">직관형</div></div><div class="mbti-component"><div class="mbti-letter">T</div><div class="text-sm font-semibold">사고형</div></div><div class="mbti-component"><div class="mbti-letter">J</div><div class="text-sm font-semibold">판단형</div></div>
                    </div>
                </div>
                <div class="content-card p-0">
                    <div class="comparison-table">
                        <div class="table-header"><i class="fas fa-balance-scale mr-2"></i>강점 & 발전영역</div>
                        <div class="table-content">
                            <div class="mb-4"><h4 class="font-bold text-green-600 mb-2"><i class="fas fa-thumbs-up mr-1"></i>주요 강점</h4><div class="strength-item"><i class="fas fa-check-circle text-green-500 mr-2"></i><span class="text-sm">높은 독립성</span></div><div class="strength-item"><i class="fas fa-check-circle text-green-500 mr-2"></i><span class="text-sm">분석적 사고</span></div><div class="strength-item"><i class="fas fa-check-circle text-green-500 mr-2"></i><span class="text-sm">문제 해결 능력</span></div></div>
                            <div><h4 class="font-bold text-orange-600 mb-2"><i class="fas fa-arrow-up mr-1"></i>발전 영역</h4><div class="development-item"><i class="fas fa-exclamation-triangle text-orange-500 mr-2"></i><span class="text-sm">감정 표현</span></div><div class="development-item"><i class="fas fa-exclamation-triangle text-orange-500 mr-2"></i><span class="text-sm">사회적 교류</span></div></div>
                        </div>
                    </div>
                </div>
                <div class="content-card p-6">
                    <h2 class="section-title"><div class="icon-container"><i class="fas fa-code"></i></div>적합한 개발 분야</h2>
                    <div class="text-center flex-grow flex flex-col justify-center">
                        <div class="field-badge"><i class="fas fa-database mr-2"></i>데이터 과학/AI</div><div class="field-badge"><i class="fas fa-sitemap mr-2"></i>시스템 설계</div><div class="field-badge"><i class="fas fa-server mr-2"></i>백엔드 개발</div><div class="field-badge"><i class="fas fa-cogs mr-2"></i>알고리즘 최적화</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body></html>
"""

# 직업가치관 페이지 HTML 템플릿
job_values_html_template = """
<!DOCTYPE html><html lang="ko"><head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>직업가치관 검사</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { margin: 0; padding: 0; font-family: 'Noto Sans KR', sans-serif; }
        .slide-container { width: 100%; height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); position: relative; padding: 2rem; box-sizing: border-box; display: flex; align-items: center; justify-content: center; }
        .main-title { color: #e9e7f5; font-weight: 700; font-size: 3rem; text-align: center; margin-bottom: 1.5rem; }
        .content-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(15px); border-radius: 20px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); animation: slideUp 0.8s ease-out forwards; opacity: 0; transform: translateY(30px); }
        @keyframes slideUp { to { transform: translateY(0); opacity: 1; } }
        .main-grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 1.5rem; }
        .chart-container { height: 350px; position: relative; padding: 1rem;}
        .value-item { display: flex; align-items: center; justify-content: space-between; padding: 0.75rem; margin-bottom: 0.5rem; border-radius: 10px; font-size: 0.9rem; }
        .top-value { background: linear-gradient(135deg, #10b981, #059669); color: white; }
        .bottom-value { background: linear-gradient(135deg, #f59e0b, #d97706); color: white; }
        .score-badge { background: rgba(255, 255, 255, 0.3); padding: 0.25rem 0.75rem; border-radius: 15px; font-weight: 700; font-size: 0.85rem; }
        .job-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; }
        .job-badge { background: linear-gradient(135deg, #84fab0, #8fd3f4); color: #374151; padding: 0.5rem 0.75rem; border-radius: 15px; font-weight: 600; font-size: 0.8rem; text-align: center; box-shadow: 0 3px 12px rgba(132, 250, 176, 0.3); }
        .insight-text { color: #4a5568; font-size: 1rem; line-height: 1.8; text-align:center; }
        .highlight { background: linear-gradient(135deg, #ff9a9e, #fecfef); color: #444; padding: 0.25rem 0.5rem; border-radius: 8px; font-weight: 600; }
        .section-title { color: #4a5568; font-weight: 700; font-size: 1.25rem; margin-bottom: 1rem; display: flex; align-items: center; }
        .icon-container { background: linear-gradient(135deg, #667eea, #764ba2); color: white; width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 0.75rem; }
    </style>
</head><body>
    <div class="slide-container">
        <div class="relative z-10" style="width:100%; max-width: 1200px;">
            <h1 class="main-title">직업가치관 검사 결과</h1>
            <div class="main-grid">
                <div class="content-card p-6"><h2 class="section-title"><div class="icon-container"><i class="fas fa-chart-pie"></i></div>가치관 분석 차트</h2><div class="chart-container">__CHART_AREA__</div></div>
                <div class="space-y-4">
                    <div class="content-card p-4"><h2 class="section-title"><div class="icon-container"><i class="fas fa-trophy"></i></div>상위 가치관</h2>__TOP_VALUES_HTML__</div>
                    <div class="content-card p-4"><h2 class="section-title"><div class="icon-container"><i class="fas fa-arrow-down"></i></div>하위 가치관</h2>__BOTTOM_VALUES_HTML__</div>
                </div>
            </div>
            <div class="content-card p-6 mt-6">
                <h2 class="section-title justify-center"><div class="icon-container"><i class="fas fa-briefcase"></i></div>추천 직업 분야</h2>
                <div class="job-grid mb-4">
                    <div class="job-badge"><i class="fas fa-shield-alt mr-1"></i>산업안전원</div><div class="job-badge"><i class="fas fa-flask mr-1"></i>자연과학연구원</div><div class="job-badge"><i class="fas fa-balance-scale mr-1"></i>법무사</div><div class="job-badge"><i class="fas fa-user-tie mr-1"></i>정부행정관리자</div><div class="job-badge"><i class="fas fa-microscope mr-1"></i>환경시험원</div><div class="job-badge"><i class="fas fa-map mr-1"></i>GIS전문가</div>
                </div>
                <div class="insight-text mt-4">
                    <p>
                        <span class="highlight">__INSIGHT_TEXT__</span>
                    </p>
                </div>
            </div>
        </div>
    </div>
</body></html>
"""

# 직무역량 페이지 HTML 템플릿
competency_html_template = """
<!DOCTYPE html><html lang="ko"><head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>직무역량 분석</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { margin: 0; padding: 0; font-family: 'Noto Sans KR', sans-serif; }
        .slide-container { width: 100%; height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); position: relative; padding: 2rem; box-sizing: border-box; display: flex; align-items: center; justify-content: center; }
        .main-title { color: #e9e7f5; font-weight: 700; font-size: 3rem; text-align: center; margin-bottom: 1.5rem; }
        .content-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(15px); border-radius: 20px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); animation: slideUp 0.8s ease-out forwards; opacity: 0; transform: translateY(30px); }
        @keyframes slideUp { to { transform: translateY(0); opacity: 1; } }
        .main-grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 1.5rem; }
        .chart-container { height: 300px; position: relative; padding: 1rem;}
        .competency-item { display: flex; align-items: center; margin-bottom: 0.75rem; padding: 0.75rem; border-radius: 10px; font-size: 0.9rem; color: white;}
        .strength-item { background: linear-gradient(135deg, #10b981, #059669); }
        .development-item { background: linear-gradient(135deg, #f59e0b, #d97706); }
        .score-badge { background: rgba(255, 255, 255, 0.3); padding: 0.25rem 0.75rem; border-radius: 15px; font-weight: 700; font-size: 0.85rem; margin-left: auto; }
        .insight-text { color: #4a5568; font-size: 1rem; line-height: 1.8; text-align:center;}
        .highlight { background: linear-gradient(135deg, #ff9a9e, #fecfef); color: #444; padding: 0.25rem 0.5rem; border-radius: 8px; font-weight: 600; }
        .competency-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 1rem; }
        .competency-badge { background: linear-gradient(135deg, #84fab0, #8fd3f4); color: #374151; padding: 0.5rem 1rem; border-radius: 15px; font-weight: 600; font-size: 0.85rem; text-align: center; box-shadow: 0 3px 12px rgba(132, 250, 176, 0.3); }
        .section-title { color: #4a5568; font-weight: 700; font-size: 1.25rem; margin-bottom: 1rem; display: flex; align-items: center; }
        .icon-container { background: linear-gradient(135deg, #667eea, #764ba2); color: white; width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 0.75rem; }
    </style>
</head><body>
    <div class="slide-container">
        <div class="relative z-10" style="width:100%; max-width: 1200px;">
            <h1 class="main-title">직무역량 분석</h1>
            <div class="main-grid">
                <div class="content-card p-6"><h2 class="section-title"><div class="icon-container"><i class="fas fa-chart-pie"></i></div>역량 분포 차트</h2><div class="chart-container">__CHART_AREA__</div></div>
                <div class="space-y-4">
                    <div class="content-card p-4"><h2 class="section-title"><div class="icon-container"><i class="fas fa-star"></i></div>핵심 강점</h2>__STRENGTHS_HTML__</div>
                    <div class="content-card p-4"><h2 class="section-title"><div class="icon-container"><i class="fas fa-arrow-up"></i></div>보완 영역</h2>__DEVELOPMENT_AREAS_HTML__</div>
                </div>
            </div>
            <div class="content-card p-6 mt-6">
                <h2 class="section-title justify-center"><div class="icon-container"><i class="fas fa-chart-line"></i></div>종합 분석 및 발전 방향</h2>
                <div class="competency-grid mb-4">
                    <div class="competency-badge"><i class="fas fa-cogs mr-2"></i>복잡한 문제 해결</div><div class="competency-badge"><i class="fas fa-project-diagram mr-2"></i>시스템적 사고</div><div class="competency-badge"><i class="fas fa-handshake mr-2"></i>소통 역량 개발</div><div class="competency-badge"><i class="fas fa-balance-scale mr-2"></i>감정 관리 기술</div>
                </div>
                <div class="insight-text mt-4">
                    <p>
                        <span class="highlight">__INSIGHT_TEXT__</span>
                    </p>
                </div>
            </div>
        </div>
    </div>
</body></html>
"""


# --- 사이드바 및 페이지 렌더링 로직 ---

st.sidebar.title("📑 발표 목차")
page_options = ["🏠 홈", "1. 기본 소개", "2. 성격유형(MBTI)", "3. 직업가치관 검사", "4. 직무역량 분석"]
selected_page = st.sidebar.radio("이동할 페이지를 선택하세요:", page_options)


if selected_page == "🏠 홈":
    components.html(home_slide_html, height=1050, scrolling=True)
elif selected_page == "1. 기본 소개":
    components.html(intro_slide_html, height=1050, scrolling=True)
elif selected_page == "2. 성격유형(MBTI)":
    components.html(mbti_slide_body_html, height=1050, scrolling=True)

# --- 직업가치관 페이지 (인터랙티브) ---
elif selected_page == "3. 직업가치관 검사":
    with st.expander("📊 직업가치관 데이터 편집"):
        cols = st.columns(3)
        for i, (label, value) in enumerate(st.session_state.job_values.items()):
            with cols[i % 3]:
                st.session_state.job_values[label] = st.slider(label, 0.0, 5.0, value, 0.1, key=f"job_{label}")

    st.write("---")
    cols = st.columns(3)
    if cols[0].button("📊 레이더 차트", key="job_radar", use_container_width=True): st.session_state.job_chart_type = '레이더 차트'
    if cols[1].button("📊 막대 차트", key="job_bar", use_container_width=True): st.session_state.job_chart_type = '막대 차트'
    if cols[2].button("📝 데이터 표", key="job_table", use_container_width=True): st.session_state.job_chart_type = '데이터 표'
    
    values = st.session_state.job_values
    labels = list(values.keys())
    data_points = list(values.values())
    df = pd.DataFrame(list(values.items()), columns=['가치관', '점수'])
    top_3 = df.nlargest(3, '점수')
    bottom_3 = df.nsmallest(3, '점수').sort_values(by='점수', ascending=False)
    
    top_html = "".join([f'<div class="top-value value-item"><span><i class="fas fa-medal mr-2"></i>{row["가치관"]}</span><span class="score-badge">{row["점수"]:.1f}</span></div>' for _, row in top_3.iterrows()])
    bottom_html = "".join([f'<div class="bottom-value value-item"><span><i class="fas fa-hand-holding-heart mr-2"></i>{row["가치관"]}</span><span class="score-badge">{row["점수"]:.1f}</span></div>' for _, row in bottom_3.iterrows()])
    insight = f'{top_3.iloc[0]["가치관"]}, {top_3.iloc[1]["가치관"]} 등을 중시하며, 안정적인 환경을 선호합니다.'

    chart_area_html = ""
    chart_type = st.session_state.job_chart_type
    if chart_type == '레이더 차트':
        chart_area_html = f"""
            <canvas id="valueChart"></canvas>
            <script>
                if (window.myJobChart) window.myJobChart.destroy();
                window.myJobChart = new Chart(document.getElementById('valueChart'), {{
                    type: 'radar',
                    data: {{ labels: {json.dumps(labels)}, datasets: [{{ data: {data_points}, backgroundColor: 'rgba(102, 126, 234, 0.2)', borderColor: 'rgba(102, 126, 234, 1)', borderWidth: 3, pointRadius: 5 }}] }},
                    options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ r: {{ beginAtZero: true, max: 5, pointLabels: {{ font: {{ size: 12 }} }} }} }} }}
                }});
            </script>
        """
    elif chart_type == '막대 차트':
        chart_area_html = f"""
            <canvas id="valueChart"></canvas>
            <script>
                if (window.myJobChart) window.myJobChart.destroy();
                window.myJobChart = new Chart(document.getElementById('valueChart'), {{
                    type: 'bar',
                    data: {{ labels: {json.dumps(labels)}, datasets: [{{ data: {data_points}, backgroundColor: 'rgba(102, 126, 234, 0.6)' }}] }},
                    options: {{ responsive: true, maintainAspectRatio: false, indexAxis: 'y', plugins: {{ legend: {{ display: false }} }}, scales: {{ x: {{ beginAtZero: true, max: 5 }} }} }}
                }});
            </script>
        """
    elif chart_type == '데이터 표':
        table_html = '<div style="overflow-y:auto;height:350px;"><table class="w-full text-left"><thead><tr class="border-b"><th class="p-2">가치관</th><th class="p-2 text-right font-bold">점수</th></tr></thead><tbody>'
        table_html += "".join([f'<tr class="border-b"><td class="p-2">{k}</td><td class="p-2 text-right font-bold">{v:.1f}</td></tr>' for k, v in sorted(values.items(), key=lambda item: item[1], reverse=True)])
        table_html += '</tbody></table></div>'
        chart_area_html = table_html

    final_html = job_values_html_template.replace('__CHART_AREA__', chart_area_html).replace('__TOP_VALUES_HTML__', top_html).replace('__BOTTOM_VALUES_HTML__', bottom_html).replace('__INSIGHT_TEXT__', insight)
    components.html(final_html, height=1050, scrolling=True)

# --- 직무역량 페이지 (인터랙티브) ---
elif selected_page == "4. 직무역량 분석":
    with st.expander("📊 직무역량 데이터 편집"):
        cols = st.columns(3)
        for i, (label, value) in enumerate(st.session_state.competency_values.items()):
            with cols[i % 2]: # 2열로 배치
                st.session_state.competency_values[label] = st.slider(label, 0, 100, value, 1, key=f"comp_{label}")

    st.write("---")
    cols = st.columns(3)
    if cols[0].button("📊 레이더 차트", key="comp_radar", use_container_width=True): st.session_state.competency_chart_type = '레이더 차트'
    if cols[1].button("📊 막대 차트", key="comp_bar", use_container_width=True): st.session_state.competency_chart_type = '막대 차트'
    if cols[2].button("📝 데이터 표", key="comp_table", use_container_width=True): st.session_state.competency_chart_type = '데이터 표'

    values = st.session_state.competency_values
    labels = list(values.keys())
    data_points = list(values.values())
    df = pd.DataFrame(list(values.items()), columns=['역량', '점수'])
    strengths = df[df['점수'] >= 80]
    dev_areas = df[df['점수'] < 80].sort_values(by='점수', ascending=False)

    strengths_html = "".join([f'<div class="strength-item competency-item"><span><i class="fas fa-brain mr-2"></i>{row["역량"]}</span><span class="score-badge">{row["점수"]}</span></div>' for _, row in strengths.iterrows()])
    dev_areas_html = "".join([f'<div class="development-item competency-item"><span><i class="fas fa-users mr-2"></i>{row["역량"]}</span><span class="score-badge">{row["점수"]}</span></div>' for _, row in dev_areas.iterrows()])
    
    insight = "핵심 강점과 보완점을 파악하여 지속적으로 성장하는 개발자가 되겠습니다."
    if not strengths.empty:
        insight = f'{strengths.iloc[0]["역량"]}, {strengths.iloc[1]["역량"]} 역량이 뛰어나며, {dev_areas.iloc[0]["역량"]} 역량을 보완하면 좋습니다.' if len(strengths) > 1 and not dev_areas.empty else f'{strengths.iloc[0]["역량"]} 역량이 뛰어납니다.'

    chart_area_html = ""
    chart_type = st.session_state.competency_chart_type
    if chart_type == '레이더 차트':
        chart_area_html = f"""
            <canvas id="competencyChart"></canvas>
            <script>
                if (window.myCompChart) window.myCompChart.destroy();
                window.myCompChart = new Chart(document.getElementById('competencyChart'), {{
                    type: 'radar', data: {{ labels: {json.dumps(labels)}, datasets: [{{ data: {data_points}, backgroundColor:'rgba(255,154,158,0.2)', borderColor:'rgba(255,154,158,1)', borderWidth:3 }}] }},
                    options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend:{{display:false}} }}, scales: {{ r: {{ beginAtZero:true, max:100, pointLabels:{{font:{{size:12}} }} }} }} }}
                }});
            </script>
        """
    elif chart_type == '막대 차트':
        chart_area_html = f"""
            <canvas id="competencyChart"></canvas>
            <script>
                if (window.myCompChart) window.myCompChart.destroy();
                window.myCompChart = new Chart(document.getElementById('competencyChart'), {{
                    type: 'bar', data: {{ labels: {json.dumps(labels)}, datasets: [{{ data: {data_points}, backgroundColor:'rgba(255,154,158,0.6)' }}] }},
                    options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend:{{display:false}} }}, scales: {{ y: {{ beginAtZero:true, max:100 }} }} }}
                }});
            </script>
        """
    elif chart_type == '데이터 표':
        table_html = '<div style="overflow-y:auto;height:300px;"><table class="w-full text-left"><thead><tr class="border-b"><th class="p-2">역량</th><th class="p-2 text-right font-bold">점수</th></tr></thead><tbody>'
        table_html += "".join([f'<tr class="border-b"><td class="p-2">{k}</td><td class="p-2 text-right font-bold">{v}</td></tr>' for k, v in sorted(values.items(), key=lambda item: item[1], reverse=True)])
        table_html += '</tbody></table></div>'
        chart_area_html = table_html

    final_html = competency_html_template.replace('__CHART_AREA__', chart_area_html).replace('__STRENGTHS_HTML__', strengths_html).replace('__DEVELOPMENT_AREAS_HTML__', dev_areas_html).replace('__INSIGHT_TEXT__', insight)
    components.html(final_html, height=1050, scrolling=True)