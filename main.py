import logging
import csv
import pandas as pd

from datetime import datetime, timedelta
from client import KaspiClient
from convert import convert_datetime_to_milliseconds as conv_d
from convert import convert_datetime_from_milliseconds as conv_d_rev

connector = KaspiClient()

logger = logging.getLogger(__name__)

file_name = 'sman_orders_archive'


def write_to_excel_file(file=f'{file_name}.csv'):
    df = pd.read_csv(file, delimiter=';')

    excel_file = f'{file_name}.xlsx'
    df.to_excel(excel_file, index=False)


def write_to_csv_file(data: list):
    with open(f'{file_name}.csv', 'a') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(data)


def parse(page_number: int, start_date: int, end_date: int):
    data = connector.get_orders(page_number=page_number, page_size=100, start_date=start_date, end_date=end_date)

    for d in data:
        order = {'id': d['id'],
                 'phone_number': d['attributes']['customer']['cellPhone'],
                 'first_name': d['attributes']['customer']['firstName'],
                 'last_name': d['attributes']['customer']['lastName'],
                 'date': conv_d_rev(d['attributes']['creationDate'])}

        write_to_csv_file([order['id'], order['first_name'], order['last_name'], order['phone_number'], order['date']])


def func():
    start_d, end_d = '2020-02-28', '2024-05-11'

    start_date = datetime.strptime(start_d, '%Y-%m-%d')
    end_date = datetime.strptime(end_d, '%Y-%m-%d')

    write_to_csv_file(['Номер заказа', 'Телефон', 'Имя клиента', 'Фамилия клиента', 'Дата заказа'])

    while start_date < end_date:
        next_date = start_date + timedelta(days=14)

        # calc
        pageCnt = connector.get_page_cnt_of_orders(start_milliseconds=conv_d(start_date),
                                                   end_milliseconds=conv_d(next_date))

        print('parsing dates between: %s and %s. pageCnt = %s' % (start_date, next_date, pageCnt))

        for page in range(pageCnt):
            parse(page_number=page, start_date=conv_d(start_date), end_date=conv_d(next_date))

        start_date = next_date


if __name__ == '__main__':
    func()
