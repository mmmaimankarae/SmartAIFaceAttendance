from datetime import datetime

now = datetime.now()
print("b", now)
checkingTime = now.strftime("%H:%M")
af1300 = now.replace(hour = 13, minute = 0, second = 0)
af1315 = now.replace(hour = 13, minute = 15, second = 59)

mr0900 = now.replace(hour = 9, minute = 0, second = 0)
mr0915 = now.replace(hour = 9, minute = 15, second = 59)
if af1300 <= now <= af1315:
    print(checkingTime)
if mr0900 <= now <= mr0915:
    print(checkingTime)
    
now = now = datetime.now()
print("a", now)

beforeDay = datetime.now().strftime("%d/%m/%Y")
lastChecking = datetime.strtime(studentInfo['check the time'], "%H:%M")
today = now.strftime("%d/%m/%Y")
checkingTime = now.strftime("%H:%M")
if beforeDay == today:
    modeType = 1
    checkMatche = 0