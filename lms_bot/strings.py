# coding: utf-8
# Just strings, no freaking UNICODE error anymore, we'll use Python 3 this time.

st = {
	'test': "Hola vuala!",
	'first_start': "Ukki X ga xush kelibsiz!\n\nXo'sh, eng avval qiladigan ish - bu siz bilan kelishuv. /terms buyrug'idan foydalaning, qolgan ishlar keyin hal bo'ladi.",
	'start': [
		'Oq rang aslidayam oqmi?', 
		"Kechasi uxlashga yotganda sizdayam soatlab shiftga qarab yotib, uxlolmaslik kasalligi bormi?", 
		"Nima endi bu?", 
		"Qalamimni uchi sindi, qalam ochgich qani endi...", 
		"Nega chap qo'lim o'ng tomonda joylashmagan, agar u o'ng tomonda joylashganida u haliyam chap qo'lim bo'lib qolarmidi yo... ha mayli.",
		"Chap ko'zingizni qising, endi u bilan ekranga qarang. Nimadir xatomi 🤔",
		"Ehh, ha mayli...",
		"👀",
		"Kecha yotuvdim, uxlab qoldim.",
	],
	'terms': "Bu endi shunchaki login/parol masalasi emas, shaxsiy axborot dahlsizligi o'rtada turibdi.\nSiz bizga jo'natgan login/parollaringiz serverimizda saqlanadi va LMS saytidan ma'lumotlarni olish uchun ishlatiladi.\nLogin/parolingiz hech kimga berilmaydi, tarqatilmaydi.\n\nAgar siz login/parolingiz bizda saqlanishiga rozi bo'lsangiz, davom eting, aks holda dasturdan foydalanmang.\n\nRo'yxatdan o'tish uchun /reg komandasidan foydalaning",
	
	'registration': "🔹 lms.tuit.uz saytidagi login va parolingizni jo'nating, ularni probel bilan ajratib yozing. Masalan: <code>a.valiyev test12</code>",
	'reg_logging': "⏰ Ulanilmoqda...",
	'reg_logged_successfully': "<b>{name} sifatida ro'yxatdan o'tildi</b> ✅\n\nTOKEN olish uchun /token komandasini jo'nating",
	'reg_wrong_credentials': "<b>Login yoki parol xato, qayta urinib ko'ring</b> ❌",
	'reg_invalid_input': "Hey! Mana bunaqa tarzda kiriting: <code>login parol</code>\nMasalan, <code>a.valiyev test12</code>",
	'reg_fatal_error': "Login paytida LMS kutilganidek ishlamadi, qayta urinib ko'ring.",
	'reg_check_credentials': "⭕️ <b>Tekshirib ko'ring, bular to'g'rimi?</b>\n\n<b>Login:</b> <code>{login}</code>\n<b>Parol:</b> <code>{password}</code>",
	'reg_check_credentials_yes_button': "To'g'ri ✅",
	'reg_check_credentials_no_button': "Xato ❌",
	'reg_check_credentials_retry': "Login va parolingizni ehtiyotkorlik bilan tekshirib, qaytadan kiriting",
	'reg_click_to_finish': "<b>🔹 Ro'yxatdan o'tishni to'liq yakunlash uchun tugmani bosing</b>\n\nUkki X dasturini o'rnatganmisiz? Agar o'rnatgan bo'lsangiz, pastdagi tugmani bosing, aks holda avvall dasturni o'rnating, keyin tugmani bosing.",

	'deep_linking_login_success': "Pastdagi tugmani bosing",
	'deep_linking_login_success_button': "Ulanish",

	'friends_searching':"🔎 <b>Do'stlar qidirilmoqda...</b>",
	'friends_result': '<a href="{link}">{name} - do\'stlar</a>\n\n📊<code> Qidiruvga {search_time:.2f} soniya vaqt sarflandi</code>',
	'friends_search_completed': "📝 Qidiruv yakunlandi. Sahifa tayyorlanmoqda...",
	'friends_unknown_or_restricted_account': "⭕️ {name}",
	'friends_unknown_key': "unkown",

	'files_searching': "🔎 Fayl qidirilmoqda, iltimos kuting...",
	'files_sending': "File sizga jo'natilmoqda...",
	'files_file_ready': "Faylingiz tayyor, yoqimli ishtaha ✅",
	'files_caption': "#ukki #file #{}\n#ukki_file",
	'files_not_found': "Faylingizni LMS dan topa olmadim :(",
	'files_not_functioning': "Fayl yuklab olish vaqtincha ishlamaydi, yangi versiyani kuting.",
	'files_file_dl_error': "Faylni LMS dan yuklab olishda xatolik kelib chiqdi :(",

	'token_info': "Ushbu tokendan Ukki Android dasturida ro'yxatdan o'tishda foydalanishingiz mumkin. Iltimos, uni boshqalarga bermang, tokeningiz orqali akkauntingizga ulanish mumkin.\n\n<code>{token}</code>",
	'not_authorized': "Siz ro'yxatdan o'tmagansiz, /reg komandasini sinab ko'ring",
	
	'tg_profile': '🎓 <a href="tg://user?id={tg_id}">{name}</a>',
	'tg_profile_only_girls': "Yaxshi va yomon yigitlani profiliga sizi ulab beromiman, dugonalarizdan birortasini tanlang :)",
	'tg_profile_only_boys': "Uzr akasi, qizlani profiliga ulab beromiman, o'lay agar, juda noqulay...",
	'tg_profile_target_not_found': "Negadir bu odamni Telegramdan qidirib topa olmadim. Balki ro'yxatdan o'tishga ulgurmagandir hali?",

	'user_information': "<b>🎓 {name}</b>\n\n🔵 <b>Telegram profillaringiz:</b>\n 🔹 {telegram_accounts}\n\n📱 <b>Qurilmalaringiz:</b> \n 🔹 {devices}",

	'user_info_list_item_telegram_account': '<a href="tg://user?id={tg_id}">{tg_acc_name}</a> \n        <code>{login_time}</code>',
	'user_info_list_item_device': '{device}\n        <code>{login_time}</code>',
	'user_info_list_item_device_not_found': "qurilmalar topilmadi",
	
	'added_new_notification': "Notification qo'shildi:\n<b>{title}</b>\n\n {data}\n\n <i>{notifier}</i>",
	'wrong_notification_format': "Noto'g'ri format, mana bundan foydalaning: TITLE\n<->\nDATA\n<->\nNOTIFIER",
	'notifications_list': "{nid}: {title}\n",
	'notification_deleted': "Bildirishnoma o'chirildi",

	'user_not_permitted': "Ukki ilovasidan foydalanish ayni paytda faqat beta testerlarga ruxsat berilgan, beta tester sifatida qo'shilish uchun @UkkiChatda #ukki_hero heshtegini yozib qoldiring",

	'command_restricted_in_group': "Bu komanda guruhda ishlatish uchun taqiqlangan",
	'privacy_token_revoked': "⚠️ <b>Xavfsizlik bildirishnomasi</b>\n\n{name} nomidagi akkauntning tokeni yangilandi. Mavjud akkauntga ulangan barcha qurilma va Telegram akkauntlardan foydalanish huquqi dominant akkaunt tomonidan bekor qilindi.\n\nUkki X mobil dasturida yangi token yordamida qaytadan ro'yxatdan o'tishingiz zarur.\n\n🔵 Dominant akkaunt - LMS akkauntiga 'Ukki'da eng birinchi ro'yxatdan o'tgan Telegram akkaunt. Mavjud dominant akkaunt tizimdan chiqqan, yoki boshqa bir LMS akkauntga ulangan paytda dominantlik huquqi undan keyin ulangan navbatdagi akkauntga o'tkaziladi.",
	'privacy_not_dominant_account': "Ushbu Telegram akkaunt dominant emas. Tokenni yangilash huquqi faqat dominant akkauntga beriladi.\n\n🔵 Dominant akkaunt - LMS akkauntiga 'Ukki'da eng birinchi ro'yxatdan o'tgan Telegram akkaunt. Mavjud dominant akkaunt tizimdan chiqqan, yoki boshqa bir LMS akkauntga ulangan paytda dominantlik huquqi undan keyin ulangan navbatdagi akkauntga o'tkaziladi.",
	'privacy_token_not_exist': "Akkaunt topilmadi",

	'emoji_boy': "🙎🏻‍♂️",
	'emoji_girl': "🙎🏻‍♀️",
	'emoji_hat': "🎓",
	'emoji_stats': "📊",
	'emoji_search': "🔎",
	'emoji_recycle': "♻️",

	'fatal_eror': "Kutilmagan xatolik yuz berdi"
}

def get_string(key='test'):
	if type(key) == str:
		return st.get(key, None)
	else:
		raise ValueError("You little shit! Give me string!")