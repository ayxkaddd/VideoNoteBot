import os


class Resize:

	# def __init__(self, path_from, path_to):
	# 	self.path_from = path_from
	# 	self.path_to = path_to


	def resize_video(self, path_from, path_to):
		command = f"ffmpeg -i {path_from} -vf scale=460:460 {path_to}"
		os.system(f"{command}")
		os.system(f"rm {path_from}")
