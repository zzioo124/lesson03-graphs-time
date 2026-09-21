import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("1년 치 일별 박스오피스 데이터를 바탕으로 시간에 따른 영화 흥행 추이를 살펴봅니다.")
st.divider()

# 2. 데이터 불러오기 및 전처리 (캐싱을 사용하여 속도 향상)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # '날짜' 열을 문자열로 바꾼 뒤 진짜 날짜(datetime) 데이터로 변환 (예: 20230101 -> 2023-01-01)
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# ==========================================
# [구역 1] 특정 영화의 일별 관객수 변화
# ==========================================
st.header("📍 1. 특정 영화의 일별 관객수 변화")

# 드롭다운을 위한 영화 목록 추출 (가나다 순 정렬)
movie_list = sorted(df['영화명'].unique())

# 영화 선택 드롭다운
selected_movie = st.selectbox("그래프를 확인할 영화를 선택하세요:", movie_list)

# 선택한 영화 데이터만 필터링
movie_df = df[df['영화명'] == selected_movie]

if not movie_df.empty:
    # Plotly 선 그래프 생성
    fig1 = px.line(
        movie_df, 
        x='날짜', 
        y='일관객', 
        title=f"'{selected_movie}' 일별 관객수 추이",
        markers=True,
        labels={'일관객': '일일 관객수(명)', '날짜': '상영 날짜'}
    )
    
    # 마우스 오버(hover) 시 보여줄 정보 설정
    fig1.update_traces(hovertemplate='<b>날짜:</b> %{x}<br><b>관객수:</b> %{y:,}명<extra></extra>')
    
    # 그래프 출력
    st.plotly_chart(fig1, use_container_width=True)
    
    # 알 수 있는 것 문구 자리
    st.info("💡 **이 그래프로 알 수 있는 것:** (예시: 개봉 첫 주말에 관객이 가장 많이 몰리며, 이후 점진적으로 하락하는 추세를 보인다.)")

else:
    st.warning("해당 영화의 데이터가 없습니다.")

st.divider()

# ==========================================
# [구역 2] (앞으로 추가할 그래프 자리)
# ==========================================
st.header("📍 2. (다음 그래프 제목을 입력하세요)")
st.write("이곳에 새로운 데이터를 분석하는 그래프와 위젯을 추가할 수 있습니다.")

# 향후 추가될 코드를 위한 임시 공간
# ...

st.info("💡 **이 그래프로 알 수 있는 것:** (분석 내용을 적어주세요)")
