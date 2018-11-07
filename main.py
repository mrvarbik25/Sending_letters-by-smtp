from getpass import getpass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pickle import load, dump
from sys import argv

cfgSettings = []

def send(login, password, url, toaddr, msg):
    """отправка писем"""
    try:
        server = smtplib.SMTP_SSL(url, 465)
        server.login(login, password)
        print('[ ', '\u001b[32m' + 'OK', ' ] ', 'Successful connect to smtp.', sep='\u001b[0m')
        server.sendmail(login, toaddr, msg.as_string())
        print('[ ', '\u001b[32m' + 'OK', ' ] ', 'Successful Email sent.', sep='\u001b[0m')
        server.quit()
    except:
        print('[ ', '\u001b[31m' + 'OK', ' ] ', 'Could not connect to smtp.', sep='\u001b[0m')
        raise SystemExit

def poll():
    """опрос пользователя и отправка писем"""
    login = input('Login: ')    # опрос пользователя логин почты с которой отправлять письма
    password = getpass()    # пароль почты с которой отправлять письма
    toaddr = input('Receiver: ')    # кому отправлять письма
    url = 'smtp.gmail.com'  # url smtp

    msg = MIMEMultipart()
    msg['Subject'] = input('Email title: ') # title
    body = input('Letter:\n')   # содержание письма
    msg['From'] = login # от кого
    msg.attach(MIMEText(body, 'plain'))
    send(login, password, url, toaddr, msg)
    global cfgSettings
    cfgSettings = [login, password, toaddr, msg['Subject'], body]   #   запись в переменную всех настроек

def cfg():
    """создает файл с настройками"""
    choice = input('Сreate a configuration file? ' + '\u001b[42m' + '[Y]es' + '\u001b[0m' + ' or ' + '\u001b[41m' + '[N]o?' + '\u001b[0m' + ' ').lower() # опрос, записать в файл конфигурацию?
    if choice == 'y':
        cfgFile = open('cfg.bin', 'wb') # создаем бинарный файл настроек
        dump(cfgSettings, cfgFile)  # через pickle записываем в него переменную cfgSettings
        cfgFile.close()
        print('[ ', '\u001b[32m' + 'OK', ' ] ', 'Successfully settings written to configuration file \'cfg.bin\'', sep='\u001b[0m')
    elif choice == 'n':
        raise SystemExit    # выход

def arg():
    """возвращает аргументы в виде списка"""
    global args
    args = argv[1:]
    return args

def work_with_args():
    url = 'smtp.gmail.com'
    msg = MIMEMultipart()
    with open(arg()[0], 'rb') as cfgFile:   # открыть конфигурационный файл
        text = load(cfgFile)
    login = text[0]
    password = text[1]
    toaddr = text[2]
    msg['Subject'] = text[3]
    body = text[4]
    msg['From'] = text[0]
    msg.attach(MIMEText(text[4], 'plain'))
    print('[ ', '\u001b[32m' + 'OK', ' ] ', 'Successful read.', sep='\u001b[0m')
    send(login, password, url, toaddr, msg) # отправить письмо учитывая содержимое конфигурационного файла

def main():
    if arg() != []: # если в аргументах что то есть
        work_with_args()
    else:
        poll()
        cfg()

if __name__ == '__main__':
    main()
