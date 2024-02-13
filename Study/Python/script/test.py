# import time

# nowtime = time.strftime("%Y-%m-%d", time.localtime())
# print(nowtime)
# # weektime = int(nowtime) - 7
# # print(weektime)


# from datetime import datetime,timedelta

# nowtime = datetime.now()

# weektime = nowtime - timedelta(days=7)

# print(weektime.strftime("%Y-%m-%d"))

from configparser import ConfigParser

config = ConfigParser()

config.read('application.properties')

mcbackupsnum = config.get('mcbackupsnum')

print(mcbackupsnum)