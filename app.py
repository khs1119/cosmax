import json
import pathlib

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Paper Navi", layout="wide")

# Streamlit 기본 여백/헤더를 제거해서 원본 HTML 앱이 화면을 그대로 채우도록 함
st.markdown(
    """
    <style>
      .block-container { padding: 0 !important; max-width: 100% !important; }
      header[data-testid="stHeader"] { display: none; }
      #MainMenu { visibility: hidden; }
      footer { visibility: hidden; }
      iframe { border: none; display: block; }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = pathlib.Path(__file__).parent

# 원본 index.html / results.html 은 두 개의 정적 페이지이며
#   - index.html    : location.href = 'results.html?keyword=...' 로 이동
#   - results.html  : URLSearchParams(location.search) 로 keyword 를 읽음
# 하지만 Streamlit 의 components.html 은 샌드박스 iframe(srcdoc) 안에서 실행되므로
# 위 방식(별도 파일로의 이동, iframe 자체의 쿼리스트링 읽기)이 동작하지 않는다.
#
# 그래서 여기서 두 페이지를 Streamlit 의 쿼리 파라미터(?keyword=...)로 라우팅한다.
#   - keyword 가 있으면 결과 페이지(results.html)
#   - 없으면 검색 랜딩 페이지(index.html)
# iframe 안의 이동/키워드 읽기는 아래 문자열 치환으로 부모(Streamlit) URL 과 이어준다.

# iframe 안의 검색 이동을 부모(Streamlit) 페이지의 쿼리 파라미터로 승격시키는 헬퍼.
# srcdoc iframe 은 부모와 동일 출처를 상속하므로 window.parent.location 접근이 가능하다.
NAVI_BRIDGE = """
<script>
  window.__naviGo = function (kw) {
    var target = window.parent || window;
    var qs = kw ? ('?keyword=' + encodeURIComponent(kw)) : '';
    try {
      target.location.search = qs;
    } catch (e) {
      // 부모 접근이 막힌 경우(예: 크로스오리진) 최소한 현재 창이라도 이동
      window.location.search = qs;
    }
  };
  window.__naviHome = function () {
    window.__naviGo('');
    return false;
  };
</script>
"""

# 원본 JS 안의 페이지 이동 코드. index.html 과 results.html 에서 동일한 문자열을 쓴다.
NAV_SNIPPET = "location.href = 'results.html?keyword=' + encodeURIComponent(kw);"

# results.html 이 keyword 를 읽는 부분(iframe 자체의 location.search 는 비어 있으므로 값 주입)
KEYWORD_READ_SNIPPET = "(params.get('keyword') || '').trim();"

# 결과 페이지 로고의 '홈으로' 링크 (별도 파일 이동 → 부모 URL 초기화로 대체)
LOGO_LINK_SNIPPET = 'href="index.html"'


def prepare_html(html: str, keyword: str) -> str:
    # 부모 URL 로 이동을 승격시키는 브릿지 스크립트를 <head> 최상단에 주입
    html = html.replace("<head>", "<head>" + NAVI_BRIDGE, 1)

    # iframe 안의 이동을 부모(Streamlit) 쿼리 파라미터 갱신으로 대체
    html = html.replace(NAV_SNIPPET, "window.__naviGo(kw);")

    # 로고 '홈' 링크 → 쿼리 파라미터 초기화
    html = html.replace(
        LOGO_LINK_SNIPPET,
        'href="javascript:void(0)" onclick="return window.__naviHome()"',
    )

    # 결과 페이지에는 서버가 정한 keyword 값을 직접 주입
    html = html.replace(
        KEYWORD_READ_SNIPPET,
        "(" + json.dumps(keyword) + " || '').trim();",
    )
    return html


raw_keyword = st.query_params.get("keyword", "")
if isinstance(raw_keyword, list):
    raw_keyword = raw_keyword[0] if raw_keyword else ""
keyword = (raw_keyword or "").strip()

if keyword:
    html_path = BASE_DIR / "results.html"
    height = 3200
else:
    html_path = BASE_DIR / "index.html"
    height = 1500

html = prepare_html(html_path.read_text(encoding="utf-8"), keyword)
components.html(html, height=height, scrolling=True)
