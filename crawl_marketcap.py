from playwright.sync_api import Browser, Page, Playwright, sync_playwright
import json
from pathlib import Path
import pandas as pd
from load_dir import OUT_DIR
from preprocess import table_to_dataframe

def run_playwright(slow_mo: float = None) -> tuple[Playwright, Browser, Page]:
    play: Playwright = sync_playwright().start()    # playwright 객체 생성

    browser:  Browser = play.chromium.launch(    # Browser 객체 생성
        args=["--start-maximized"],    # 웹 브라우저 최대화
        headless=False,    # 헤드리스 모드 사용 여부
        slow_mo=slow_mo    # 자동화 처리 지연 시간
    )

    page : Page = browser.new_page(no_viewport=True)    # Page 객체 생성 
    return play, browser, page


# 시가총액 페이지로 이동 (Async)
def goto_market_cap(page: Page):
    page.goto('https://finance.naver.com')
    page.get_by_role("link", name="국내증시").click()
    page.get_by_role("link", name="시가총액", exact=True).first.click()


# 시가총액 수집 (Async)
def parse_table_kospi(page: Page) -> tuple[list, list]:
    tag_table = page.locator("table", has_text="코스피")    # 코스피 시가총액 표
    tag_thead = tag_table.locator("thead > tr > th")    # # 표의 헤더 부분
    header = tag_thead.all_inner_texts()

    tag_tbody = tag_table.locator("tbody > tr")     # 보디 행
    body = []
    rows = tag_tbody.all()
    for tr in rows:
        tds = tr.locator("td")
        td_texts = tds.all_inner_texts()
        body.append(td_texts)

    return header, body

def fetch_total_page(page:Page) -> int:
    table = page.locator("table", has_text="페이지 네비게이션")    # <table> 태그 추출
    td = table.locator("tbody > tr > td").last    # 마지막 <td> 태그 추출
    href = td.locator("a").get_attribute("href")    # <a> 태그 href 속성 추출
    return int(href.split("=")[-1])    # URL에서 페이지 추출
 

def goto_page(page:Page, to:int):
    page.goto(f"https://finance.naver.com/sise/sise_market_sum.naver?&page={to}")

def fetch_market_cap(page: Page) -> pd.DataFrame:
    total_page = fetch_total_page(page)
    result = []

    for to in range(1, total_page+1):
        goto_page(page, to)
        header, body = parse_table_kospi(page)

        df = table_to_dataframe(header, body)
        result.append(df)

    return pd.concat(result)


# OUT_1 = OUT_DIR / f"{Path(__file__).stem}.json"
# OUT_2 = OUT_DIR / f"{Path(__file__).stem}.csv"
OUT_3 = OUT_DIR / "result.csv"

if __name__ == '__main__':
    play, browser, page = run_playwright(slow_mo=1000)

    goto_market_cap(page)    # 시가총액 페이지로 이동
    header, body = parse_table_kospi(page)    # 코스피 시가총액 데이터 수집

    dumped = json.dumps(dict(header=header, body=body), 
                        ensure_ascii=False, indent=2)
    
    # OUT_1.write_text(dumped, encoding="utf-8")    # json으로 저장

    # parsed = json.loads(OUT_1.read_text(encoding="utf-8"))    # json 파일 불러오기
    # header, body = parsed["header"], parsed["body"]

    # df = table_to_dataframe(header, body)
    # df.to_csv(OUT_2, index=False)

    total_page = fetch_total_page(page)
    print(f"{total_page=}")
    
    df_result = fetch_market_cap(page)    # 코스피 시가총액 표 추출
    df_result.to_csv(OUT_3, index=False)

    browser.close()
    play.stop()