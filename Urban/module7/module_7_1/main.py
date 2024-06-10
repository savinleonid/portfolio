"""File read test with preloaded test.txt file"""

from pprint import pprint

file = open("test.txt", mode="r", encoding="utf8")  # open file in read mode with utf8 encoding
file_content = file.read()  # reads whole content including encoding title and special characters
file.close()  # close file

pprint(file_content)  # pprint library for easy readable layout
