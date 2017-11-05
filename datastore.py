import pickle

FILENAME = "cbse_data"
def pickle_it(data, file_name):

	with open(file_name, 'wb') as fh:
		pickle.dump(data, fh)

def unpickle_it(file_name):
	with open(file_name, 'rb') as fh:
		data = pickle.loads(fh.read())
	return data