# Code & Req By @Sami3D
import telebot,os, time
from telebot import types
import json
import random
import string
import re
import requests,user_agent
# - - - - - - - - -  [ Bot & Others ]  - - - - - - - - - 
TOKEN = '7202513885:AAENYe5rVv-Jhqx-PiD0yEDIpbSt37sMezg'
OID = 707679061
bot = telebot.TeleBot(TOKEN)
r = requests.session()
user = user_agent.generate_user_agent()
DATA_FILE = 'dataSS.json'
sstop = "False"
from datetime import datetime, timedelta
if os.path.exists('Ids.txt'):
    os.remove('Ids.txt')
    print('تم حذف ملف التخزين النصي القديم.')
if not os.path.exists('Ids.json'):
    ids_data = {
        str(OID): {
            'subscription_end': (datetime.now() + timedelta(days=380*365)).strftime('%Y-%m-%d')
        }
    }
    with open('Ids.json', 'w') as json_file:
        json.dump(ids_data, json_file, ensure_ascii=False, indent=4)
    print('تم إنشاء ملف التخزين JSON وتفعيل اشتراك لمدة 380 سنة للمالك.')
else:
    print('ملف التخزين JSON موجود بالفعل.')
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
# - - - - - - - - -  [ ]  - - - - - - - - - 
def list_subscribers(message):
    try:
        with open('Ids.json', 'r') as file:
            ids_data = json.load(file)

        if ids_data:
            subscribers = "\n".join([f"User ID: {user_id}, Subscription End: {data['subscription_end']}" for user_id, data in ids_data.items()])
            bot.send_message(message.chat.id, f'قائمة المشتركين  :  \n{subscribers}')
        else:
            bot.send_message(message.chat.id, 'لا يوجد مشتركين. ❌')
    except FileNotFoundError:
        bot.send_message(message.chat.id, 'ملف التخزين غير موجود. ❌')
# - - - - - - - - -  [ ]  - - - - - - - - - 
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != OID:
        bot.reply_to(message, 'You are not authorized to use this command. ❌')
        return

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('إضــافة اشـتـراك (➕)', callback_data='add_subscription')
    btn2 = types.InlineKeyboardButton('حـذف اشتـراك (➖)', callback_data='remove_subscription')
    btn3 = types.InlineKeyboardButton('عرض قائمة المشتركين (👤)', callback_data='list_subscribers')
    markup.add(btn1)
    markup.row(btn2)
    markup.row(btn3)
    bot.send_message(message.chat.id, "مـࢪحبا ! طاب يومك ، أنا هنا لخدمتك في إدارتي 🇵🇸", reply_markup=markup)
# - - - - - - - - -  [ ]  - - - - - - - - - 

def remove_vip(message):
    user_id = message.text
    try:
        with open('Ids.json', 'r') as file:
            ids_data = json.load(file)

        if user_id in ids_data:
            del ids_data[user_id]
            with open('Ids.json', 'w') as file:
                json.dump(ids_data, file, ensure_ascii=False, indent=4)
            bot.reply_to(message, f'تم حذف معرف المستخدم: {user_id} بنجاح 🗑️')
        else:
            bot.reply_to(message, f'لم يتم العثور على معرف المستخدم: {user_id}. ❌')
    except FileNotFoundError:
        bot.reply_to(message, 'ملف التخزين غير موجود. ❌')
# - - - - - - - - -  [ ]  - - - - - - - - - 

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
    
    # قراءة مدة time.sleep من ملف JSON
    data = {}
    time_sleep = 20  # قيمة افتراضية
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
        if str(user_id) in data and 'time_sleep' in data[str(user_id)]:
            time_sleep = data[str(user_id)]['time_sleep']
    
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
            bot.edit_message_text(f'عدد البلاغات الناجحة ✅ = {success_count}\nالفاشلة ❌ = {fail_count}\nالعدد الإجمالي للتنفيذ: {total_reports} \n البريد الإلكتروني الحالي {email}', user_id, message_id, reply_markup=stop_button)
            time.sleep(time_sleep)

    bot.send_message(user_id, f'تم الانتهاء بنجاح أو تم الإيقاف ✅ وتم تنفيذ {success_count}')



