import json
import pathlib

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Paper Navi", layout="wide")

# Streamlit 기본 UI 를 제거하고 컴포넌트 iframe 이 화면 전체를 채우게 함
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

BASE_DIR = pathlib.Path(__file__).parent

# ---------------------------------------------------------------------------
# 원본 index.html / results.html 은 두 개의 정적 페이지로,
#   - index.html   : location.href = 'results.html?keyword=...' 로 이동
#   - results.html : URLSearchParams(location.search) 로 keyword 를 읽음
# 하지만 Streamlit 컴포넌트 iframe 의 sandbox 에는 allow-top-navigation 이 없고,
# srcdoc iframe 에는 'results.html' 이라는 실제 파일도 존재하지 않아서
# 페이지 간 이동이 불가능하다.
#
# 그래서 하나의 바깥 iframe(라우터) 안에 안쪽 iframe 을 두고, 두 페이지 HTML 을
# 모두 담아 둔 뒤 srcdoc 을 바꿔 끼우는 방식으로 "제자리 이동"을 구현한다.
# 안쪽 iframe 은 바깥 라우터와 동일 출처(srcdoc 상속)이므로 parent 함수 호출이
# 허용되고(allow-same-origin), 이는 top-navigation 이 아니라서 sandbox 에도 걸리지
# 않는다. 덕분에 원본 HTML 의 이동 코드만 라우터 호출로 바꿔주면 그대로 동작한다.
# ---------------------------------------------------------------------------

NAV_SNIPPET = "location.href = 'results.html?keyword=' + encodeURIComponent(kw);"
KEYWORD_READ_SNIPPET = "(params.get('keyword') || '').trim();"
LOGO_LINK_SNIPPET = 'href="index.html"'
KW_TOKEN = "%%NAVI_KW%%"


def load(name: str) -> str:
    return (BASE_DIR / name).read_text(encoding="utf-8")


def embed(s: str) -> str:
    # JS 문자열 리터럴로 안전하게 삽입: 따옴표 이스케이프(json) + </script 조기 종료 방지
    return json.dumps(s).replace("</", "<\\/")


# index.html: 검색 이동을 라우터 호출로 대체
index_html = load("index.html").replace(NAV_SNIPPET, "parent.__naviGo('results', kw);")

# results.html: keyword 값은 라우터가 srcdoc 교체 시점에 토큰으로 주입, 이동은 라우터 호출로 대체
results_html = load("results.html")
results_html = results_html.replace(
    KEYWORD_READ_SNIPPET,
    '(decodeURIComponent("' + KW_TOKEN + '") || \'\').trim();',
)
results_html = results_html.replace(NAV_SNIPPET, "parent.__naviGo('results', kw);")
results_html = results_html.replace(
    LOGO_LINK_SNIPPET,
    'href="javascript:void(0)" onclick="return parent.__naviHome()"',
)

router = (
    '<!doctype html><html><head><meta charset="utf-8">'
    "<style>html,body{margin:0;padding:0;height:100%;overflow:hidden}"
    "#page{border:0;width:100%;height:100vh;display:block}</style>"
    '</head><body><iframe id="page"></iframe><script>'
    "var __PAGES = { index: " + embed(index_html) + ", results: " + embed(results_html) + " };"
    'var __frame = document.getElementById("page");'
    "window.__naviGo = function(page, kw){"
    "  var html = __PAGES[page] || __PAGES.index;"
    '  if (page === "results") html = html.replace("' + KW_TOKEN + '", encodeURIComponent(kw || ""));'
    "  __frame.srcdoc = html;"
    "};"
    'window.__naviHome = function(){ window.__naviGo("index",""); return false; };'
    'window.__naviGo("index","");'
    "</script></body></html>"
)

components.html(router, height=800, scrolling=False)
