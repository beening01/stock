import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import plotly.express as px


from load_dir import OUT_DIR

df = pd.read_csv(OUT_DIR / "result_etf.csv") 

'''
컬럼
- 전일비: 전일 대비 증감
- 등락률: 전일 대비 종가 변화 (종가-전일종가)/ 전일종가*100
- NAV: ETF 1주가 실제로 보유하고 있는 가치
'''

# # ✅ 1. ETF별 수익률 비교 (성과 분석)
# fig = px.bar(
#     df.sort_values("3개월수익률", ascending=False).head(20),
#     x="3개월수익률",
#     y="종목명",
#     orientation="h",
#     color="3개월수익률",
#     color_continuous_scale="RdBu",
#     title="ETF 3개월 수익률 TOP 20"
# )
# fig.update_layout(yaxis={'categoryorder':'total ascending'})
# fig.show()

# img_path = OUT_DIR / "ETF_returns_20.png"
# fig.write_image(img_path, width=1600, height=900, scale=2)    # 이미지 파일로 저장


#############################################################################
# # 📈 2. 거래량 vs 수익률 버블 차트 (Bubble Chart)
# # 군집화 대상 컬럼만 추출
# X = df[["3개월수익률", "거래량"]].dropna()

# # KMeans 모델 생성 (k=4로 예시)
# kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
# clusters = kmeans.fit_predict(X)

# # 군집 결과를 원본 DataFrame에 추가
# df["cluster"] = clusters

# # 거래량 컬럼을 로그 스케일로 변환 (1을 더해서 log(0) 방지)
# df['log_거래량'] = np.log1p(df['거래량'])

# # 버블 차트 시각화
# fig = px.scatter(
#     df,
#     x='3개월수익률',
#     y='log_거래량',
#     size='log_거래량',
#     color='cluster',
#     hover_name='종목명',
#     title='ETF 3개월 수익률 vs 거래량 (로그 스케일)',
#     labels={'3개월수익률': '3개월 수익률 (%)', 'log_거래량': '거래량 (log scale)'}
# )

# fig.show()
## > 무엇을 보여주는지 잘 해석하기 어려움


#############################################################################
# # 🔥 3. NAV 대비 현재가 괴리율 산점도 (Price vs NAV)
# df["괴리율(%)"] = (df["현재가"] - df["NAV"]) / df["NAV"] * 100

# fig = px.scatter(
#     df,
#     x="종목명",
#     y="괴리율(%)",
#     color="괴리율(%)",
#     color_continuous_scale="Viridis",
#     title="ETF 괴리율 분석",
# )
# fig.update_layout(xaxis_tickangle=-45)
# fig.show()
# # > 괴리율 거의 없음


#############################################################################
# 🧊 4. 등락률 히트맵 (Heatmap)
# 히트맵용 데이터셋 구성 (복수 지표)
# 예시: 히트맵에 사용할 열만 남기고 결측값 제거
heatmap_data = df[['종목명', '등락률', '3개월수익률', '거래량']].copy()

# 결측값 제거
heatmap_data.dropna(inplace=True)

# 종목명을 인덱스로
heatmap_data.set_index('종목명', inplace=True)


# 히트맵 시각화
fig = px.imshow(
    heatmap_data.T,  # 종목명이 X축으로 가게 Transpose
    color_continuous_scale='RdBu',
    aspect='auto',
    title="ETF 주요 지표 히트맵 (결측값 제거)"
)
fig.show()

