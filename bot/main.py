import os
import telebot
from resizevideo import Resize


token = '' # <--- bot token here

bot = telebot.TeleBot(token)
resize = Resize()

save_dir = 'video'
out_dir = 'output'

@bot.message_handler(commands=['start'])
def start(message):
	bot.send_chat_action(message.from_user.id, 'typing')
	bot.send_message(message.from_user.id, 'send me some video')


@bot.message_handler(commands=['help'])
def help(message):
	bot.send_chat_action(message.chat.id, 'typing')
	bot.send_message(message.chat.id, 'just send me some video or gif and you can see the result')


@bot.message_handler(content_types=['video', 'animation'])
def video_note(message):
	try:
		src = f'{message.chat.id}.mp4'
		
		try:
			file_id_info = bot.get_file(message.video.file_id)
			print("File is video")
		except:
			file_id_info = bot.get_file(message.animation.file_id)
			print("File is animation")
		
		bot.send_chat_action(message.chat.id, 'typing')
		sent_message = bot.send_message(message.chat.id, 'downloading file...')
		
		downloaded_file = bot.download_file(file_id_info.file_path)
		
		# save file to dir
		with open(f'{save_dir}/{src}', 'wb') as file:
			file.write(downloaded_file)

		bot.send_chat_action(message.chat.id, 'typing')
		bot.edit_message_text('resizing video...', message.chat.id, message_id=sent_message.message_id)
		
		# resize file
		resize.resize_video(path_from=f'{save_dir}/{src}', path_to=f"{out_dir}/{src}")

		bot.edit_message_text('sending video note...', message.chat.id, message_id=sent_message.message_id)
		bot.send_chat_action(message.chat.id, 'record_video')
		bot.send_video_note(message.chat.id, open(f"output/{message.chat.id}.mp4", 'rb'))
		
		# remove file
		
		os.system(f'rm {out_dir}/{src}')
		
		bot.edit_message_text('Done!', message.chat.id, message_id=sent_message.message_id)
	except Exception as ex:
		print(f'VIDEO NOTE EXCPET\n{ex=}')
		bot.send_message(message.chat.id, "Something went wrong. Please try again later.")


bot.polling(none_stop=True, interval=0)