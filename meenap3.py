'''from playwright.sync_api import sync_playwright
from datetime import datetime
import google_sheets  # assumes you have this module ready like in your Economic Times script
import time
URL = ["https://chartink.com/screener/copy-copy-copy-sreelakshmi-guruvayoorappan-b-atr-volume-rocket-8",
       "https://chartink.com/screener/hammar-cash-low-paradaily",
       "https://chartink.com/screener/copy-nk-sir-s-uptrend-stocks-all-time-uptrend",
       "https://chartink.com/screener/agp-bullish2-p5",
       "https://chartink.com/screener/1-longtrend-ve",
       "https://chartink.com/screener/copy-copy-down-tranding-buy-at-low-7",
       "https://chartink.com/screener/copy-akshat-monthly-momentum-37",
       "https://chartink.com/screener/all-u1-nk-sir-s-uptrend-stocks-all-time-uptrend",
       "https://chartink.com/screener/aaa8-vp-rocket",
       "https://chartink.com/screener/aaa13-vp-sheshapathi",
       "https://chartink.com/screener/agp-shesha-bulloong1",
       "https://chartink.com/screener/smbg2-new-multibegger-stocks-for-next-few-days",
       "https://chartink.com/screener/copy-sjbl6ch-shesha-buy-bollinger-band-weekly",
       "https://chartink.com/screener/svp2-closing-3-up-since-3-days",
       "https://chartink.com/screener/smbg2-multibegger-stocks-for-next-few-days",
       "https://chartink.com/screener/shesha-magic-buy-love",
       "https://chartink.com/screener/copy-mahi-2-master-trader-vishnu-final-40-address-this-urgent-bellinaire-38-to-47-3",
       "https://chartink.com/screener/cash-tss-momentum-long",
       "https://chartink.com/screener/copy-copy-bb-blaster-2",
       "https://chartink.com/screener/copy-the-best-btst-193",
       "https://chartink.com/screener/22-nw-shesha-magic-buy-love",
       "https://chartink.com/screener/copy-atp-above-long-cash-2",
       "https://chartink.com/screener/22-nw-shesha-magic-buy-love-f-o",
       "https://chartink.com/screener/agp-bullong-2-1",
       "https://chartink.com/screener/agp-bullish2",
       "https://chartink.com/screener/copy-atp-above-long-24"]
       
sheet_id = "1ahDo4LcPCBHVmkxZWYHLmhgCrsGkr_TOlFFNnRAXpi4"
worksheet_name = ["p1","p2","p3","p4","p5","p6","p7","p8","p9","p10","p11","p12","p13","p14","p15","p16","p17","p18","p19","p20","p21","p22","p23","p24","p25","p26"]

def scrape_chartink(URL, worksheet_name):
    print(f"🚀 Starting Chartink scrape for {worksheet_name}...")
    print(f"🌐 Loading: {URL}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
        page = context.new_page()
        page.goto(URL)

        print("📊 Waiting for table to load...")
        page.wait_for_selector("table.table-striped.scan_results_table tbody tr", timeout=15000)
        time.sleep(3)  # allow time for AJAX rows to load

        page.screenshot(path=f"{worksheet_name}_debug.png", full_page=True)

        table_rows = page.query_selector_all("table.table-striped.scan_results_table tbody tr")
        print(f"📥 Extracted {len(table_rows)} rows. Updating Google Sheet...")

        headers = ["Sr", "Stock Name", "Symbol", "Links", "Change", "Price", "Volume"]
        rows = []
        for row in table_rows:
            cells = row.query_selector_all("td")
            row_data = [cell.inner_text().strip() for cell in cells]
            rows.append(row_data)

        # Update Sheet
        google_sheets.update_google_sheet_by_name(sheet_id, worksheet_name, headers, rows)

        # Add Timestamp
        now = datetime.now().strftime("Last updated on: %Y-%m-%d %H:%M:%S")
        google_sheets.append_footer(sheet_id, worksheet_name, [now])

        browser.close()
        print(f"✅ Google Sheet '{worksheet_name}' updated.")


for i in URL:
    scrape_chartink(i,worksheet_name[URL.index(i)])
    print(worksheet_name[URL.index(i)]," updated")
'''

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
import google_sheets
import time

