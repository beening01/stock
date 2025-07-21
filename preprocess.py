# 데이터 정제하기
import pandas as pd
import json
from pathlib import Path
from load_dir import OUT_DIR


def clean_white_space(text: str) -> str:
    return " ".join(text.split())    # 공백 문자 정제

def table_to_dataframe(header: list, body: list) -> pd.DataFrame:
    df = pd.DataFrame(body, columns=header)    # DataFrame 객체 생성
    df = df.dropna(how="any")    # 빈 데이터가 있으면 행 삭제
    df = df.iloc[:, :-1]    # 마지막열 삭제

    for col in df.columns:
        df[col] = df[col].apply(clean_white_space)    # 열 공백 문자 정제

    return df


def clean_etf_data(OUT_DIR):
    df = pd.read_csv(OUT_DIR / "crawl_ETF.csv")

    # 쉼표 제거 + 숫자형 변환
    cols_to_int = ["현재가", "전일비", "NAV", "거래량", "거래대금(백만)"]
    for col in cols_to_int:
        df[col] = df[col].str.replace(",", "").astype(float)

    # 수익률, 등락률: % 제거 → float
    cols_percent = ["등락률", "3개월수익률"]
    for col in cols_percent:
        df[col] = (
            df[col]
            .str.replace("%", "")         # % 제거
            .str.replace(",", "")         # 혹시 쉼표 들어간 경우 대비
            .astype(float)
        )

    # 결측치 처리: 3개월 수익률만 일부 누락
    df = df.dropna(subset=["3개월수익률"])  # 또는 df["3개월수익률"].fillna(0)

    # 확인
    print(df.dtypes)
    print(df.head())


# from crawl_marketcap import OUT_1

# if __name__ == "__main__":
#     parsed = json.loads(OUT_1.read_text(encoding='utf-8'))
#     header = parsed["header"]
#     body = parsed["body"]

#     df = table_to_dataframe(header, body)
#     df.to_csv(OUT_DIR / "content.csv", index=False)