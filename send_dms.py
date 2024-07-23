import asyncio
from playwright.async_api import async_playwright
import random
import streamlit as st
import json
import random

def remove_first_line(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    lines = lines[1:]
    with open(filename, 'w') as file:
        file.writelines(lines)

async def main(headless_or_no, no_of_users_to_dm, proxy_server, proxy_port, proxy_username, proxy_password, use_proxy, messages_list, i):

    async with async_playwright() as p:

        if use_proxy == 'Yes':
            browser = await p.firefox.launch(proxy={
                    'server': f"{proxy_server}:{proxy_port}",
                    'username': proxy_username,
                    'password': proxy_password
                }, channel='firefox', headless=headless_or_no)
            
        elif use_proxy == 'No':
            browser = await p.firefox.launch(channel='firefox', headless=headless_or_no)

        context = await browser.new_context()

        cookies_file = f'assets/logins/session{i+1}.json'
        with open(cookies_file, 'r') as json_file:
                saved_cookies = json.load(json_file)
        await context.add_cookies(saved_cookies)

        page = await context.new_page()
        await page.bring_to_front()
        await page.goto("https://www.instagram.com/")
        await asyncio.sleep(random.uniform(4, 5))

        await page.keyboard.press("Tab")
        await asyncio.sleep(2)
        await page.keyboard.press("Enter")
        await asyncio.sleep(2)

        unique_usernames = []

        with open('assets/usernames.txt', 'r') as file:
            for line in file:
                username = line.strip()
                if username not in unique_usernames:
                    unique_usernames.append(username)
        
        count = 0

        for username in unique_usernames:
                
                remove_first_line("assets/usernames.txt")
                message = random.choice(messages_list)
                st.info(f'Message Choice: {message}')
                count = int(count + 1)
                await page.goto(f'https://www.instagram.com/direct/')
                await asyncio.sleep(random.uniform(5, 6))
                div_selector = '.x6s0dn4.x78zum5.xdt5ytf.xl56j7k'
                div_element = await page.query_selector(div_selector)
                await div_element.click()
                await asyncio.sleep(4)
                await page.keyboard.type(username)
                div_exists = await page.wait_for_selector(f'span.x1lliihq.x193iq5w.x6ikm8r.x10wlt62.xlyipyv.xuxw1ft')
                await asyncio.sleep(3)
                await page.keyboard.press("Tab")
                await asyncio.sleep(1)
                await page.keyboard.press("Enter")
                await asyncio.sleep(1)
                await page.keyboard.press("Tab")
                await asyncio.sleep(1)
                await page.keyboard.press("Enter")
                await asyncio.sleep(1)
                await page.keyboard.type(message)
                await asyncio.sleep(2)
                await page.keyboard.press("Enter")
                await asyncio.sleep(2)

                st.success(f"Message Sent to {username}")
                if count == no_of_users_to_dm:
                    st.warning(f"{no_of_users_to_dm} People Messaged With Account {i+1}, Moving on to Next Account.")
                    break

        await browser.close()