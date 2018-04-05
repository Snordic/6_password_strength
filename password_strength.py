import re
import getpass
import sys


def load_blacklist(filepath):
    with open(filepath, 'r', encoding='utf-8') as file_blacklist:
        return file_blacklist.read().splitlines()


def has_lower_case(password):
    return bool(re.search(r'[a-z]', password)) * 2


def has_upper_case(password):
    return bool(re.search(r'[A-Z]', password)) * 2


def has_digital(password):
    return bool(re.search(r'\d', password))


def has_symbols(password):
    return bool(re.search(r'\W', password)) * 2


def check_length_password(password, min_length=7):
    return not bool(len(password) > min_length)


def check_number_phone(password):
    return bool(re.search(r'[+7|7-8]\d{11}', password))


def check_date(password):
    return bool(re.search(r'\d{1,2}[.]\d{1,2}[.]\d{2,4}', password))


def check_email(password):
    return bool(re.search(r'\w{1,30}[@]\w{1,8}[.][ru|com]+', password))


def check_in_blacklist(password, blacklist):
    return password in blacklist


def check_password_strength(password, blacklist):
    point_strength = 0
    checklist = [
        has_digital,
        has_lower_case,
        has_symbols,
        has_upper_case,
    ]
    list_prohibitions = [
        check_length_password,
        check_number_phone,
        check_date,
        check_email,
    ]
    if check_in_blacklist(password, blacklist):
        print('Ваш пароль находится в черном списке паролей!')
        return point_strength
    for check in list_prohibitions:
        if check(password):
            print('Ваш пароль содержит личную информацию, '
                  'либо его длина меньше 8 символов.')
            return point_strength
    point_strength = 3
    for check in checklist:
        point_strength += check(password)
    return point_strength


if __name__ == '__main__':
    try:
        black_list = load_blacklist(sys.argv[1])
    except (FileNotFoundError, IndexError):
        print('Warning: Файл содеражищий запрещенные пароли не добавлен,'
              ' качество проверки может ухудшится!')
        black_list = []
    user_password = getpass.getpass()
    result_point = check_password_strength(user_password, black_list)
    print('{} {}/{}'.format('Результат проверки:', result_point, '10'))




