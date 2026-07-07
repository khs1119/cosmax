import streamlit as st
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="페이퍼 나비 | Paper Navi",
    page_icon="🦋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바 네비게이션
st.sidebar.title("🦋 페이퍼 나비")
page = st.sidebar.radio(
    "페이지 선택",
    ["홈", "탐색 결과"],
    label_visibility="collapsed"
)

# CSS 스타일 (라이트/다크 테마 지원)
st.markdown("""
<style>
:root {
    --primary: #2563eb;
    --primary-hover: #1d4ed8;
    --bg: #ffffff;
    --bg-alt: #f8fafc;
    --fg: #0f172a;
    --text-muted: #475569;
    --border: #e2e8f0;
    --icon-bg: #eff6ff;
}

body {
    font-family: "Pretendard", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.main-header {
    text-align: center;
    padding: 60px 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 12px;
    margin-bottom: 40px;
}

.main-header h1 {
    font-size: 48px;
    font-weight: 700;
    margin: 0 0 10px 0;
}

.main-header p {
    font-size: 18px;
    opacity: 0.95;
    margin: 10px 0;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin: 40px 0;
}

.feature-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 24px;
    transition: all 0.3s ease;
}

.feature-card:hover {
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    border-color: #2563eb;
}

.feature-icon {
    font-size: 32px;
    margin-bottom: 12px;
}

.feature-card h3 {
    color: #0f172a;
    margin: 12px 0;
    font-size: 18px;
}

.feature-card p {
    color: #475569;
    font-size: 14px;
    line-height: 1.6;
    margin: 0;
}

.search-box {
    display: flex;
    gap: 12px;
    margin: 30px 0;
    flex-wrap: wrap;
}

.input-field {
    flex: 1;
    min-width: 250px;
    padding: 12px 16px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    font-size: 14px;
}

.btn-primary {
    padding: 12px 24px;
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.3s ease;
}

.btn-primary:hover {
    background: #1d4ed8;
}

.results-container {
    margin-top: 40px;
}

.result-item {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    transition: all 0.3s ease;
}

.result-item:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.result-title {
    color: #2563eb;
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 8px 0;
    text-decoration: none;
}

.result-url {
    color: #10b981;
    font-size: 12px;
    margin-bottom: 8px;
}

.result-snippet {
    color: #475569;
    font-size: 14px;
    line-height: 1.6;
    margin: 8px 0;
}

.tags {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 12px;
}

.tag {
    background: #eff6ff;
    color: #2563eb;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
}

.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #475569;
}

.empty-state-icon {
    font-size: 48px;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

# 홈 페이지
if page == "홈":
    st.markdown("""
    <div class="main-header">
        <h1>🦋 페이퍼 나비</h1>
        <p>Paper Navi — 연구의 지도를 그리다</p>
        <p style="font-size: 14px; opacity: 0.9;">AI 기반 논문 탐색 및 분석 플랫폼</p>
    </div>
    """, unsafe_allow_html=True)

    # 검색 박스
    col1, col2 = st.columns([4, 1])
    with col1:
        search_query = st.text_input(
            "검색어를 입력하세요",
            placeholder="예: 머신러닝, 자연어 처리, ...",
            label_visibility="collapsed"
        )
    with col2:
        search_button = st.button("🔍 검색", use_container_width=True)

    if search_button and search_query:
        st.session_state.search_query = search_query
        st.switch_page("pages/results.py")

    # 특징
    st.markdown("""
    <h2 style="text-align: center; color: #0f172a; margin-top: 50px; margin-bottom: 30px;">주요 기능</h2>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <h3>포괄적 검색</h3>
            <p>수백만 개의 논문 중에서 당신의 연구 주제와 관련된 논문을 빠르게 찾아보세요.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔬</div>
            <h3>지능형 분석</h3>
            <p>AI를 활용하여 논문의 핵심 내용과 연구 동향을 자동으로 분석합니다.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🗺️</div>
            <h3>연구 지도</h3>
            <p>논문 간의 관계를 시각화하여 연구 분야의 전체 맥락을 파악할 수 있습니다.</p>
        </div>
        """, unsafe_allow_html=True)

    # 추가 정보
    st.markdown("---")
    st.markdown("""
    ## 🚀 시작하기

    1. **검색**: 위의 검색창에서 관심 있는 주제를 입력하세요
    2. **탐색**: 검색 결과에서 관련 논문들을 확인하세요
    3. **분석**: 각 논문의 상세 정보와 인사이트를 얻으세요

    ## 💡 팁

    - 더 정확한 결과를 원한다면 구체적인 키워드를 사용하세요
    - 필터를 활용하여 특정 연도나 분야의 논문만 볼 수 있습니다
    - 관심 있는 논문을 저장하여 나중에 비교할 수 있습니다
    """)

# 탐색 결과 페이지
elif page == "탐색 결과":
    st.title("🔍 탐색 결과")

    if "search_query" not in st.session_state:
        st.info("🔍 홈 페이지에서 검색어를 입력해주세요.")
    else:
        search_query = st.session_state.search_query

        # 필터
        col1, col2, col3 = st.columns(3)
        with col1:
            year_filter = st.selectbox("연도", ["모든 연도", "2024", "2023", "2022", "2021"])
        with col2:
            field_filter = st.selectbox("분야", ["모든 분야", "머신러닝", "자연어 처리", "컴퓨터 비전", "기타"])
        with col3:
            sort_by = st.selectbox("정렬", ["관련도 순", "최신 순", "인용 수 순"])

        st.markdown(f"""
        <div style="background: #eff6ff; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
            <p style="margin: 0; color: #2563eb;"><strong>검색어:</strong> {search_query}</p>
            <p style="margin: 8px 0 0 0; color: #475569; font-size: 14px;">
                필터: {year_filter} | {field_filter} | {sort_by}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # 샘플 결과
        st.markdown("""
        <div class="results-container">
        """, unsafe_allow_html=True)

        # 예시 결과 아이템
        for i in range(5):
            st.markdown(f"""
            <div class="result-item">
                <h4 class="result-title">연구 논문 제목 {i+1}: {search_query}에 관한 심층 분석</h4>
                <p class="result-url">https://arxiv.org/abs/2024.{i+1:05d}</p>
                <p class="result-snippet">
                    본 논문은 {search_query}의 최신 발전 동향과 기술 방법론을 소개합니다. 
                    다양한 데이터셋에서의 실험 결과를 통해 제안한 방법의 효율성을 입증합니다.
                </p>
                <div class="tags">
                    <span class="tag">인용 수: 42</span>
                    <span class="tag">2024년 발행</span>
                    <span class="tag">관련도: 95%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # 페이지네이션
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown("<div style='text-align: center; color: #475569; margin-top: 20px;'>1 / 10 페이지</div>", unsafe_allow_html=True)