@bot.message_handler(commands=['vip'])
def vip(message):
    if message.from_user.id != OID:
        bot.reply_to(message, 'You are not authorized to use this command. ❌')
        return

    s = message.text.split(' ')
    if len(s) > 1:
        user_id = s[1]

        msg = bot.send_message(message.chat.id, 'الرجاء إدخال مدة الاشتراك (بالأيام):')
        bot.register_next_step_handler(msg, lambda msg: set_vip_duration(user_id, msg))
    else:
        bot.reply_to(message, 'يرجى تقديم معرف المستخدم. ❌')

def set_vip_duration(user_id, message):
    try:
        duration_days = int(message.text)
        subscription_end = datetime.now() + timedelta(days=duration_days)

        try:
            with open('Ids.json', 'r') as file:
                ids_data = json.load(file)
        except FileNotFoundError:
            ids_data = {}

        ids_data[user_id] = {
            'subscription_end': subscription_end.strftime('%Y-%m-%d')
        }

        with open('Ids.json', 'w') as file:
            json.dump(ids_data, file, ensure_ascii=False, indent=4)

        bot.reply_to(message, f'تم إضافة معرف المستخدم: {user_id} بنجاح مع اشتراك لمدة {duration_days} يومًا ✅')
    except ValueError:
        bot.reply_to(message, 'الرجاء إدخال عدد صحيح من الأيام. ❌')

@bot.message_handler(commands=['disvip'])
def disvip(message):
    if message.from_user.id != OID:
        bot.reply_to(message, 'You are not authorized to use this command. ❌')
        return

    s = message.text.split(' ')
    if len(s) > 1:
        user_id = s[1]
        try:
            with open('Ids.json', 'r') as file:
                ids_data = json.load(file)

            if user_id in ids_data:
                del ids_data[user_id]

                with open('Ids.json', 'w') as file:
                    json.dump(ids_data, file, ensure_ascii=False, indent=4)

                bot.reply_to(message, f'User ID: {user_id} removed successfully 🗑️')
            else:
                bot.reply_to(message, f'User ID: {user_id} not found. ❌')

        except FileNotFoundError:
            bot.reply_to(message, 'The file does not exist. ❌')
    else:
        bot.reply_to(message, 'Please provide a user ID. ❌')

