st = {
	'new_login': "<b>⚠️ Hozirgina akkauntingizga ulanildi.</b>\n\n🔹Qurilma: <b>{device}</b>\n🔹Dastur: <b>{app}</b>\n\n<b>Akkauntingizga sizga berilgan TOKEN yordamida ulanildi.</b>"
}

def get_string(key='test'):
	if type(key) == str:
		return st.get(key, None)
	else:
		raise ValueError("You little shit! Give me string!")
