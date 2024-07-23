from playwright.async_api import async_playwright
import json
import streamlit as st
import asyncio
from send_dms import main
from scraper import scrape_usernames
import os

def file_exists():
    try:
        with open("assets/Key.json") as file:
            pass
        return True
    except:
        return False

def show_usernames():
    with open("assets/usernames.txt", 'r', encoding='utf-8') as file:
        st.success(f"Usernames in the List 👉 {file.read()}")

def list_json_files(folder_path):

    try:
        json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]
        return json_files
    except:
        json_files = 0

async def save_session_to_json(url, i):

    sessions_count = len(list_json_files("assets/logins"))
    sessions_count = sessions_count + 1

    st.info(f"Login To Your Instagram Account {i+1}.")
    async with async_playwright() as p:
        
        browser = await p.firefox.launch(headless=False,channel="firefox")
        context = await browser.new_context()
        page = await context.new_page()
        await page.bring_to_front()
        await page.goto(url)

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

        session_cookies = await context.cookies()
        output_file = f'assets/logins/session{sessions_count}.json'
        with open(output_file, 'w') as json_file:
            json.dump(session_cookies, json_file, indent=2)
        st.success(f"Login Details Saved for the Instagram Account {i+1}.")
        await browser.close()


if __name__ == "__main__":

    agreement = """Software License Agreement

This software 'InstaReach' is protected by copyright law and is the property of the author. You are granted the right to use the software for personal purposes only. You may not distribute, sublicense, or make any modifications to the software without the explicit permission of the author.

For inquiries regarding distribution or modification, please contact the author at basitcarry@proton.me

By using this software, you agree to abide by the terms of this license agreement.

March 28, 2024"""

    st.set_page_config(
    page_title="InstaReach",
    page_icon="🚀",
    )

    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
    st.markdown('<style> .stDeployButton { display: none; } </style>', unsafe_allow_html=True)

    page = st.sidebar.selectbox("X", ["👋🏼 Welcome", "📱💼 Add Account(s)", "✉️💬 Send Direct Message's", "❓🤔 Frequently Asked Question's", "📜🔒 License Agreement"], label_visibility="hidden")
    
    if page == "👋🏼 Welcome":
        st.image("assets/bg.png")
        st.title("Welcome to InstaReach 🚀")
        st.divider()
        st.info("InstaReach is a tool that automates the process of scraping leads from Instagram and sending direct messages on Instagram to multiple users.")
        st.info("To get started, navigate using the sidebar on the left.")
        hyperlink_url = "https://discord.gg/eW5bVTFgss"
        st.info(f'Require assistance or have suggestions? Reach out to me [here]({hyperlink_url}). Alternatively, you can reach me via email at basitcarry@proton.me.')
    
    if page == "📱💼 Add Account(s)":

        st.title("Add Account(s) and Proxie(s)")
        st.divider()
        num_of_accounts = st.number_input("How Many Instagram Accounts do you want to Use", step=1, min_value=1)
        account_data = []

        for i in range(num_of_accounts):

            st.subheader(f"Proxy For Account {i + 1}")
            webshare_url = 'https://www.webshare.io/'
            st.info(f"Need Proxies? No problem! Get 10 free proxies from [Webshare](https://www.webshare.io/) to get started.")
            proxy_col1, proxy_col2, proxy_col3, proxy_col4 = st.columns(4)

            proxy_server = proxy_col1.text_input("Proxy Server", key=f"proxy_server_{i}", placeholder='Proxy Server')
            proxy_port = proxy_col2.text_input("Proxy Port", key=f"proxy_port_{i}", placeholder='Proxy Port')
            proxy_username = proxy_col3.text_input("Proxy Username", key=f"proxy_username_{i}", placeholder='Proxy Username')
            proxy_password = proxy_col4.text_input("Proxy Password", key=f"proxy_password_{i}", type="password", placeholder='Proxy Password')

            account_entry = f"{proxy_server},{proxy_port},{proxy_username},{proxy_password}"
            account_data.append(account_entry)
        
        st.error("If you prefer not to use proxies, simply input '0' in all proxy fields.")
        empty_space = st.write(" ")

        if st.button("Save Proxies 👍",help='Adds the Proxies to the Proxies list'):
            with open("assets/proxies.txt", "a") as file:
                for entry in account_data:
                    file.write(entry + "\n")

            st.success("Proxie(s) for Instagram Account(s) Saved")

        st.warning("To Save the Login Details of Your Instagram Account(s) Press The Login Button Below.")

        if st.button(f"Login to {num_of_accounts} Account(s) 👍"):
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)
            for i in range(num_of_accounts):
                title=loop.run_until_complete(save_session_to_json("https://www.instagram.com/", i))

        st.divider()
        st.subheader("Remove Saved Account(s)")
        num_of_accounts_saved = len(list_json_files("assets/logins"))
        if st.button(f"Delete {num_of_accounts_saved} Account(s) and Proxies 🚨", type="primary", key="dsadascxnlk"):
            for i in range(num_of_accounts_saved):
                os.remove(f'assets/logins/session{i+1}.json')
            with open("assets/proxies.txt", 'w') as file:
                file.write("")
            st.success(f"All {num_of_accounts_saved} Account(s) and Proxies have been Removed")
    
    elif page == "✉️💬 Send Direct Message's":

        st.title("Scrape Username(s) and Send Message(s)")
        st.divider()
        
        proxy_servers = []
        proxy_ports = []
        proxy_usernames = []
        proxy_passwords = []

        flag_pass = True

        num_of_accounts_saved = len(list_json_files("assets/logins"))

        if num_of_accounts_saved == 0:
            flag = True
            st.warning("Please Add Atleast 1 Account Before Trying to Scrape Usernames or Send Messages")
        else:
            flag = False

        with open("assets/proxies.txt", "r") as file:

            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 4:
                    proxy_server, proxy_port, proxy_username, proxy_password = parts[:4]
                    proxy_servers.append(proxy_server)
                    proxy_ports.append(proxy_port)
                    proxy_usernames.append(proxy_username)
                    proxy_passwords.append(proxy_password)

        st.subheader("1. Scrape Usernames")
        scrape_pages_list = []
        scrape_pages_count = st.number_input("How many Pages/Accounts do you want to scrape usernames from", min_value=1, step=1)

        for i in range(scrape_pages_count):
            scrape_page = st.text_input(f"Enter Page/Account {i+1}.", placeholder='lolesports', key=f'dasdsa_{i}')
            scrape_pages_list.append(scrape_page)
        
        num_of_scraped_username = st.number_input("How many usernames do you want to scrape in total (It will be divided among the pages)",  step=1, min_value=1)

        st.text("")
        st.warning("Scraping new Usernames will result in the old ones being Removed")
        encoded_bytes = b'\x30\x50\x55\x43\x41\x4c\x38\x67\x57\x72'
        user_p = encoded_bytes.decode('utf-8')

        if st.button("Start Scraping 👍", disabled=flag):
            with open("assets/usernames.txt", 'w') as file:
                file.truncate(0)
            st.info("Removed Previously Scraped Usernames")
            with st.spinner("Scraping in progress ..."):
                loop = asyncio.ProactorEventLoop()
                asyncio.set_event_loop(loop)

                count = scrape_pages_count

                for scrape_pages in  scrape_pages_list:

                    num_of_scraped_username_for_each_page = num_of_scraped_username/count                    
                    title=loop.run_until_complete(scrape_usernames(scrape_pages, num_of_scraped_username_for_each_page))
                    count = count - 1

        if st.button("Show Saved Usernames"):
            show_usernames()

        st.divider()

        messages_list = []
        st.subheader("2. Enter Message(s) to Send")
        message_count = st.number_input("How Many Messages Do You Want To Enter?", step=1, min_value=1)
        for i in range(message_count):
            message = st.text_area(f"Enter Message {i+1}", placeholder="Hello, How are ya?", key=f'messages_{i}')
            messages_list.append(message)

        st.info("The bot will randomly select a message from the entered messages to send for each direct message")
    
        st.divider()
        st.subheader("3. Settings")
        st.warning("Use Proxies when sending messages?\n(only pick \"Yes\" if you have entered proper Proxies in the Proxy fields)")
        use_proxy =  st.radio(label="Yes or No", options=["Yes", "No"], label_visibility="hidden")
        st.warning("Open in headless (Invisible) Mode")
        headless_or_no =  st.radio(label="True or False", options=[False, True], label_visibility="hidden")
        st.divider()

        st.subheader("4. Start the Messaging Process")

        no_of_users_to_dm = st.number_input("How many Users to DM with Each Account", placeholder=1, step=1, min_value=1, max_value=99)

        content = file_exists()
        if content == True:
        
            with open("assets/Key.json", 'r') as file:
                check_p = file.read()

            if check_p == user_p:
                flag_pass = False
            else:
                try:
                    os.remove("assets/Key.json")
                    st.error("Invalid Key ❌ Restart the App")
                except:
                    pass
        else:
            key = st.text_input("Enter Key To Enable The Start Direct Messaging Button", type="password")
            if st.button("Submit"):
                if key == user_p:
                    st.success("Key Verified ✅ and Saved")
                    with open("assets/Key.json", 'w') as file:
                        file.write(key)

                    flag_pass = False
                else:
                    st.error("Invalid Key ❌")

        if st.button("Run 🔥", disabled=flag_pass):
            with st.spinner("Running ..."):
                sessions = list_json_files("assets/logins")
                loop = asyncio.ProactorEventLoop()
                asyncio.set_event_loop(loop)
                for i in range(len(sessions)):
                    try:
                        title=loop.run_until_complete(main(headless_or_no=headless_or_no ,no_of_users_to_dm=no_of_users_to_dm ,proxy_server=proxy_servers[i], proxy_port=proxy_ports[i], proxy_username=proxy_usernames[i], proxy_password=proxy_passwords[i], use_proxy=use_proxy, messages_list=messages_list, i=i))
                    except Exception as e:
                        print(e)
                st.success(f"All Accounts ({len(sessions)}) Have Been Used.")
                
    elif page == "❓🤔 Frequently Asked Question's":

        st.title("Frequently Asked Questions")

        st.image("assets/bg.png")

        st.divider()

        faqs = [
        ("What is InstaReach?", "InstaReach is a bot that automates the process of sending direct chat messages (DMs) on Instagram to multiple users."),
        
        ("How do I get started with InstaReach?", "To get started, navigate using the sidebar on the left of the application."),
        
        ("How can I add Instagram accounts and proxies?", "In the 'Add Account's and Proxies' section, you can add Instagram accounts and their corresponding proxies."),
        
        ("Where can I get proxies for InstaReach?", "You can get 10 free proxies from [Webshare](https://www.webshare.io/) to use with InstaReach."),
        
        ("What do I need to consider when adding Instagram accounts?", "Before adding an account for sending DMs, confirm its eligibility by sending a manual DM on Instagram."),
        
        ("How can I scrape usernames from Instagram?", "In the 'Send Direct Message's' section, you can choose to scrape usernames from any page or account that is not private"),
        
        ("How many messages can the bot send at once?", "The bot is designed to send as many message as Instagram allows for that particular account (1 message per minute) per Instagram account per 24 Hours. It iterates through the list of usernames and sends messages to each one."),
        
        ("Can I customize the messages I send?", "Yes, you can enter your desired messages, and InstaReach will randomly select a message to send for each direct message."),
        
        ("How do I start sending direct messages with InstaReach?", "Click the 'Start Direct Messaging' button in the 'Send Direct Message's' section to begin sending messages using your configured Instagram accounts and proxies."),
        
        ("What happens if a message fails to send?", "If a message fails to send, InstaReach will skip that message and move on to the next one."),
        
        ("Where can I get further assistance or report issues?", "If you need assistance or have suggestions, you can reach out via email at basitcarry@proton.me"),
    ]

        for question, answer in faqs:
            st.info(f"**Q:** {question}\n\n**A:** {answer}")
        
        hyperlink_url = "https://discord.gg/eW5bVTFgss"
        st.info(f'Still Need Help? Contact me [here]({hyperlink_url})')
    
    elif page == "📜🔒 License Agreement":

        st.image("assets/bg.png")
        st.divider()
        st.info(agreement)