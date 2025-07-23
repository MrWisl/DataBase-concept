import secrets
import string


class DataBase:
    __people = {}
    __instance = None
    name = None
    __admname = ''

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.role = None
        self.__lfilter = []
        self.__pfilter = []
        self.__message_log = {}
        self.__message_pas = {}

    def registr(self):
        print('Регистрация нового пользователя')
        while True:
            login = input('Введите имя пользователя >>>').strip()
            if login == '':
                print('Имя пользователя не указано! Повторите попытку')
                continue
            if login in self.__lfilter:
                print('Логин запрещен! Повторите попытку')
                continue
            if login in self.__people.keys():
                print('Такой логин уже есть! Повторите попытку')
                continue
            break
        while True:
            password = input('Введите пароль>>>').strip()

            if password == '':
                print('Пустое поле ввода пароля! Повторите попытку')
                continue
            if password in self.__pfilter:
                print('Пароль Запрещен! Повторите попытку')
                continue
            break
        passwordadm = input('Введите админский пароль если вы его знаете >>>').strip()
        if passwordadm == '1234imadmin' and self.__instance.__admname == '':
            print('получен доступ root')
            self.__instance.role = 'root'
            self.__instance.__admname = login
        else:
            self.__instance.role = 'member'
        self.__instance.name = login
        self.__people[login] = password
        print('регистрация завершена')

    @staticmethod
    def solution():
        while True:
            answ = input('подтвердить?(Да/Нет) >>>').strip()
            if answ.lower() == 'да':
                return True
            elif answ.lower() == 'нет':
                return False
            else:
                print('неправильный символ попробуйте снова')

    @staticmethod
    def generate_random():
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(characters) for _ in range(7))

    def __del__(self):
        print('База данных была удалена')

    def get_database(self):
        if self.role == 'root':
            print(f'количество участников: {len(self.__people)}')
            print(f'Информация об участниках: {self.__people}')
        else:
            print(f'Ваш логин: {self.__instance.name}')
            print(f'Ваш пароль: {self.__people[self.__instance.name]}')

    def blocked(self):
        if self.role == 'root' or self.__people != {}:
            while True:
                print(self.__people)
                login = input('введите логин пользователя которого хотите забанить').strip()
                if login not in self.__people.keys():
                    print('Данного логина нет в базе данных! Повторите попытку')
                    continue
                if login == '':
                    print('Пустой логин! Повторите попытку')
                    continue
                break
            if login == self.__instance.__admname:
                print('Вы не можете забанить себя :)')
                return
            if self.solution():
                if login in self.__message_log:
                    del self.__message_log[login]
                if login in self.__message_pas:
                    del self.__message_pas[login]
                del self.__people[login]
                print('Успешно')
                print(self.__people)
            else:
                print('блокировка отменена')
        else:
            print('недостаточно прав или база пуста')

    @staticmethod
    def help():
        print('список команд для использования функций ДБ')
        helps = {'/help': 'вызов меню помощи',
                 '/ban': 'блокировка пользователя',
                 '/info': 'показать информацию о пользователе(ях)',
                 '/end': 'закончить работу базы данных',
                 '/whoami': 'узнайте кто вы',
                 '/addfilter': 'добавить фильтр',
                 '/removefilter': 'удалить фильтр',
                 '/rename': 'изменить имя пользователя',
                 '/repass': 'сменить пароль участника базы данных',
                 '/relog': 'сменить логин участника базы данных',
                 '/enter': 'войти в аккаунт',
                 '/registr': 'зарегистрировать аккаунт'}
        print('вывод меню помощи')
        for command, doc in helps.items():
            print(f'{command}: {doc}')

    def rename(self):
        name = input('введите новое имя >>>').strip()
        print(f'ваше имя: {name}?')
        if self.solution():
            self.__instance.name = name
            print(f'операция завершена теперь вы {name}')
        else:
            print('операция отменена')

    def repass(self):
        if self.role == 'root':
            while True:
                print(self.__people)
                login = input('введите логин пользователя >>>').strip()
                if login not in self.__people.keys():
                    print('Логин отсутствует в базе! Повторите попытку')
                    continue
                if login == '':
                    print('Пустая строка! Повторите попытку')
                    continue
                break
            while True:
                password = input('введите новый пароль >>>').strip()
                if password == '':
                    print('Пустая строка! Повторите попытку')
                    continue
                if password.lower() in self.__pfilter:
                    print('пароль запрещен админом, повторите попытку')
                    continue
                break

            if self.solution():
                if self.__people[login] in self.__message_pas:
                    self.__message_pas[password] = self.__message_pas.pop(self.__people[login])
                else:
                    self.__message_pas[password] = self.__people[login]
                self.__people[login] = password

                print('Операция завершена успешно')
                print(f'Новый пароль: {self.__people[login]}')
        elif self.__people == {}:
            print('В базе данных пусто')
        else:
            while True:
                password = input('введите новый пароль >>>').strip()
                if password == '':
                    print('Пустая строка! Повторите попытку')
                    continue
                if password.lower() in self.__pfilter:
                    print('пароль запрещен админом, повторите попытку')
                    continue
                break
            if self.solution():
                self.__people[self.__instance.name] = password
                print('операция завершена успешно')
                print(f'Ваш пароль: {self.__people[self.__instance.name]}')
            else:
                print('Операция отменена')

    def addfilter(self):
        if self.role == 'root':
            while True:
                filter_type = input('на что вы хотите добавить фильтр? (логин/пароль) >>>').lower().strip()
                if filter_type in ('логин', 'пароль'):
                    break
                print('Такой опции нет, повторите попытку')
            while True:
                fil = input('введите фильтр>>>').strip()
                if fil in self.__lfilter:
                    print('Такой логин уже запрещен! Повторите попытку')
                    continue
                break
            if filter_type== 'логин':
                if self.solution():
                    self.__lfilter.append(fil.lower())
                    banlog = [login.lower() for login in self.__people
                              for blogin in self.__lfilter if login.lower() == blogin]
                    if banlog:
                        for banl in banlog:
                            print(f'у участника {banl} недопустимый логин произведена замена')
                            new_log = 'user' + self.generate_random()
                            self.__people[new_log] = self.__people.pop(banl)
                            if banl in self.__message_log:
                                self.__message_log[new_log] = self.__message_log.pop(banl)
                            self.__message_log[new_log] = banl
                            print(new_log)
                    print('фильтр добавлен')
                    print(self.__lfilter)
            elif filter_type.lower() == 'пароль':
                if self.solution():
                    self.__pfilter.append(fil.lower())
                    for key in self.__people:
                            if self.__people[key] in self.__pfilter:
                                print(f'у пользователя {key} запрещенный пароль, производится замена')
                                newpass = self.generate_random()
                                if self.__people[key] in self.__message_pas:
                                    self.__message_pas[newpass] = self.__message_pas.pop(self.__people[key])
                                else:
                                    self.__message_pas[newpass] = self.__people[key]
                                self.__people[key] = newpass
                                print(f'Новый пароль: {self.__people[key]}')

                            else:
                                continue
                    print(f'список текущих фильтров: {self.__pfilter}')
                    print('фильтр добавлен')
                else:
                    print('операция отменена')
            else:
                print('такого варианта ответа нет попробуйте еще раз')
        else:
            print('команда доступна только админам')

    def removefilter(self):
        if self.role == 'root':
            print('Недостаточно прав')
            return
        while True:
            filter_type = input('Выберете тип фильтра : логин/пароль >>>').lower().strip()
            if filter_type in ('логин', 'пароль'):
                break
            print('Такой опции нет!! Повторите попытку')
        filterlist = self.__lfilter if filter_type == 'логин' else self.__pfilter
        if not filterlist:
            print('фильтры отсутствуют')
            return
        while True:
            print(f'текущий список фильтров: {filterlist}')
            fil = input('введите название фильтра >>>').lower().strip()
            if fil in filterlist:
                break
            print('Фильтра не существует повторите попытку')
        if self.solution():
            filterlist.remove(fil)
            print(f'Измененный список фильтров: {filterlist}')
        else:
            print('операция отменена')

    def relog(self):
        if self.role == 'root':
            while True:
                print(self.__people)
                oldlog = input('введите старый логин пользователя >>>').strip()
                if oldlog == '':
                    print('Пустая строка повторите попытку !')
                    continue
                if oldlog not in self.__people.keys():
                    print('такого пользователя нет, попробуйте снова')
                    continue
                break

            while True:
                newlog = input('введите новый логин пользователя >>>')
                if newlog.lower()  in self.__lfilter:
                    print('Запрещенный логин! Повторите попытку')
                    continue

                if newlog in self.__people.keys():
                    print('Логин занят! Повторите попытку !')
                    continue

                if newlog == '':
                    print('Пустая строка ! Повторите попытку')
                    continue
                break

            if self.solution():
                if oldlog in self.__message_log:
                    self.__message_log[newlog] = self.__message_log.pop(oldlog)
                else:
                    self.__message_log[newlog] = oldlog
                self.__people[newlog] = self.__people.pop(oldlog)
                print('изменения были произведены успешно')
            else:
                print('операция отменена')
        elif self.__people == {}:
            print('База данных пуста')
        else:
            while True:
                newlog = input('Введите новый логин >>>').strip()
                if newlog.lower() in self.__lfilter:
                    print('Запрещенный логин! Повторите попытку')
                    continue
                if newlog in self.__people.keys():
                    print('Логин занят! Повторите попытку !')
                    continue
                if newlog == '':
                    print('Пустая строка! Повторите попытку')
                    continue
                break
            if self.solution():
                self.__people[newlog] = self.__people.pop(self.__instance.name)
                self.__instance.name = newlog
                print('изменения были произведены успешно')
            else:
                print('операция отменена')

    def enter(self):
        print('Чтобы войти в аккаунт напишите логин и пароль')
        while True:
            login = input('Введите логин >>>').strip()
            if login == '':
                print('Пустая строка! Повторите попытку')
                continue
            if login in self.__message_log.values():
                login  = ''.join([key[0] for key in self.__message_log.items() if login in key])
                print('Ваш логин был изменен',
                      f'Ваш новый логин {login}', sep='\n')
                del self.__message_log[login]
            if login not in self.__people.keys():
                print('Логин не найден!')
                answ = input('Желаете зарегистрироваться: Да/Нет >>>').lower()
                if  answ == 'да':
                    self.registr()
                    return
                else:
                    continue
            break
        while True:
            password = input('Введите пароль >>>').strip()
            if password == '':
                print('Пустая строка! Повторите попытку')
                continue
            if password in self.__message_pas.values():
                print('ваш предыдущий пароль был изменен',
                        f'Ваш новый пароль {self.__people[login]}', sep='\n')
                password = self.__people[login]
                del self.__message_pas[self.__people[login]]
            if password != self.__people[login]:
                print('Неверный пароль! Повторите попытку.')
                continue
            break
        if self.solution():
            print(f'Вход произведен успешно, теперь вы {login}')
            self.__instance.name = login
            self.__instance.role = 'member' if login not in self.__instance.__admname else 'root'

db = DataBase()
db.registr()
print('Вводите команды, /help, чтобы вызвать меню помощи')
while True:
    choose = input()
    if choose == '/help':
        db.help()
    elif choose == '/registr':
        db.registr()
    elif choose == '/ban':
        db.blocked()
    elif choose == '/info':
        db.get_database()
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
    elif choose == '/enter':
        db.enter()
    else:
        print('такой команды нет')
