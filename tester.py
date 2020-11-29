import datetime

hour_diff = datetime.timedelta(days=1,hours=20,minutes=42, seconds=45)

check1 = datetime.timedelta(hours=40)
check2 = datetime.timedelta(hours=48)
print(check1)
print(check2)
print(hour_diff)
if hour_diff >= check1 and hour_diff <= check2:
	print("check in time")
else:
	print("invalid time")