URLS = [
    "https://chartink.com/screener/copy-copy-copy-sreelakshmi-guruvayoorappan-b-atr-volume-rocket-8",
    "https://chartink.com/screener/hammar-cash-low-paradaily",
    "https://chartink.com/screener/copy-nk-sir-s-uptrend-stocks-all-time-uptrend",
    "https://chartink.com/screener/agp-bullish2-p5",
    "https://chartink.com/screener/1-longtrend-ve",
    "https://chartink.com/screener/copy-copy-down-tranding-buy-at-low-7",
    "https://chartink.com/screener/copy-akshat-monthly-momentum-37",
    "https://chartink.com/screener/all-u1-nk-sir-s-uptrend-stocks-all-time-uptrend",
    "https://chartink.com/screener/aaa8-vp-rocket",
    "https://chartink.com/screener/aaa13-vp-sheshapathi",
    "https://chartink.com/screener/agp-shesha-bulloong1",
    "https://chartink.com/screener/smbg2-new-multibegger-stocks-for-next-few-days",
    "https://chartink.com/screener/copy-sjbl6ch-shesha-buy-bollinger-band-weekly",
    "https://chartink.com/screener/svp2-closing-3-up-since-3-days",
    "https://chartink.com/screener/smbg2-multibegger-stocks-for-next-few-days",
    "https://chartink.com/screener/shesha-magic-buy-love",
    "https://chartink.com/screener/copy-mahi-2-master-trader-vishnu-final-40-address-this-urgent-bellinaire-38-to-47-3",
    "https://chartink.com/screener/cash-tss-momentum-long",
    "https://chartink.com/screener/copy-copy-bb-blaster-2",
    "https://chartink.com/screener/copy-the-best-btst-193",
    "https://chartink.com/screener/22-nw-shesha-magic-buy-love",
    "https://chartink.com/screener/copy-atp-above-long-cash-2",
    "https://chartink.com/screener/22-nw-shesha-magic-buy-love-f-o",
    "https://chartink.com/screener/agp-bullong-2-1",
    "https://chartink.com/screener/agp-bullish2",
    "https://chartink.com/screener/copy-atp-above-long-24"
]

sheet_id = "1ahDo4LcPCBHVmkxZWYHLmhgCrsGkr_TOlFFNnRAXpi4"
worksheet_names = ["p1","p2","p3","p4","p5","p6","p7","p8","p9","p10","p11","p12","p13","p14","p15","p16","p17","p18","p19","p20","p21","p22","p23","p24","p25","p26"]

def scrape_chartink(url, worksheet_name):
    print(f"\n🚀 Starting scrape for '{worksheet_name}'")
    print(f"🌐 Loading URL: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            page.goto(url, wait_until='networkidle')
            time.sleep(3)  # Ensure AJAX content loads

            if page.is_visible("text='No records found'"):
                print(f"⚠️ No records found at {url}. Updating empty data.")
                rows = []
            else:
                page.wait_for_selector("table.w-full tbody tr", timeout=60000)
                table_rows = page.query_selector_all("table.w-full tbody tr")
                print(f"📥 Extracted {len(table_rows)} rows.")

                rows = []
                for row in table_rows:
                    cells = row.query_selector_all("td")
                    row_data = [cell.inner_text().strip() for cell in cells]
                    rows.append(row_data)

            headers = ["Sr", "Stock Name", "Symbol", "Links", "Change", "Price", "Volume"]
            google_sheets.update_google_sheet_by_name(sheet_id, worksheet_name, headers, rows)

            now = datetime.now().strftime("Last updated on: %Y-%m-%d %H:%M:%S")
            google_sheets.append_footer(sheet_id, worksheet_name, [now])

            print(f"✅ Worksheet '{worksheet_name}' updated successfully.")

        except PlaywrightTimeoutError:
            print(f"❌ Timeout: Table not found on {url}")

        except Exception as e:
            print(f"❌ Error occurred: {e}")

        finally:
            page.screenshot(path=f"{worksheet_name}_debug.png", full_page=True)
            browser.close()


for index, url in enumerate(URLS):
    scrape_chartink(url, worksheet_names[index])
    print(f"⏱️ Finished '{worksheet_names[index]}'\n")
