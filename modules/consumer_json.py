import os
import json

class ConsumerJson():

	def __init__(self, path, file_name):
		self._path = path
		self._file_name = file_name


	def consumer_json(self):

		if not os.path.exists(self._path):
			print("Failed, path: %s don't exists" % self._path)
			return

		path = os.path.join(self._path, self._file_name)
		
		data = ""

		try :
			
			f = open(path, "r")
			data = json.load(f)

		except FileNotFoundError as e:
			print(e)
		else:
			f.close()

		return data 

if __name__ == "__main__":

	cj = ConsumerJson("credential", "google-search.json")
	data = cj.consumer_json()

	print(data)
