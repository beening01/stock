# 데이터 정제하기
import pandas as pd
import numpy as np
import json
from pathlib import Path
from load_dir import OUT_DIR


def clean_etf_csv(csv_path: str) -> pd.DataFrame:
    """
    ETF CSV 파일을 읽어 전처리된 DataFrame을 반환합니다.

    - 쉼표 및 기호 제거
    - 퍼센트 수치 변환
    - 수치형 형식 변환
    - 결측값 제거
    """
    df = pd.read_csv(csv_path)

    # 숫자형 컬럼: 쉼표 제거 후 float 변환
    cols_to_float = ["현재가", "전일비", "NAV", "거래량", "거래대금(백만)"]
    for col in cols_to_float:
        df[col] = df[col].astype(str).str.replace(",", "", regex=False)
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 수익률 컬럼 (% 제거 후 float 변환)
    percent_cols = ["등락률", "3개월수익률"]
    for col in percent_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("%", "", regex=False)
            .str.replace(",", "", regex=False)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 결측값 제거 (특히 수익률 결측이 있는 경우)
    df = df.dropna(subset=["3개월수익률"]).reset_index(drop=True)

    return df


OUT_preprocess = OUT_DIR / "result_erf.csv"

if __name__ == "__main__":

    # 파일 경로 지정
    csv_path = OUT_DIR / "crawl_ETF.csv"

    # 정제된 DataFrame 불러오기
    df_clean = clean_etf_csv(csv_path)

    # 확인
    print(df_clean.info())
    print(df_clean.dtypes)

    df_clean.to_csv(OUT_preprocess, index=False)