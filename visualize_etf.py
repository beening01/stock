import plotly.express as px
import pandas as pd
from load_dir import OUT_DIR

df = pd.read_csv(OUT_DIR / "result_etf.csv") 

'''
컬럼 분석
- 전일비: 전일 대비 증감
- 등락률: 전일 대비 종가 변화 (종가-전일종가)/ 전일종가*100
- NAV: ETF 1주가 실제로 보유하고 있는 가치
'''

# ✅ ETF별 수익률 비교 (성과 분석)
fig = px.bar(
    df.sort_values("3개월수익률", ascending=False).head(20),
    x="3개월수익률",
    y="종목명",
    orientation="h",
    color="3개월수익률",
    color_continuous_scale="RdBu",
    title="ETF 3개월 수익률 TOP 20"
)
fig.update_layout(yaxis={'categoryorder':'total ascending'})
fig.show()

img_path = OUT_DIR / "ETF_returns_20.png"
fig.write_image(img_path, width=1600, height=900, scale=2)    # 이미지 파일로 저장
