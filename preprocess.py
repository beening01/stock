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

# from crawl_marketcap import OUT_1

# if __name__ == "__main__":
#     parsed = json.loads(OUT_1.read_text(encoding='utf-8'))
#     header = parsed["header"]
#     body = parsed["body"]

#     df = table_to_dataframe(header, body)
#     df.to_csv(OUT_DIR / "content.csv", index=False)