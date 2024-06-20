import telebot,os
from telebot import types
import json
import random
import string
import re
import requests,user_agent
# - - - - - - - - -  [ Bot & Others ]  - - - - - - - - - 
TOKEN = '7202513885:AAENYe5rVv-Jhqx-PiD0yEDIpbSt37sMezg'
bot = telebot.TeleBot(TOKEN)
r = requests.session()
user = user_agent.generate_user_agent()
DATA_FILE = 'dataSS.json'
sstop = "False"
# - - - - - - - - -  [ Func(s)]  - - - - - - - - - 
try:
    with open(DATA_FILE, 'r') as file:
        users_data = json.load(file)
except FileNotFoundError:
    users_data = {}
def save_data():
    with open(DATA_FILE, 'w') as file:
        json.dump(users_data, file, ensure_ascii=False, indent=4)

def process_problem_description(message):
    user_id = str(message.from_user.id)
    description = message.text
    if len(description) < 25:
        msg = bot.send_message(user_id, 'الرجاء إدخال وصف للمشكلة بطول لا يقل عن 25 حرفًا.')
        bot.register_next_step_handler(msg, process_problem_description)
    else:
        users_data[user_id] = users_data.get(user_id, {})
        users_data[user_id]['message'] = description
        save_data()
        bot.send_message(user_id, 'تم حفظ وصف المشكلة بنجاح.')
def process_phone_number(message):
    user_id = str(message.from_user.id)
    phone_number = message.text
def process_phone_number(message):
    user_id = str(message.from_user.id)
    phone_number = message.text
    if not re.match(r'^\+\d{10,15}$', phone_number):
        users_data[user_id]['number'] = " " 
        save_data()
        bot.send_message(user_id, 'لم يتم تحديد رقم الهاتف، تم تخزين القيمة الافتراضية بنجاح.')
    else:
        users_data[user_id]['number'] = phone_number
        save_data()
        bot.send_message(user_id, 'تم حفظ الرقم بنجاح.')

def check_and_execute(user_id):
    user_id = str(user_id)
    try:
        user_data = users_data.get(user_id, {})
        missing_elements = []
        if not user_data.get('message'):
            missing_elements.append(' وصف المشكلة ')
        if missing_elements:
            bot.send_message(user_id, f'الرجاء التأكد من تعيين جميع القيم. العناصر المفقودة: {", ".join(missing_elements)}.')
        else:
            msg = bot.send_message(user_id, 'الرجاء إرسال عدد البلاغات التي تريد ارسالها من كل ايميل . عزيزي المستخدم سوف يتم احتساب البلاغات الكلية بضرب عدد البلاغات التي ادخلتها في عدد الايميلات في الملف [ ادخل عدد بين 1 و 300 ]')
            bot.register_next_step_handler(msg, process_report_count)
    except Exception as e:
        print(f"خطأ في التحقق من البيانات: {e}")
        bot.send_message(user_id, 'حدث خطأ أثناء محاولة التحقق من البيانات.')

def process_report_count(message):
    try:
        report_count = int(message.text)
        if 1 <= report_count <= 300:
            execute_task(message.chat.id, report_count)
        else:
            bot.send_message(message.chat.id, 'الرجاء إرسال رقم صحيح بين 1 و 300.')
    except ValueError:
        bot.send_message(message.chat.id, 'الرجاء إرسال رقم صحيح.')
def extract_user_data(user_id):
    user_id = str(user_id)
    try:
        with open(DATA_FILE, 'r') as file:
            users_data = json.load(file)
        message = users_data.get(user_id, {}).get('message', 'لا توجد رسالة')
        phone_number = users_data.get(user_id, {}).get('number', 'لم يتم تحديد رقم الهاتف')
        
        return message, phone_number
    except FileNotFoundError:
        print("لم يتم العثور على ملف البيانات.")
        return None, None
    except json.JSONDecodeError:
        print("خطأ في تنسيق ملف JSON.")
        return None, None



