import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Paper Navi", layout="wide")

# Streamlit 기본 UI(헤더/여백/메뉴/푸터)를 모두 제거하고,
# 정적 페이지를 담은 iframe 이 화면 전체를 채우도록 고정한다.
st.markdown(
    """
    <style>
      [data-testid="stAppViewContainer"],
      [data-testid="stMain"],
      .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
      header[data-testid="stHeader"], footer, #MainMenu { display: none !important; }
      iframe {
        position: fixed;
        inset: 0;
        width: 100vw !important;
        height: 100vh !important;
        border: none;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# index.html -> results.html 이동은 정적 파일 서빙(app/static/*) 위에서
# iframe 이 "자기 자신"을 이동시키는 방식으로 브라우저가 그대로 처리한다.
#
# Streamlit 컴포넌트 iframe 의 sandbox 에는 allow-top-navigation 이 없어서
# 부모(Streamlit) 창을 바꾸는 방식은 막히지만, iframe 내부의 동일 출처 이동은
# 허용되므로 원본 HTML 의 location.href / URLSearchParams(location.search) 가
# 아무 수정 없이 그대로 동작한다.
components.iframe("app/static/index.html", height=800, scrolling=True)
