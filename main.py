
import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="서울 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"

st.title("🌡️ 서울의 100년간 연평균 기온 변화")
st.write("서울의 기온 데이터를 이용해 연도별 평균기온의 변화를 살펴봅니다.")


# 데이터 불러오기
@st.cache_data
def load_data():
    # 먼저 UTF-8로 읽기
    try:
        df = pd.read_csv(DATA_URL, encoding="utf-8")
    except UnicodeDecodeError:
        # UTF-8이 아니면 CP949로 다시 시도
        df = pd.read_csv(DATA_URL, encoding="cp949")

    return df


try:
    df = load_data()

    # 날짜를 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

    # 평균기온을 숫자로 변환
    df["평균기온"] = pd.to_numeric(
        df["평균기온"],
        errors="coerce"
    )

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    # 연도별 평균기온 계산
    yearly_temp = (
        df.dropna(subset=["평균기온", "연도"])
        .groupby("연도")["평균기온"]
        .mean()
        .reset_index()
    )

    # 연도순 정렬
    yearly_temp = yearly_temp.sort_values("연도")

    st.subheader("📈 연도별 연평균 기온")

    # 그래프
    chart_data = yearly_temp.set_index("연도")

    st.line_chart(
        chart_data["평균기온"],
        x_label="연도",
        y_label="평균기온 (℃)"
    )

    # 데이터 기간 표시
    first_year = int(yearly_temp["연도"].min())
    last_year = int(yearly_temp["연도"].max())

    st.info(
        f"📊 {first_year}년부터 {last_year}년까지 "
        "서울의 연평균 기온 변화를 나타낸 그래프입니다."
    )

    # 데이터 표
    with st.expander("연도별 평균기온 데이터 보기"):
        display_data = yearly_temp.copy()
        display_data["평균기온"] = display_data["평균기온"].round(2)

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )

except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.write(f"오류 내용: {e}")
