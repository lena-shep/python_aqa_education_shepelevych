import re
# print(help(re))

find = []
for word in dir(re):
    if "find" in word:
        find.append(word)

print(sorted(find))

# import time
#
# print(time.time())

# from time import ctime
#
# print(ctime())

# from datetime import date, time, datetime
#
# print(datetime.today())

# import os
# #
# print(os.name)
#
# import sys
#
# print(sys.argv)
#
# f = open('test.txt')
#
# print(f.read())
#
# f = open("test.txt", "w")
# f.write("new test")
# f.close()

