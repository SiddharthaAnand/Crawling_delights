import visualizer
import json
import os

class ReadJson:
	def __init__(self):
		self.data = {}

	def read_json(self, filename):
		cwd = os.getcwd()
		if os.path.isfile(cwd + filename):
			with open(filename) as json_data:
				self.data = json.load(json_data)

		return self.data
		
	def convert_json_to_list(self):
		if len(self.data) != 0:
			for roll in self.data:
				
