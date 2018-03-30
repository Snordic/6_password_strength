import re


class print_my_error(Exception):
    def __init__(self, error):
        self.error = error


def get_user_password():
    print('Введите ваш пароль: ')
    return input()


def load_blacklist(filepath):
    with open(filepath, 'r', encoding='utf-8') as file_blacklist:
        return file_blacklist.read().splitlines()


def find_lower_case(password):
    if bool(re.search(r'[a-z]', password)):
        return 2
    else:
        return 0


def find_upper_case(password):
    if bool(re.search(r'[A-Z]', password)):
        return 2
    else:
        return 0


def find_digital(password):
    if bool(re.search(r'\d', password)):
        return 1
    else:
        return 0


def find_symbols(password):
    if bool(re.search(r'\W', password)):
        return 2
    else:
        return 0


def check_length_password(password, min_length=7):
    error_check = 'Пароль должен быть не менее 8 символов'
    result_check = not bool(len(password) > min_length)
    if result_check:
        raise print_my_error(error=error_check)


def check_number_phone(password):
    error_check = 'В качестве пароля запрещено использовать номер телефона'
    result_check = bool(re.search(r'[+7|7-8]\d{11}', password))
    if result_check:
        raise print_my_error(error=error_check)


def check_date(password):
    error_check = 'В качестве пароля запрещено использовать календарные даты'
    result_check = bool(re.search(r'\d{1,2}[.]\d{1,2}[.]\d{2,4}', password))
    if result_check:
        raise print_my_error(error=error_check)


def check_email(password):
    error_check = 'В качестве пароля запрещено использовать емаил'
    result_check = bool(re.search(r'\w{1,30}[@]\w{1,8}[.][ru|com]+', password))
    if result_check:
        raise print_my_error(error=error_check)


def check_in_blacklist(password, blacklist):
    error_check = 'Пароль находится в запрещеном листе!'
    result_check = password in blacklist
    if result_check:
        raise print_my_error(error=error_check)


def check_password_strength(password, blacklist):
    point_strength = 0
    list_prohibition = [check_date, check_email, check_number_phone, check_length_password]
    list_inclusion = [find_digital, find_lower_case, find_symbols, find_upper_case]
    try:
        if blacklist:
            check_in_blacklist(password, blacklist)
        for check_password in list_prohibition:
            check_password(password)
    except print_my_error as prohibit:
                return prohibit.error
    else:
        point_strength += 3
        for check_password in list_inclusion:
            point_strength += check_password(password)
        return '{} {}/{}'.format('Оценка вашего пароля: ', point_strength, '10')


if __name__ == '__main__':
    try:
        black_list = load_blacklist('blacklist.txt')
    except FileNotFoundError:
        print('Warning: Файл blacklist.txt не найден, качество проверки может ухудшится!')
        black_list = None
    finally:
        user_password = get_user_password()
        print(check_password_strength(user_password, black_list))




