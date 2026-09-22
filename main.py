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
        orientation="h",
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
# [구역 3] 날짜별 10위권 일관객 합계 (영역 그래프)
# ====================================================
st.header("3. 날짜별 10위권 일관객 합계 추이")
st.caption("매일 박스오피스 10위권 영화들의 일관객을 모두 더해 극장가 전체 관객 규모의 흐름을 영역 그래프로 나타냅니다.")

# 날짜별 10위권 일관객 합계 계산
df_daily_total = df.groupby('날짜')['일관객'].sum().reset_index().sort_values('날짜')

# 관객 수 합계가 가장 컸던 상위 3일 추출
top3_days = df_daily_total.nlargest(3, '일관객')

# 영역 그래프(Area Chart) 생성
fig3 = px.area(
    df_daily_total,
    x='날짜',
    y='일관객',
    title="날짜별 10위권 관객수 전체 합계 흐름",
    labels={'날짜': '날짜', '일관객': '10위권 관객수 합계 (명)'}
)

# 호버 포맷 지정
fig3.update_traces(
    hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>10위권 총 관객수:</b> %{y:,}명<extra></extra>",
    fillcolor="rgba(31, 119, 180, 0.3)",
    line=dict(color="#1f77b4")
)

# 관객수 TOP 3 날짜에 텍스트 및 화살표 표시 (Annotation)
for rank, (_, row) in enumerate(top3_days.iterrows(), 1):
    date_str = row['날짜'].strftime('%Y-%m-%d')
    val_str = f"{row['일관객']:,}명"
    
    fig3.add_annotation(
        x=row['날짜'],
        y=row['일관객'],
        text=f"<b>🔥 TOP {rank}</b><br>{date_str}<br>({val_str})",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#E02424",
        ax=0,
        ay=-45,
        bgcolor="white",
        bordercolor="#E02424",
        borderwidth=1,
        borderpad=4
    )

fig3.update_layout(hovermode="x unified")

st.plotly_chart(fig3, use_container_width=True)

# 그래프 분석 내용 작성 칸
st.info("💡 **이 그래프로 알 수 있는 것**: 명절, 연휴, 크리스마스 등 1년 중 극장가 전체에 관객이 가장 몰렸던 최전성기 날짜 TOP 3와 극장가 비수기/성수기 시즌 흐름을 한눈에 파악할 수 있습니다.")

st.markdown("---")


# ====================================================
# [구역 4] 기간 내 총 관객수 TOP 10 영화 (가로 막대그래프)
# ====================================================
st.header("4. 기간 내 총 관객수 TOP 10 영화")
st.caption("분석 기간 동안 10위권 내에서 동원한 총 관객수를 기준으로 TOP 10 영화를 선정하여 순위를 비교합니다.")

# 영화별 총 관객수 및 10위권 진입 일수 집계
df_movie_summary = (
    df.groupby('영화명')
    .agg(
        총관객수=('일관객', 'sum'),
        진입일수=('날짜', 'count')
    )
    .reset_index()
)

# 총 관객수 기준 상위 10개 영화 추출
df_top10 = df_movie_summary.nlargest(10, '총관객수')

# 가로 막대그래프에서 상위 순위가 위쪽에 오도록 오름차순 정렬
df_top10_sorted = df_top10.sort_values('총관객수', ascending=True)

# Plotly 가로 막대그래프 생성
fig4 = px.bar(
    df_top10_sorted,
    x='총관객수',
    y='영화명',
    orientation='h',
    text='총관객수',
    title="기간 내 총 관객수 TOP 10 영화 및 10위권 진입 일수",
    labels={'총관객수': '총 관객수 (명)', '영화명': '영화 제목'},
    color='총관객수',
    color_continuous_scale='Blues'
)

# 막대 외부 수치 레이블 및 customdata(10위권 진입 일수) 지정
fig4.update_traces(
    texttemplate='%{text:,}명',
    textposition='outside',
    customdata=df_top10_sorted[['진입일수']],
    hovertemplate="<b>영화명:</b> %{y}<br><b>총 관객수:</b> %{x:,}명<br><b>10위권 진입 일수:</b> %{customdata[0]}일<extra></extra>"
)

# 차트 여백 및 색상바(Colorbar) 레이아웃 조정
fig4.update_layout(
    coloraxis_showscale=False,
    xaxis=dict(title="총 관객수 (명)"),
    yaxis=dict(title="영화 제목"),
    height=500
)

st.plotly_chart(fig4, use_container_width=True)

# 그래프 분석 내용 작성 칸
st.info("💡 **이 그래프로 알 수 있는 것**: 분석 기간 내 최다 관객을 동원한 히트작 10편의 누적 규모 차이와, 각 영화가 박스오피스 10위권 내에 며칠 동안 상주(롱런)했는지를 한눈에 비교할 수 있습니다.")

st.markdown("---")


# ====================================================
# [구역 5] (다섯 번째 그래프 추가 구역)
# ====================================================
# st.header("5. 다섯 번째 그래프 구역")
# st.caption("새로운 분석 시각화 요소를 지속적으로 추가할 수 있는 확장 영역입니다.")
