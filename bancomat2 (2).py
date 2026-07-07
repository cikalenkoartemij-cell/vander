class Client:
    def __init__(self,id,name,balance,pin):
        self.id = id
        self.name = name
        self.balance = balance
        self.pin = pin

class ATM:
    def __init__(self):
        self.clients = {}
    def atm_interface(self):
        while True:
            print('\n1- Добавить клиента \n2- Войти в систему \n0- Выход')
            choice = input('\nВыберите действие: ')
            if choice == '0':
                break
            elif choice == '1':
                id=int(input('Создай свое ID: '))
                name=input('Придумай себе имя: ')
                balance=int(input('Введи свой стартовый баланс: '))
                pin=int(input('Создай свой пин: '))
                self.clients[id]=Client(id,name,balance,pin)
                print(f'Клиент {name} добавлен')
            elif choice == '2':
                id=int(input('Введи свой ID: '))
                client=self.clients[id]
                if client:
                    while True:
                        ou=int(input(f'Введи пин для {name} : '))
                        if ou == client.pin:
                            print('\nДобро пожаловать ')
                            self.operation_menu(client)
                            break
                        else :
                            print('Неверный пин, попробуй еще раз')
                else:
                    print('Клиент не найден')
    def operation_menu(self,client):
        while True:
            print('1- Пополнить \n2- Снять \n3- Изменить имя \n0- Выйти из аккаунта')
            op = input('Действие: ')
            if op == '0':
                break
            elif op == '1':
                amount=int(input('Сумма пополнения: '))
                client.balance += amount
                print('Баланс пополнен')
            elif op == '2':
                count=int(input('Сумма снятия: '))
                if count<= client.balance and count <=500:
                    client.balance -= count
                    print('Деньги выданы')
                else:
                    print('Сумма превышает лимита или баланса')
            elif op == '3':
                client.name=input('Введи новое имя: ')
atm = ATM()
atm.atm_interface()


