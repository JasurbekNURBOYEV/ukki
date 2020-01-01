# coding: utf-8
# My DreamGraph handles all the trouble here, if you see an error, let's pretend you didn't, thank you.

from dreamgraph import LogIn
import base64
from strings import get_string

token = "f8b8b79df9d38e8da49ab9adc8590f2fdfa4dccfa6712dcca319caf4ed7e"
client = LogIn(token)

# create new pages
def create_new_page(content, title, author_name=None, author_url=None):
	page = client.create_page(title, content, author_url, author_name)
	return page.url

def generate_friends_page(user_id, friends_data):
	print("TELEGRAPH: " + str(friends_data))
	names = friends_data['all_friends']
	sum_of_friends = len(names)-1
	page_data = [{'tag': 'pre', 'children': [{'tag': 'b', 'children': ['{} Jami {} ta do\'stlar topildi'.format(get_string('emoji_stats'), sum_of_friends)]}]}]
	for stream in list(friends_data.keys())[1:]:
		number_of_stream_friends = len(friends_data[stream])
		if number_of_stream_friends > 0:
			page_data.append({'tag': 'pre', 'children': [{'tag': 'b', 'children': ['🔵 {} - {} ta'.format(stream, number_of_stream_friends)]}]})
			boys = []
			girls = []
			for f in friends_data[stream]:
				if names.get(user_id.user_id, None) != names.get(f, None):
					if (names.get(f, '').split()[0].endswith("a")):
						girls.append(f)
					else:
						boys.append(f)
			if names[user_id.user_id].split()[0].endswith("a"):
				for girl in sorted(girls):
					if names[girl].startswith(get_string('friends_unknown_key')):
						name = get_string('friends_unknown_or_restricted_account').format(name=names[girl].replace(get_string('friends_unknown_key'), '', 1))
						page_data.append({'tag': 'p', 'children': ['   {} {}'.format(get_string('emoji_girl'), name)]})
					else:	
						page_data.append({'tag': 'p', 'children': ['   {} '.format(get_string('emoji_girl')), {'tag': 'a', 'attrs': {'href': 'tg://resolve/?domain=UkkiXbot&start={}'.format(base64.b64encode('sp{}_{}'.format(girl, names[girl].replace(' ', '_')).encode()).decode())}, 'children': ['{}'.format(names[girl])]}]})
				for boy in sorted(boys):
					if names[boy].startswith(get_string('friends_unknown_key')):
						name = get_string('friends_unknown_or_restricted_account').format(name=names[boy].replace(get_string('friends_unknown_key'), '', 1))
						page_data.append({'tag': 'p', 'children': ['   {} {}'.format(get_string('emoji_boy'), name)]})
					else:
						page_data.append({'tag': 'p', 'children': ['   {} '.format(get_string('emoji_boy')), {'tag': 'a', 'attrs': {'href': 'tg://resolve/?domain=UkkiXbot&start={}'.format(base64.b64encode('sp{}_{}'.format(boy, names[boy].replace(' ', '_')).encode()).decode())}, 'children': ['{}'.format(names[boy])]}]})
			else:
				for boy in sorted(boys):
					if names[boy].startswith(get_string('friends_unknown_key')):
						name = get_string('friends_unknown_or_restricted_account').format(name=names[boy].replace(get_string('friends_unknown_key'), '', 1))
						page_data.append({'tag': 'p', 'children': ['   {} {}'.format(get_string('emoji_boy'), name)]})
					else:
						page_data.append({'tag': 'p', 'children': ['   {} '.format(get_string('emoji_boy')), {'tag': 'a', 'attrs': {'href': 'tg://resolve/?domain=UkkiXbot&start={}'.format(base64.b64encode('sp{}_{}'.format(boy, names[boy].replace(' ', '_')).encode()).decode())}, 'children': ['{}'.format(names[boy])]}]})
				for girl in sorted(girls):
					if names[girl].startswith(get_string('friends_unknown_key')):
						name = get_string('friends_unknown_or_restricted_account').format(name=names[girl].replace(get_string('friends_unknown_key'), '', 1))
						page_data.append({'tag': 'p', 'children': ['   {} {}'.format(get_string('emoji_girl'), name)]})
					else:	
						page_data.append({'tag': 'p', 'children': ['   {} '.format(get_string('emoji_girl')), {'tag': 'a', 'attrs': {'href': 'tg://resolve/?domain=UkkiXbot&start={}'.format(base64.b64encode('sp{}_{}'.format(girl, names[girl].replace(' ', '_')).encode()).decode())}, 'children': ['{}'.format(names[girl])]}]})

	return create_new_page(page_data, "{} {} - do'stlar".format(get_string('emoji_hat'), friends_data['all_friends'][user_id.user_id]))