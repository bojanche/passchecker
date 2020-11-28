import requests
import hashlib
import getpass


def request_api_data(hash_to_check):
    address = 'https://api.pwnedpasswords.com/range/' + hash_to_check
    res = requests.get(address)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, counted in hashes:
        if h == hash_to_check:
            return counted
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


password = getpass.getpass('Please enter password to check: ')
count = pwned_api_check(password)
if count:
    print(f'Your password was found {count} times... you should change your password!')
else:
    print(f'Your password was NOT found.')