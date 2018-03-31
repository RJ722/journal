NAME = 'Rahul Jha'
IMAGE = 'https://user-images.githubusercontent.com/15556382/38166660-32f47482-3545-11e8-967a-5e15a3474eae.jpeg'


class Author:
	def __init__(self, name, image):
		self.name = name
		self.image = image


author = Author(NAME, IMAGE)
