import configparser
import sys
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate

# Получаем список всех файлов в текущей директории
files = [f for f in os.listdir('.') if f.endswith('.csv')]

# Сортируем файлы по времени последнего изменения
files.sort(key=lambda x: os.path.getmtime(x))

# Проверяем, что найдено как минимум два файла
if len(files) < 2:
    sys.exit()
else:
    # Получаем два последних файла
    latest_file = files[-1]
    previous_file = files[-2]

    # Читаем файлы в DataFrame
    df_latest = pd.read_csv(latest_file)
    df_previous = pd.read_csv(previous_file)

    # Сравнение DataFrame
    differences = df_previous.compare(df_latest)

# Проверка наличия различий
if not differences.empty:

    # Сохранение различий в файл
    differences.to_csv('differences_report.csv', index=False)

    config = configparser.ConfigParser()
    config.read('config.ini')

    from_mail = config['email']['from_mail']
    from_passwd = config['email']['from_passwd']
    server_adr = config['email']['server_adr']
    to_mail = config['email']['to_mail']

    msg = MIMEMultipart()  # Создаем сообщение
    msg["From"] = from_mail  # Добавляем адрес отправителя
    msg['To'] = to_mail  # Добавляем адрес получателя
    msg["Subject"] = Header('тест', 'utf-8')  # Пишем тему сообщения
    msg["Date"] = formatdate(localtime=True)  # Дата сообщения
    msg.attach(MIMEText("Проверка связи", 'html', 'utf-8'))  # Добавляем форматированный текст сообщения

    # Добавляем файл
    filepath = "differences_report.csv"  # путь к файлу
    part = MIMEBase('application', "octet-stream")  # Создаем объект для загрузки файла
    part.set_payload(open(filepath, "rb").read())  # Подключаем файл
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',
                    f'attachment; filename="{os.path.basename(filepath)}"')
    msg.attach(part)  # Добавляем файл в письмо

    smtp = smtplib.SMTP(server_adr, 587)  # Создаем объект для отправки сообщения
    smtp.starttls()  # Открываем соединение
    smtp.ehlo()
    smtp.login(from_mail, from_passwd)  # Логинимся в свой ящик
    smtp.sendmail(from_mail, to_mail, msg.as_string())  # Отправляем сообщения
    smtp.quit()  # Закрываем соединение

    # Удаление файла после отправки
    os.remove('differences_report.csv')

    # Удаляем каждый файл с расширением .csv
    for file in files:
        os.remove(file)

else:
    sys.exit()