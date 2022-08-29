import telebot
import os
from resizevideo import Resize


token = '' # <--- bot token here

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
	bot.send_chat_action(message.from_user.id, 'typing')
	bot.send_message(message.from_user.id, 'send me some video')


@bot.message_handler(commands=['help'])
def help(message):
	bot.send_chat_action(message.chat.id, 'typing')
	bot.send_message(message.chat.id, 'just send me some video or gif and you can see the result')


@bot.message_handler(content_types=['video'])
def video_note(message):
	try:
		save_dir = 'video'
		file_id_info = bot.get_file(message.video.file_id)
		bot.send_chat_action(message.chat.id, 'typing')
		sent_message = bot.send_message(message.chat.id, 'download file...')
		downloaded_file = bot.download_file(file_id_info.file_path)
		src = f'{message.chat.id}.mp4'
		# save file to dir
		with open(f'{save_dir}/{src}', 'wb') as new_file:
			new_file.write(downloaded_file)

		bot.send_chat_action(message.chat.id, 'typing')
		bot.edit_message_text('resize video...', message.chat.id, message_id=sent_message.message_id)
		out_dir = f'output/{src}'
		# resize this file
		resize = Resize(path_from=f'{save_dir}/{src}', path_to=out_dir)
		resize.resize_video()
		path = f'output/{message.chat.id}.mp4'
		bot.edit_message_text('sends video note...', message.chat.id, message_id=sent_message.message_id)
		file = open(path, 'rb')
		bot.send_chat_action(message.chat.id, 'record_video')
		bot.send_video_note(message.chat.id, file)
		# remove file
		os.system(f'rm {path}')
		bot.edit_message_text('Done!', message.chat.id, message_id=sent_message.message_id)
	except Exception as ex:
		print(f'VIDEO NOTE EXCPET\n{ex=}')


@bot.message_handler(content_types=['animation'])
def video_note_animation(message):
	try:
		save_dir = 'video'
		file_id_info = bot.get_file(message.animation.file_id)
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
		resize.resize_video()
		path = f'output/{message.chat.id}.mp4'
		bot.edit_message_text('sends video note...', message.chat.id, message_id=sent_message.message_id)
		file = open(path, 'rb')
		bot.send_chat_action(message.chat.id, 'record_video')
		bot.send_video_note(message.chat.id, file)
		os.system(f'rm {path}')
		bot.edit_message_text('Done!', message.chat.id, message_id=sent_message.message_id)
	except Exception as ex:
		print(f'VIDEO NOTE EXCPET\n{ex=}')


bot.polling(none_stop=True, interval=0)
