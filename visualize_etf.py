import plotly.express as px
import pandas as pd
from load_dir import OUT_DIR

df = pd.read_csv(OUT_DIR / "result_etf.csv") 



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