def execute_task(user_id, count):
    global sstop
    user_message, user_phone_number = extract_user_data(user_id)

    success_count = 0
    fail_count = 0
    user_id = str(user_id)
    if not os.path.isfile(f'gmails{user_id}.txt'):
        bot.send_message(user_id, "قم بتعيين ملف الإيميلات أولا ")
        return
    with open(f'gmails{user_id}.txt', 'r') as file:
        emails = [email.strip() for email in file.readlines()]

    total_reports = len(emails) * count
    response = bot.send_message(user_id, f'بدء المهمة، العدد الإجمالي للتنفيذ: {total_reports}')
    message_id = response.message_id
    stop_button = types.InlineKeyboardMarkup()
    stop_button.add(types.InlineKeyboardButton('𝗦𝗧𝗢𝗣 ❌ ', callback_data='stop'))
    
    for i in range(count):
        if sstop == "True":
            sstop = "False"
            break
        for email in emails:
            if sstop == "True":
                break
            try:
	            cookies = {
	                'stel_ssid': '05454145b80ac88fd0_8875163941627286509',
	            }
	
	            headers = {
	                'authority': 'telegram.org',
	                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	                'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
	                'cache-control': 'max-age=0',
	                'content-type': 'application/x-www-form-urlencoded',
	                'origin': 'https://telegram.org',
	                'referer': 'https://telegram.org/support',
	                'sec-ch-ua': '"Not_A Brand";v="99", "Chromium";v="90"',
	                'sec-ch-ua-mobile': '?0',
	                'sec-ch-ua-platform': '"Windows"',
	                'sec-fetch-dest': 'document',
	                'sec-fetch-mode': 'navigate',
	                'sec-fetch-site': 'same-origin',
	                'sec-fetch-user': '?1',
	                'upgrade-insecure-requests': '1',
	                'user-agent': user,
	            }
	
	            data = {
	                'message': user_message,
	                'email': email,
	                'phone': user_phone_number,
	                'setln': '',
	            }
	
	            response = r.post('https://telegram.org/support', cookies=cookies, headers=headers, data=data)
	            if "شكر" in response.text:
	                success_count += 1
	            else:
	                fail_count += 1
            except Exception as e:
                bot.send_message(user_id, f'حدث خطأ: {e}')
                fail_count += 1
            bot.edit_message_text(f'عدد البلاغات الناجحة ✅ = {success_count}\nالفاشلة ❌ = {fail_count}\nالعدد الإجمالي للتنفيذ: {total_reports} \n البريد الإلكتروني الحالي {email}', user_id, message_id,reply_markup=stop_button)

    bot.send_message(user_id, f'تم الانتهاء بنجاح  أو تم الإبقاف ✅  وتم تنفيذ {success_count}')



@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global sstop
    user_id = call.from_user.id
    message = call.message  

    if call.data == "describe_problem":
        msg = bot.send_message(user_id, 'الرجاء وصف مشكلتك بالتفصيل.')
        bot.register_next_step_handler(msg, process_problem_description)
    elif call.data == "enter_number":
        msg = bot.send_message(user_id, 'الرجاء إدخال رقمك الخاص الذي يبدأ ب "+" ويحتوي على رمز دولة صحيح.')
        bot.register_next_step_handler(msg, process_phone_number)
    elif call.data == "start":
        check_and_execute(user_id)
    elif call.data == "email":
    	bot.send_message(user_id, " مرحبا قم بإرسال الملف الخاص بالبريد الإلكتروني وسيتم تعيينه بنجاح . ")
    elif call.data == "stop":
    	sstop = "True"
    	bot.edit_message_text(f" تم إيقاف المهمة بنجاح ، ", call.message.chat.id, call.message.message_id)
    else:
        bot.send_message(user_id, 'تم إكمال المهمة بنجاح.')
    


# معالجة الأوامر الخاصة بـ '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('أدخل وصف مشكلتك', callback_data='describe_problem')
    btn2 = types.InlineKeyboardButton('أدخل الرقم الخاص بك', callback_data='enter_number')
    btn3 = types.InlineKeyboardButton(" تحميل ملف البريد الإلكتروني ", callback_data='email')
    btn4 = types.InlineKeyboardButton('بدء التشغيل', callback_data='start')
    markup.add(btn1)
    markup.row(btn2)
    markup.row(btn3)
    markup.row(btn4)
    bot.send_message(message.chat.id, "مرحبا عزيزي، إختر من الأزرار أدناه", reply_markup=markup)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        if os.path.exists(f'gmail{chat_id}.txt'):
            os.remove(f'gmails{chat_id}.txt')
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f'gmails{chat_id}.txt', 'wb') as new_file:
            new_file.write(downloaded_file)
        with open(f'gmails{chat_id}.txt', 'r') as file:
            email_count = len(file.readlines())
        success_message = (
            "تم تعيين ملف الإيميلات بنجاح\n"
            f"عدد الإيميلات الموجودة بالملف = {email_count}\n" )
        bot.send_message(chat_id, success_message)
    
    except Exception as e:
        bot.send_message(chat_id, f"حدث خطأ: {e}")
bot_info = bot.get_me()
if bot_info.username:
    print(f"STARTED User Bot: @{bot_info.username}")
else:
    print("Unable to fetch bot username")
bot.polling(non_stop=True)
