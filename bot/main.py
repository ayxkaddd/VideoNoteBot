import os
import telebot
from resizevideo import Resize

token = ''

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def start(message):
	bot.send_chat_action(message.from_user.id, 'typing')
	bot.send_message(message.from_user.id, 'send me some video')


@bot.message_handler(content_types=['video'])
def video_note(message):
	try:
		save_dir = 'video'
		file_id_info = bot.get_file(message.video.file_id)
		bot.send_chat_action(message.chat.id, 'typing')
		sent_message = bot.send_message(message.chat.id, 'download file...')
		downloaded_file = bot.download_file(file_id_info.file_path)
		src = f'{message.chat.id}.mp4'

		with open(f'{save_dir}/{src}', 'wb') as new_file:
			new_file.write(downloaded_file)

		bot.send_chat_action(message.chat.id, 'typing')
		bot.edit_message_text('resize video...', message.chat.id, message_id=sent_message.message_id)
		out_dir = f'output/{src}'
		resize = Resize(path_from=f'{save_dir}/{src}', path_to=out_dir)
		resize.res_video()
		bot.edit_message_text("[*] File added:\nFile name - {}\ntype /send_video_note".format(src), message.chat.id, message_id=sent_message.message_id)
	except Exception as ex:
		print(f'VIDEO NOTE EXCPET\n{ex=}')


@bot.message_handler(commands=['send_video_note'])
def send_video_note(message):
	try:
		path = f'output/{message.chat.id}.mp4'
		bot.send_message(message.chat.id, 'wait...')
		file = open(path, 'rb')
		bot.send_chat_action(message.chat.id, 'record_video')
		bot.send_video_note(message.chat.id, file)
		os.system(f'rm {path}')
	except Exception as ex:
		bot.send_message(message.chat.id, f'except - {ex}')


bot.polling(none_stop=True, interval=0)
