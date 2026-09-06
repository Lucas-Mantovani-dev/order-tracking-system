data = [
    12,
    34,
    56,
    78,
    90,
    "2026-09-03 19:51:07"
]

old_date = data[5][0:10]

from datetime import datetime
date_obj = datetime.strptime(old_date, "%Y-%m-%d")
new_date = date_obj.strftime("%d/%m/%Y")

date_time = new_date + data[5][10::]

print(date_time)
