
import streamlit as st
import pandas as pd


# ---------------------------------
# 페이지 설정
# ---------------------------------
st.set_page_config(
    page_title="서울 기온 변화",
    page_icon="🌡️",
    layout="wide"
)


# ---------------------------------
# 데이터 불러오기
# ---------------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"


@st.cache_data
def load_data():
    try:
        # UTF-8 인코딩으로 먼저 시도
        return pd.read_csv(DATA_URL, encoding="utf-8")
    except UnicodeDecodeError:
        # 실패하면 CP949로 시도
        return pd.read_csv(DATA_URL, encoding="cp949")


# ---------------------------------
# 데이터 처리
# ---------------------------------
try:
    df = load_data()

    # 날짜를 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce"
    )

    # 기온 데이터를 숫자로 변환
    for column in ["평균기온", "최저기온", "최고기온"]:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # 연도 추출
    df["연도"] = df["날짜"].dt.year


    # ---------------------------------
    # 제목
    # ---------------------------------
    st.title("🌡️ 서울의 100년간 연평균 기온 변화")

    st.write(
        "서울의 기온 데이터를 분석하여 "
        "연도별 연평균 기온의 변화를 살펴봅니다."
    )


    # ---------------------------------
    # 원본 데이터 요약통계
    # ---------------------------------
    st.subheader("📊 원본 데이터 요약통계")

    st.write(
        "원본 데이터의 평균기온, 최저기온, 최고기온에 대한 "
        "개수, 평균, 표준편차, 최솟값, 사분위수, 최댓값을 나타냅니다."
    )

    # 요약통계 계산
    summary = df[
        ["평균기온", "최저기온", "최고기온"]
    ].describe()

    # 통계 항목을 한글로 변경
    summary = summary.rename(
        index={
            "count": "개수",
            "mean": "평균",
            "std": "표준편차",
            "min": "최소",
            "25%": "25%",
            "50%": "중앙값",
            "75%": "75%",
            "max": "최대"
        }
    )

    # 소수점 둘째 자리까지 표시
    summary = summary.round(2)

    # 행과 열을 바꾼 형태
    st.dataframe(
        summary,
        use_container_width=True
    )


    # ---------------------------------
    # 연도별 연평균 기온 계산
    # ---------------------------------
    yearly_temp = (
        df.dropna(subset=["연도", "평균기온"])
        .groupby("연도")["평균기온"]
        .mean()
        .reset_index()
    )

    # 연도순으로 정렬
    yearly_temp = yearly_temp.sort_values("연도")


    # ---------------------------------
    # 연도별 연평균 기온 그래프
    # ---------------------------------
    st.subheader("📈 연도별 연평균 기온")

    chart_data = yearly_temp.set_index("연도")

    st.line_chart(
        chart_data["평균기온"],
        x_label="연도",
        y_label="연평균 기온 (℃)"
    )


    # ---------------------------------
    # 분석 기간
    # ---------------------------------
    first_year = int(yearly_temp["연도"].min())
    last_year = int(yearly_temp["연도"].max())

    st.info(
        f"📅 {first_year}년부터 {last_year}년까지의 "
        "서울 연평균 기온 변화를 보여주는 그래프입니다."
    )


    # ---------------------------------
    # 연도별 데이터 표
    # ---------------------------------
    with st.expander("📋 연도별 연평균 기온 데이터 보기"):

        display_data = yearly_temp.copy()

        display_data["평균기온"] = (
            display_data["평균기온"].round(2)
        )

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )


    # ---------------------------------
    # 원본 데이터 일부 보기
    # ---------------------------------
    with st.expander("📄 원본 데이터 보기"):

        st.dataframe(
            df.head(20),
            use_container_width=True,
            hide_index=True
        )


# ---------------------------------
# 오류 처리
# ---------------------------------
except Exception as e:
    st.error("데이터를 불러오거나 처리하는 중 오류가 발생했습니다.")

    st.write("오류 내용:")
    st.code(str(e))
