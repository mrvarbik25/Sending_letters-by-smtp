from colorama import Fore, Back, Style
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
        print('[ ' + Fore.GREEN + 'OK' + Style.RESET_ALL + ' ] ' + 'Successful connect to smtp.')
        server.sendmail(login, toaddr, msg.as_string())
        print('[ ' + Fore.GREEN + 'OK' + Style.RESET_ALL + ' ] ' + 'Successful Email sent.')
        server.quit()
    except:
        print('[ ' + Fore.RED + 'OK' + Style.RESET_ALL + ' ] ' + 'Could not connect to smtp.')

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
    choice = input(Style.RESET_ALL + 'Сreate a configuration file? ' + Back.GREEN + '[Y]es' + Style.RESET_ALL + ' or '+ Back.RED + '[N]o?' + Style.RESET_ALL + ' ').lower() # опрос, записать в файл конфигурацию?
    if choice == 'y':
        cfgFile = open('cfg.bin', 'wb') # создаем бинарный файл настроек
        dump(cfgSettings, cfgFile)  # через pickle записываем в него переменную cfgSettings
        cfgFile.close()
        print(Fore.GREEN + '[ OK ] Successfully settings written to configuration file. \'cfg.bin\'' + Style.RESET_ALL)
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
    print('[ ' + Fore.GREEN + 'OK' + Style.RESET_ALL + ' ] ' + 'Successful read.')
    send(login, password, url, toaddr, msg) # отправить письмо учитывая содержимое конфигурационного файла

def main():
    if arg() != []: # если в аргументах что то есть
        work_with_args()
    else:
        poll()
        cfg()

if __name__ == '__main__':
    main()
