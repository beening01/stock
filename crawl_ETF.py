from playwright.sync_api import Browser, Page, Playwright, sync_playwright
import json
from pathlib import Path
import pandas as pd
from load_dir import OUT_DIR
from preprocess import table_to_dataframe
from crawl_marketcap import run_playwright

# ETF(Exchange Traded Fund)란? 상장지수펀드, 주가지수에 따라 수익률이 결정되는 투자 상품

# ETF 페이지로 이동
def goto_market_etf(page: Page):
    page.goto('https://finance.naver.com')
    page.get_by_role("link", name="국내증시").click()
    page.get_by_role("link", name="ETF", exact=True).first.click()


# ETF 데이터 수집
def parse_table_etf(page: Page) -> tuple[list, list]:
    tag_table = page.locator("table", has_text="ETF 주요시세정보")    # ETF 표
    tag_thead = tag_table.locator("tbody > tr").first   # 표의 헤더 부분
    tag_th = tag_thead.locator("th")    # 표의 헤더 부분
    header = tag_th.all_inner_texts()
    

    tag_tbody = tag_table.locator("tbody > tr")     # 보디 부분
    body = []
    rows = tag_tbody.all()[1:]
    for tr in rows:
        tds = tr.locator("td")
        td_texts = tds.all_inner_texts()
        if all(text.strip() == "" for text in td_texts):    # 수집된 데이터가 빈문자열이면
            continue    # 무시하기
        body.append(td_texts)

    return header, body

 

OUT_etf_1 = OUT_DIR / f"{Path(__file__).stem}.json"
OUT_etf_2 = OUT_DIR / f"{Path(__file__).stem}.csv"

if __name__ == '__main__':
    play, browser, page = run_playwright(slow_mo=1000)

    goto_market_etf(page)    # 시가총액 페이지로 이동
    header, body = parse_table_etf(page)    # 코스피 시가총액 데이터 수집

    dumped = json.dumps(dict(header=header, body=body), 
                        ensure_ascii=False, indent=2)
    
    OUT_etf_1.write_text(dumped, encoding="utf-8")    # json으로 저장

    parsed = json.loads(OUT_etf_1.read_text(encoding="utf-8"))    # json 파일 불러오기
    header, body = parsed["header"], parsed["body"]

    df = table_to_dataframe(header, body)
    df.to_csv(OUT_etf_2, index=False)

    browser.close()
    play.stop()