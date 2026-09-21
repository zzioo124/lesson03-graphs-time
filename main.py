import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("일별 박스오피스 데이터를 바탕으로 시간에 따른 영화 관객 수의 흐름을 분석합니다.")
st.markdown("---")

# 2. 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # '날짜' 열을 YYYYMMDD 형식을 감안해 실제 Datetime 타입으로 변환
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    return df

df = load_data()


# ====================================================
# [구역 1] 개별 영화의 날짜별 일관객 변화
# ====================================================
st.header("1. 개별 영화의 일별 관객수 변화")
st.caption("드롭다운에서 특정 영화를 선택하여 상영 기간 동안의 일별 관객수 변화를 관찰합니다.")

# 영화 목록 추출 및 선택 드롭다운
movie_list = sorted(df['영화명'].unique())
selected_movie = st.selectbox("영화를 선택하세요:", movie_list)

# 선택된 영화 데이터 필터링
df_selected = df[df['영화명'] == selected_movie].sort_values('날짜')

if not df_selected.empty:
    fig1 = px.line(
        df_selected,
        x='날짜',
        y='일관객',
        title=f"[{selected_movie}] 일별 관객수 추이",
        labels={'날짜': '날짜', '일관객': '일관객 수 (명)'},
        markers=True
    )
    
    # 마우스 오버 시 날짜와 관객수 표시
    fig1.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,}명<extra></extra>"
    )
    fig1.update_layout(hovermode="x unified")
    
    st.plotly_chart(fig1, use_container_width=True)

# 그래프 분석 내용 작성 칸
st.info("💡 **이 그래프로 알 수 있는 것**: 특정 영화의 개봉 초기 관객 집중도, 주말/평일 간의 관객 차이, 그리고 장기 흥행 여부를 파악할 수 있습니다.")

st.markdown("---")


# ====================================================
# [구역 2] 총 관객수 TOP 5 영화의 일별 관객수 비교
# ====================================================
st.header("2. 총 관객수 TOP 5 영화의 일별 관객수 추이 비교")
st.caption("기간 내 전체 일관객 합계가 가장 큰 상위 5개 영화의 관객수 변화를 한 그래프에서 비교합니다. (범례를 클릭하여 영화를 켜고 끌 수 있습니다)")

# 기간 내 총 일관객 수가 가장 큰 5개 영화 추출
top5_movies = df.groupby('영화명')['일관객'].sum().nlargest(5).index.tolist()

# TOP 5 영화 데이터만 필터링
df_top5 = df[df['영화명'].isin(top5_movies)].sort_values('날짜')

fig2 = px.line(
    df_top5,
    x='날짜',
    y='일관객',
    color='영화명',
    title="기간 내 총 관객수 TOP 5 영화 일별 관객수 비교",
    labels={'날짜': '날짜', '일관객': '일관객 수 (명)', '영화명': '영화 제목'},
    markers=True
)

# 마우스 오버 포맷 지정
fig2.update_traces(
    hovertemplate="<b>영화:</b> %{fullData.name}<br><b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,}명<extra></extra>"
)
fig2.update_layout(
    hovermode="x unified",
    legend=dict(
        title="영화 목록 (클릭시 토글)",
        orientation="h",  # 범례를 가로로 배치 (선택 사항)
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(fig2, use_container_width=True)

# 그래프 분석 내용 작성 칸
st.info("💡 **이 그래프로 알 수 있는 것**: 가장 흥행한 5개 영화의 스크린 독점 시기 비교, 최대 일관객수 최고점 비교, 흥행 대작 간의 시기적 경쟁 구도를 직관적으로 확인할 수 있습니다.")

st.markdown("---")


# ====================================================
# [구역 3] (추가 그래프 구역 예시)
# ====================================================
# st.header("3. 세 번째 그래프 구역")
# st.caption("새로운 분석 그래프를 여기에 지속적으로 추가할 수 있습니다.")
