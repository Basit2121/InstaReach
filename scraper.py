from playwright.async_api import async_playwright
import asyncio
import streamlit as st
import json

def count_lines(filename):
    with open(filename, 'r') as file:
        return sum(1 for line in file)
    
def remove_duplicates(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    unique_lines = set(lines)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(unique_lines)

async def scrape_usernames(url, scrape_count):

    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False, channel='firefox')
        context = await browser.new_context()
        cookies_file = 'assets/logins/session1.json'
        with open(cookies_file, 'r') as json_file:
                saved_cookies = json.load(json_file)
        await context.add_cookies(saved_cookies)
        page = await context.new_page()
        await page.goto("https://www.instagram.com/")
        await asyncio.sleep(5)
        await page.keyboard.press("Tab")
        await asyncio.sleep(1)
        await page.keyboard.press("Tab")
        await asyncio.sleep(1)
        await page.keyboard.press("Enter")
    
        while True:
            try:
                svg_element = page.locator('svg[aria-label="Search"]')
                is_visible = await svg_element.is_visible()
                if is_visible ==  True:
                    await asyncio.sleep(5)
                    break
            except Exception as e:
                print(e)
                pass

        await page.goto(f"https://www.instagram.com/{url}/")
        await asyncio.sleep(5)

        div_selector = '.x1lliihq.x1n2onr6.xh8yej3.x4gyw5p.x2pgyrj.xbkimgs.xfllauq.xh8taat.xo2y696'
        await page.click(div_selector)

        st.info(f"Scraping from {url}")

        while True:

            line_count = count_lines("assets/usernames.txt")

            if line_count >= scrape_count:
                st.success(f"Scraping Complete for Account {url}, Scraped Accounts Count is {line_count}.")
                break

            old_post_url = page.url

            await page.keyboard.press("ArrowRight")
            await asyncio.sleep(5)

            new_page_url = page.url

            if old_post_url == new_page_url:
                st.info("No more Posts Left to Scrape")
                break

            while True:
                try:
                    for _ in range(5):
                        await page.keyboard.press("PageDown")
                        await asyncio.sleep(1)
                    svg_selector = 'svg[aria-label="Load more comments"]'
                    svg_element = await page.wait_for_selector(svg_selector, timeout=3000)
                    await svg_element.click()
                except:
                    div_count = await page.query_selector_all('.x1i10hfl.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x1lku1pv.x1a2a7pz.x6s0dn4.xjyslct.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x9f619.x1ypdohk.x1f6kntn.xwhw2v2.xl56j7k.x17ydfre.x2b8uid.xlyipyv.x87ps6o.x14atkfc.xcdnw81.x1i0vuye.xjbqb8w.xm3z3ea.x1x8b98j.x131883w.x16mih1h.x972fbf.xcfux6l.x1qhh985.xm0m39n.xt0psk2.xt7dq6l.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x1n5bzlp.xqnirrm.xj34u2y.x568u83')
                    for divs in div_count:
                            inner_html = await divs.inner_text()
                            with open("assets/usernames.txt", 'a', encoding='utf-8')as file:
                                file.write(f'{inner_html}\n')
                            st.info(f'{inner_html}')
                    remove_duplicates("assets/usernames.txt", "assets/usernames.txt")
                    break

            await asyncio.sleep(5)