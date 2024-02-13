import subprocess,time
from datetime import datetime,timedelta

nowtime = datetime.now()
print(nowtime.strftime("%Y-%m-%d"))

mcbackup ="time tar -czvf /home/mc/touho_MC/mcbackups/"+nowtime.strftime("%Y-%m-%d")+".tar.gz /home/mc/touho_MC/1.20.0/"
print(mcbackup)



# result = subprocess.check_output(mcbackup,shell=True)






# weektime = nowtime - timedelta(days=7)

# print(weektime.strftime("%Y-%m-%d"))