# - - - - - - - - -  [ ]  - - - - - - - - - 
from datetime import datetime, timedelta

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    try:
        with open('Ids.json', 'r') as file:
            ids_data = json.load(file)
        
        user_info = ids_data.get(user_id)
        if user_info:
            subscription_end = datetime.strptime(user_info['subscription_end'], '%Y-%m-%d')
            if datetime.now() < subscription_end:
                markup = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton('أدخل وصف مشكلتك', callback_data='describe_problem')
                btn2 = types.InlineKeyboardButton('أدخل الرقم الخاص بك', callback_data='enter_number')
                btn3 = types.InlineKeyboardButton("تحميل ملف البريد الإلكتروني", callback_data='email')
                btn4 = types.InlineKeyboardButton('بدء التشغيل', callback_data='start')
                btn5 = types.InlineKeyboardButton(' تعييـن الوقـت الفاصـل ⌚',callback_data = 'set_time')
                markup.add(btn1)
                markup.row(btn2)
                markup.row(btn3)
                markup.row(btn4)
                markup.row(btn5)
                bot.send_message(message.chat.id, f'''↫ مـࢪحباً بك عزيزي  ،   أنا روبوت تيليجࢪام متطور 

  ↫ وظيفتي بسيطة وهي  :  "مساعدتك في إزالة قيودك على تيليجࢪام - ورفع بلاغات على الجروبات والقنوات المخالفه

  ↫ لا  داعي للتعب بعد الان
  ↬ 𝗬َِ𝗼َِ𝘂َِ𝗿 َِ𝗜َِ𝗱 َِ𝘁َِ𝗲َِ𝗹َِ𝗲 َِ𝗮َِ𝗰َِ𝗰َِ𝗼َِ𝘂َِ𝗻َِ𝘁   ↬ {user_id}

 ↫ مـالك البـوت  :   الـقـيادة قـاهـر التعزي (@kaher_01)''', reply_markup=markup)
            else:
                bot.send_message(message.chat.id, 'انتهت صلاحية اشتراكك. راسل المالك لتجديد الاشتراك :  الـقـيـادة قـاهـر التعزي (@kaher_01)')
        else:
            bot.send_message(message.chat.id, 'ليس لديك اشتراك نشط. راسل المالك للحصول على اشتراك :  الـقـيـادة قـاهـر التعزي (@kaher_01)')
    except FileNotFoundError:
        bot.send_message(message.chat.id, 'لا يوجد ملف بيانات المستخدمين. راسل المالك للحصول على اشتراك :  الـقـيـادة قـاهـر التعزي (@kaher_01)')
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global sstop
    user_id = call.from_user.id
    message = call.message

    if call.data == "describe_problem":
        msg = bot.send_message(user_id, 'الرجاء وصف مشكلتك بالتفصيل.')
        bot.register_next_step_handler(msg, process_problem_description)
    elif call.data == "enter_number":
        msg = bot.send_message(user_id, 'الرجاء إدخال رقمك الخاص الذي يبدأ ب "+" ويحتوي رمز دولة صحيح.')
        bot.register_next_step_handler(msg, process_phone_number)
    elif call.data == "start":
        check_and_execute(user_id)
    elif call.data == "email":
        bot.send_message(user_id, " مرحبا قم بإرسال الملف الخاص بالبريد الإلكتروني وسيتم تعيينه بنجاح . ")
    elif call.data == "stop":
        sstop = "True"
        bot.edit_message_text(f" تم إيقاف المهمة بنجاح ، ", call.message.chat.id, call.message.message_id)
    elif call.data == "set_time":
        msg = bot.send_message(user_id, 'الرجاء إدخال مدة الـ time.sleep (بالثواني):')
        bot.register_next_step_handler(msg, set_time_sleep)
    elif call.data == "add_subscription":
        msg = bot.send_message(call.message.chat.id, 'الرجاء إدخال معرف المستخدم:')
        bot.register_next_step_handler(msg, ask_for_duration)
    elif call.data == "remove_subscription":
        msg = bot.send_message(call.message.chat.id, 'الرجاء إدخال معرف المستخدم:')
        bot.register_next_step_handler(msg, remove_vip)
    elif call.data == "list_subscribers":
        list_subscribers(call.message)
    else:
        bot.send_message(user_id, 'تم إكمال المهمة بنجاح.')

def set_time_sleep(message):
    try:
        time_sleep = int(message.text)
        user_id = str(message.chat.id)
        data = {}
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                data = json.load(file)
        
        if user_id not in data:
            data[user_id] = {}
        
        data[user_id]['time_sleep'] = time_sleep
        
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        bot.send_message(message.chat.id, f'تم تعيين مدة time.sleep إلى {time_sleep} ثانية بنجاح.')
    except ValueError:
        bot.send_message(message.chat.id, 'الرجاء إدخال عدد صحيح من الثواني.')
# - - - - - - - - -  [ ]  - - - - - - - - - 

def ask_for_duration(message):
    user_id = message.text
    msg = bot.send_message(message.chat.id, 'الرجاء إدخال مدة الاشتراك (بالأيام):')
    bot.register_next_step_handler(msg, lambda msg: set_vip_duration(user_id, msg))

def set_vip_duration(user_id, message):
    try:
        duration_days = int(message.text)
        subscription_end = datetime.now() + timedelta(days=duration_days)

        try:
            with open('Ids.json', 'r') as file:
                ids_data = json.load(file)
        except FileNotFoundError:
            ids_data = {}

        if user_id in ids_data:
            current_end_date = datetime.strptime(ids_data[user_id]['subscription_end'], '%Y-%m-%d')
            new_end_date = current_end_date + timedelta(days=duration_days)
            ids_data[user_id]['subscription_end'] = new_end_date.strftime('%Y-%m-%d')
        else:
            ids_data[user_id] = {
                'subscription_end': subscription_end.strftime('%Y-%m-%d')
            }

        with open('Ids.json', 'w') as file:
            json.dump(ids_data, file, ensure_ascii=False, indent=4)

        bot.reply_to(message, f'تم إضافة/تجديد اشتراك معرف المستخدم: {user_id} بنجاح لمدة {duration_days} يومًا ✅')
    except ValueError:
        bot.reply_to(message, 'الرجاء إدخال عدد صحيح من الأيام. ❌')
# - - - - - - - - -  [ ]  - - - - - - - - - 
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