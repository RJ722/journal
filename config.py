NAME = 'Kenneth Reitz'
IMAGE = 'https://d3vv6lp55qjaqc.cloudfront.net/items/0m3c0f2C0k3K1L2Z3R1r/kr.svg?X-CloudApp-Visitor-Id=2577'


class Author:
	def __init__(self, name, image):
		self.name = name
		self.image = image


author = Author(NAME, IMAGE)
