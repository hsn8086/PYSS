import hashlib
import logging
import random


class FlaskLoggerFilter(logging.Filter):
    def filter(self, record):
        print(record.msg)
        return True


def get_random_token(key_len=128):
    return ''.join(
        [chr(random.choice(list(range(65, 91)) + list(range(97, 123)) + list(range(48, 58)))) for _ in range(key_len)])


def salted_hash(data, salt, additional_string=None):
    hash_salt = salt
    if additional_string is not None:
        hash_salt += hashlib.sha1(additional_string.encode('utf8')).hexdigest()
    return hashlib.sha1((data + hash_salt).encode('utf8')).hexdigest()


def request_parse(req_data):
    if req_data.method == 'POST':
        data = req_data.form
    elif req_data.method == 'GET':
        data_dict = {}
        for i in req_data.args.items():
            data_dict[i[0]] = i[1]
        data = data_dict
    else:
        data = {}
    return data


def ins(obj: iter, collection) -> bool:
    res = True
    for i in obj:
        res = res and (i in collection)
    return res


def not_ins(obj: iter, collection) -> bool:
    res = True
    for i in obj:
        res = res and (i not in collection)
    return res


def log_output(logger=__name__, log_level=logging.INFO, text=''):
    log = logging.getLogger(logger)

    log.log(log_level, text)
