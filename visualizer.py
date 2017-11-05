#use matplotlib to visualize it
#data in the form of simple axes

import matplotlib.pyplot as plt

class Visualizer:
	def __init__(self):
		print "Hello from initialiser"

	'''
	@data - data to be visualized in list comprehension form
	'''
	def visualize(self, data):
		plt.plot([1,2,3,4])
		plt.ylabel('y axis')
		plt.show()

	
