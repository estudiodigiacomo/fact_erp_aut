from datetime import datetime, timedelta

numbers_day = int('3')
date_actual = datetime.now()
new_date = date_actual + timedelta(days=numbers_day)
date_fromated = new_date.strftime("%d/%m/%Y")

print(date_fromated)