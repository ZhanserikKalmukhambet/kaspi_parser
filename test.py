from datetime import datetime

from convert import convert_datetime_to_milliseconds as conv_d

start_d, end_d = '2024-04-28', '2024-05-11'

start_date = datetime.strptime(start_d, '%Y-%m-%d')
end_date = datetime.strptime(end_d, '%Y-%m-%d')

print(conv_d(start_date))
print(conv_d(end_date))