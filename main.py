import telebot
from instagrapi import Client
import os
import time
import threading

# بيانات معتصم (mo_t911)
IG_USERNAME = "mo_t911"
IG_PASSWORD = "qweasdzxc14"
TELE_TOKEN = "8669040233:AAGvN22_WUHfQ5OkhtS_F9q0DRbN0G1hOls"

cl = Client()

def login_ig():
    try:
        print("جاري محاولة الدخول لإنستجرام من سيرفر Railway... ⏳")
        # تعيين هوية موبايل لتجنب الحظر
        cl.set_device({
            "app_version": "269.0.0.18.75",
            "android_version": 26,
            "android_release": "8.0.0",
            "device_model": "SM-G960F",
            "device_brand": "samsung",
        })
        cl.login(IG_USERNAME, IG_PASSWORD)
        print("تم الاتصال بنجاح يا معتصم! ✅")
    except Exception as e:
        print(f"فشل الدخول: {e}")
        print("تنبيه: افتح تطبيق إنستا في جوالك واضغط 'هذا أنا' إذا ظهرت.")

login_ig()

# ميزة الرد الآلي المخصص لمعتصم
def auto_reply():
    replied = []
    print("نظام الرد الآلي شغال... 🤖")
    while True:
        try:
            threads = cl.direct_threads(amount=3)
            for thread in threads:
                user_id = thread.users[0].pk
                # التأكد أن الرسالة ليست من معتصم نفسه ولم يتم الرد عليها سابقاً
                if not thread.messages[0].is_sent_by_viewer and user_id not in replied:
                    cl.direct_send("أهلاً وسهلاً 👋\nمعك الرد الآلي لمعتصم، شوي وبيرد عليك.", [user_id])
                    replied.append(user_id)
                    print(f"تم الرد آلياً على: {thread.users[0].username}")
            time.sleep(60) # فحص كل دقيقة
        except Exception as e:
            print(f"خطأ في الرد الآلي: {e}")
            time.sleep(120)

# تشغيل الرد الآلي في خلفية السيرفر
threading.Thread(target=auto_reply, daemon=True).start()

# إعداد بوت تليجرام لرفع الستوري
bot = telebot.TeleBot(TELE_TOKEN)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # إذا أرسلت صورة ومعها كلمة "ستوري" في الوصف
    if message.caption and "ستوري" in message.caption:
        try:
            bot.reply_to(message, "جاري رفع الصورة لستوري إنستجرام... 🔄")
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            file_name = "story_upload.jpg"
            with open(file_name, "wb") as new_file:
                new_file.write(downloaded_file)
            
            # رفع الصورة للستوري
            cl.photo_upload_to_story(file_name)
            bot.reply_to(message, "تم رفع الستوري بنجاح يا معتصم! 🎊✅")
            os.remove(file_name) # حذف الملف المؤقت
        except Exception as e:
            bot.reply_to(message, f"حدث خطأ أثناء الرفع: {e}")

print("Shadow King Bot is Running on Railway... 🚀")
bot.polling(none_stop=True)
