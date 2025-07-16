import random
import string



class DataBase:
    __instance = None


    # выбираются права пользователя + ломаный синглтон

    def __new__(cls, *args, **kwargs):
        print('Если вы админ то вы знаете пароль который нужно ввести)')
        password = input()
        if password == '1234imadmin':
            print('получен доступ root')
            cls.member = 'root'
            cls.name = 'root'
        else:
            print('Привет пользователь')
            cls.member = 'member'
            cls.name = 'member'
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance



    # функция, которая принимает решения

    def solution(self):
        print('подтвердить изменения? Да/Нет')
        answ = input()
        if answ.lower() == 'да':
            a = True
        elif answ.lower() == 'нет':
            print('операция отменилась')
            a = False
        else:
            print('неправильный символ')
            a = self.solution()
        return a



    # генератор случайных паролей

    @staticmethod
    def generate_password():
        # создает список из всех возможных символов
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(7))
        return password

    # инициализация словаря, количества участников, списков запрещенных логинов и паролей
    def __init__(self):
        self.__countpeople = 0
        self.__people = {}
        self.lfilter = []
        self.pfilter = []


   # Финализатор
    def __del__(self):
        print('База данных была удалена')



    # метод добавляющая участников в базу данных
    def addmembers(self):
        print('введите логин и пароль, через пробел')
        login, password = input().split(' ')
        # проверка находится ли пароль и логин в списке запрещенных логинов и паролей
        # и за тем чтобы пользователи не повторялись
        if login.lower() in self.lfilter:
            print('данный логин запрещен админом, повторите попытку')
            self.addmembers()
        elif password.lower() in self.pfilter:
            print('данный пароль запрещен админом, повторите попытку')
            self.addmembers()
        elif login in self.__people.keys():
            print('пользователь с таким логином уже существует')
            return
        # в случае прохода всех проверок принимается решение добавить ли нового участника или нет
        else:
            var = self.solution()
            if var:
                self.__people[login] = password
                self.__countpeople += 1
                print('Успешно')
                print(self.__people)


    # позволяет получить данные из Базы Данных

    def get_database(self):
        # проверяет, является ли пользователь админом, а затем выводит информацию

        if self.member == 'root':
            print(f'количество участников: {self.__countpeople}')
            print(f'Информация об участниках: {self.__people}')
        else:
            print('Доступно только админу')
            print('ошибка Недодастоточно прав')


    # метод блокировки пользователей

    def blocked(self):

        # проверка на права пользователя
        if self.member == 'root':
            print(self.__people)

            # проверка на пустой словарь базы данных

            if self.__people == {}:
                print('Удалять некого')
                return None
            else:

                # принятие решения и блокировка пользователя

                print('введите логин пользователя которого хотите забанить')
                login = input()
                var = self.solution()
                if var:
                    del self.__people[login]
                    self.__countpeople -= 1
                    print('Успешно')
                    print(self.__people)
        else:
            print('команда доступна только админам')

    # статичный метод помощи
    @staticmethod
    def help():
        print('список команд для использования функций ДБ')
        helps = {'/help': 'вызов меню помощи', '/ban': 'блокировка пользователя',
                '/add': 'добавить пользователя', '/info': 'показать статистики базы данных',
                 '/end': 'закончить работу базы данных', '/whoami': 'узнайте кто вы',
                 '/addfilter': 'добавить фильтр', '/removefilter': 'удалить фильтр',
                 '/rename': 'изменить имя пользователя', '/repass': 'сменить пароль участника баззы данных', '/relog':
                     'сменить логин участника базы данных'}
        print(helps)

    # метод, который переименовывает пользователя

    def rename(self):
        print('введите новое имя')
        name = input()
        print(f'ваше имя: {name}')
        var = self.solution()
        if var:
            self.name = name
            print(f'операция завершена теперь вы {name}')
        else:
            print('операция отменена')

    # метод изменения пароля участника базы данных

    def repass(self):
        if self.member == 'root':

            #проверка на пустоту базы данных

            if self.__people == {}:
                print('в БД нет пользователей')
                return

            # ввод нового пароля и принятие решения

            else:
                print('введите логин пользователя')
                print(self.__people)
                login = input()
                print('введите новый пароль')
                password = input()
                var = self.solution()

                # случай если пароль не запрещен и пользователь захотел его поменять

                if var and password not in self.pfilter:
                    try:
                        self.__people[login] = password
                    except ValueError:
                        print('операция завершена с ошибкой')
                        print('неверный логин')
                        return
                    print('операция завершена успешно')
                    print(self.__people)

                    # случай если пароль запрещен

                elif password in self.pfilter:
                    print('пароль запрещен админом, повторите попытку')
                    self.repass()
                else:
                    print('операция отменена')
        else:
            print('команда доступна только админу')


    # метод добавления фильтра

    def addfilter(self):

        # проверка является ли пользователь админом

        if self.member == 'root':
            print('на что вы хотите добавить фильтр логин/пароль')
            answ = input()

            # случай если пользователь захотел сделать запрещенный логин

            if answ.lower() == 'логин':
                print('введите запрещенный логин')
                fil = input()
                var = self.solution()

                #проверка согласен ли пользователь со своим решением и не является ли имя пользователя Аноним

                if var and fil.lower() != 'anonim':
                    banlog = None
                    self.lfilter.append(fil.lower())

                    # перебор участников ДБ на случай если есть участники с данным запрещенным логином

                    for login in self.__people.keys():
                        for blogin in self.lfilter:
                            if login.lower() == blogin.lower():
                                banlog = login
                            else:
                                continue

                     #заменяет логин если он запрещен и уже есть в ДБ на Anonim

                    if banlog is not None:
                        print(f'у участника {banlog} недопустимый логин поэтому он заменен на Anonim')
                        self.__people['Anonim'] = self.__people.pop(banlog)
                        print(self.lfilter)
                    print('фильтр добавлен')
                    print(self.__people)

               #  случай если пользователь захотел сделать фильтр на пароль

            elif answ.lower() == 'пароль':
                print('введите запрещенный пароль')
                fil = input()
                var = self.solution()
                if var:
                    self.pfilter.append(fil.lower())

                    # перебор имеющихся паролей и запрещенных

                    for key in self.__people:
                        for passw in self.pfilter:

                            # в случае наличия запрещенного пароля заменяет его на случайно сгенерированный
                            # через метод generate_password

                            if self.__people[key].lower() == passw:
                                print(f'у пользователя {key} запрещенный пароль, '
                                    f'поэтому он был заменен на случайный')
                                self.__people[key] = self.generate_password()
                                print(self.__people)


                    print(self.pfilter)
                    print('фильтр добавлен')
                else:
                    print('операция отменена')
            else:
                print('такого варианта ответа нет попробуйте еще раз')
                self.addfilter()
        else:
            print('команда доступна только админам')

    # метод удаления фильтра


    def removefilter(self):
        # проверка на права пользователя

        if self.member == 'root':
            print('фильтр чего будем удалять логин/пароль')
            answ = input()

            # случай если пользователь захотел удалить запрещенный логин

            if answ.lower() == 'логин':

                # проверка на пустоту списка запрещенных логинов

                if not self.lfilter:
                    print('у вас нет запрещенных логинов')
                    return

                # само удаление фильтра

                print('введите название фильтра')
                print(self.lfilter)
                fil = input()
                var = self.solution()
                if var:
                    self.lfilter.remove(fil)
                    print(self.lfilter)
                    print('фильтр удален')
                else:
                    print('операция отменена')

            # случай если пользователь захотел удалить запрещенный пароль

            elif answ.lower() == 'пароль':

                # проверка на пустоту списка

                if not self.pfilter:
                    print('у вас нет запрещенных паролей')
                    return

                # само удаление запрещенного пароля

                print('введите название фильтра')
                print(self.pfilter)
                fil = input()
                var = self.solution()
                if var:
                    self.pfilter.remove(fil)
                    print(self.pfilter)
                    print('фильтр удален')
                else:
                    print('операция отменена')
            else:
                print('такого варианта ответа нет попробуйте еще раз')
                self.removefilter()
        else:
            print('это команда доступна только админам')



    # метод изменения логина участника
    def relog(self):

        # проверка на права пользователя

        if self.member == 'root':

            # проверка на пустоту базы данных

            if self.__people != {}:
                print('введите старый логин пользователя')
                print(self.__people)
                oldlog = input()

                # проверка на существование введенного старого логина

                if oldlog not in self.__people.keys():
                    print('такого логина нет попробуйте еще раз')
                    return

                # ввод нового логина

                print('введите новый логин пользователя')
                newlog = input()

                # проверка является ли новый логин допустимым

                if newlog in self.lfilter:
                    print('запрещенный логин попробуйте снова')
                    return

                # приянтие решения и исход его

                var = self.solution()
                if var:
                    self.__people[newlog] = self.__people.pop(oldlog)
                    print('изменения были произведены успешно')
                    print(self.__people)
            else:
                print('в базе данных нет участников')
        else:
            print('команда доступна только админам')

db = DataBase()
print('Вводите команды, /help, чтобы вызвать меню помощи')

# бесконечный цикл для ввода команд

while True:
    choose = input()
    if choose == '/help':
        db.help()
    elif choose == '/add':
        db.addmembers()
    elif choose == '/ban':
        db.blocked()
    elif choose == '/info':
        db.get_database()

    # пишет как вас зовут

    elif choose == '/whoami':
        print(db.name)
    elif choose == '/end':
        print('концепт базы данных удален')
        del db
        break
    elif choose == '/rename':
        db.rename()
    elif choose == '/repass':
        db.repass()
    elif choose == '/removefilter':
        db.removefilter()
    elif choose == '/addfilter':
        db.addfilter()
    elif choose == '/relog':
        db.relog()
    else:
        print('такой команды нет')