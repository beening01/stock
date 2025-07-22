from pathlib import Path
import pandas as pd
import plotly.express as px
from load_dir import OUT_DIR
from crawl_marketcap import OUT_3

OUT_4 = OUT_DIR / f"{Path(__file__).stem}.csv"

# 종목별 누적비율 계산
def top_kospi_company(df:pd.DataFrame, prop:float) -> pd.DataFrame:
    df["시가총액"] = df["시가총액"].str.replace(",", "").astype(int)
    df["조단위"] = df["시가총액"] / 10_000    # 억단위 -> 조단위

    df = df.sort_values("시가총액", ascending=False)    # 내림차순
    df["누적비율"] = df["시가총액"].cumsum() / df["시가총액"].sum()
    df_sliced = df.loc[df['누적비율'] <= prop]    # 슬라이싱

    return df_sliced.filter(["종목명", "시가총액", "조단위", "누적비율"])


# 종목별 시가총액 시각화
df = pd.read_csv(OUT_3)

df_top = top_kospi_company(df, 0.5)
df_top.to_csv(OUT_4, index=False)

fig = px.treemap(
    df_top,
    path=["종목명"],    # 종목명 기준으로 데이터 분류
    values="조단위",    # 조단위 기준으로 종목별 면전 계산
)

fig.update_traces(
    marker=dict(
        cornerradius=5,    # 모서리 둥글게
        colorscale="viridis",    # 색상
        pad=dict(t=10, r=10, b=10, l=10)    # 트리맵 여백
    ),
    texttemplate = "<b>%{label}</b><br>%{value:,.0f}조원",    # 종목명, 시가총액
    textfont_size = 30
)

fig.update_layout(margin=dict(t=0, r=0, b=0, l=0))    # 이미지 여백

img_path = OUT_DIR / "result_tree.png"
fig.write_image(img_path, width=1600, height=900, scale=2)    # 이미지 파일로 저장