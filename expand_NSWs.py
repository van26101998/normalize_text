# encoding : utf-8
import re
from num2words import num2words
from unicodedata import normalize
from datetime import date

from utils import load_dict

LSEQ_DICT_PATH = './dicts/LSEQ_DICT.txt'
EN2VI_DICT_PATH = './dicts/EN2VI_DICT.txt'
ABB_DICT_PATH = './dicts/ABB_DICT_PATH.txt'
PUNC_DICT_PATH = './dicts/PUNC_DICT.txt'
CURRENCY_DICT_PATH = './dicts/CURRENCY_DICT.txt'
UNIT_DICT_PATH = './dicts/UNIT_DICT.txt'
VI_WORDS_PATH = './dicts/vietnamese_words.txt'


LSEQ_DICT = load_dict(LSEQ_DICT_PATH)
EN2VI_DICT = load_dict(EN2VI_DICT_PATH)
ABB_DICT = load_dict(ABB_DICT_PATH)
PUNC_DICT = load_dict(PUNC_DICT_PATH)
CURRENCY_DICT = load_dict(CURRENCY_DICT_PATH)
UNIT_DICT = load_dict(UNIT_DICT_PATH)

f = open(VI_WORDS_PATH, 'r', encoding='utf-8')
list_vietnamese_words = f.read().split('\n')
f.close()

def NNUM2words(num_string):
    return num2words(float(num_string), lang='vi')


def NTIME2words(time_string):
    try:
        time_arr = time_string.split(':')
        if len(time_arr) == 2:
            h = time_arr[0]
            m = time_arr[1]
            return NNUM2words(h) + " giờ " + NNUM2words(m) + " phút"
        elif len(time_arr) == 3:
            h = time_arr[0]
            m = time_arr[1]
            s = time_arr[2]
            return NNUM2words(h) + " giờ " + NNUM2words(m) + " phút " \
                + NNUM2words(s) + " giây"
    except:
        return ""


def NDAT2words(date_string):
    """ngày/tháng/năm"""
    separator = '/'
    date_arr = date_string.split(separator)
    d, m, y = date_arr[0], date_arr[1], date_arr[2]

    # đọc ngày
    dstring = ""
    if int(d) < 10:
        dstring = "mồng " + NNUM2words(d)
    else:
        dstring = NNUM2words(d)

    # đọc năm
    ystring = ""
    y = int(y)
    if y <= 1000 or y % 1000 == 0:
        ystring = NNUM2words(y)
    else:
        ystring = NNUM2words(y//100*100)
        if (y//100 % 10 == 0):
            ystring += " không trăm"
        if y % 100 < 10:
            ystring += " lẻ " + NNUM2words(y % 100)
        else:
            ystring += " " + NNUM2words(y % 100)

    return dstring + " tháng " + NNUM2words(m) \
        + " năm " + ystring


def NDAY2words(day_string):
    """ngày/tháng"""
    separator = '/'
    day_arr = day_string.split(separator)
    d, m = day_arr[0], day_arr[1]

    # đọc ngày
    dstring = ""
    if int(d) < 10:
        dstring = "mồng " + NNUM2words(d)
    else:
        dstring = NNUM2words(d)

    return dstring + " tháng " + NNUM2words(m)


def NMONT2words(mont_string):
    """tháng/năm"""
    separator = '/'
    mont_arr = mont_string.split(separator)
    m, y = mont_arr[0], mont_arr[1]

    # đọc năm
    ystring = ""
    y = int(y)
    if y <= 1000 or y % 1000 == 0:
        ystring = NNUM2words(y)
    else:
        ystring = NNUM2words(y//100*100)
        if (y//100 % 10 == 0):
            ystring += " không trăm"
        if y % 100 < 10:
            ystring += " lẻ " + NNUM2words(y % 100)
        else:
            ystring += " " + NNUM2words(y % 100)

    return NNUM2words(m) + " năm " + ystring


def NTEL2words(tel_string):
    "093.156.2565"
    tel_string = ''.join(tel_string.split('.'))
    result = ''
    for digit in tel_string:
        result += NNUM2words(digit) + ' '

    return result


def NDIG2words(dig_string):
    "3925"
    result = ''
    for digit in dig_string:
        result += NNUM2words(digit) + ' '

    return result


def NSCORE2words(score_string):
    """tỷ số `2-3`"""
    arr = score_string.split('-')
    result = NNUM2words(arr[0]) + ' ' + NNUM2words(arr[1])

    return result


def NRNG2words(range_string):
    """từ `2-3`"""
    arr = range_string.split('-')
    result = NNUM2words(arr[0]) + ' đến ' + NNUM2words(arr[1])

    return result


def NPER2words(per_string):
    """30% hoặc 30-40%"""
    per_string = re.sub(r'(?P<id>\d+)-(?P<id1>\d+)',
                        lambda x: x.group('id') + ' đến ' + x.group('id1'), per_string)
    per_string = re.sub(
        r'(?P<id>\d+)\%', lambda x: x.group('id')+' phần trăm', per_string)
    per_string = re.sub(
        r'(?P<id>\d+)', lambda x: NNUM2words(x.group('id')), per_string)

    return per_string


def NFRC2words(frac_string):
    """3/4"""
    frac_string = re.sub(r'\/', lambda x: ' phần ', frac_string)
    frac_string = re.sub(
        r'(?P<id>\d+)', lambda x: NNUM2words(x.group('id')), frac_string)

    return frac_string


def LWRD2words(word):
    try:
        result = EN2VI_DICT[word.lower()]
    except:
        # nếu word không có trong từ điển tiếng Anh
        result = None

    return result


def LSEQ2words(seq_string):
    result = ''
    for char in seq_string:
        result += LSEQ_DICT[char.upper()] + ' '

    return result


def LABB2words(abb_string):
    """ĐHBKHN"""
    result = ''
    abb_string = abb_string.strip()
    if abb_string in ABB_DICT:
        result = ABB_DICT[abb_string].split(',')[0]
    else:
        result = LSEQ2words(abb_string)

    return result


def PUNC2words(punc_string):
    result = ''
    if punc_string in PUNC_DICT:
        result = PUNC_DICT[punc_string]

    return result

def URLE2words(urle_string):
    """đọc đường link và email"""
    urle_string = re.sub(r'.com', ' chấm com ', urle_string)
    urle_string = re.sub(r'.edu', ' chấm e đu ', urle_string)
    urle_string = re.sub(r'gmail', ' gờ meo ', urle_string)
    urle_string = re.sub(r'@', ' a còng ', urle_string)
    urle_string = re.sub(r'(?P<id>{})'.format('\.|\,|\:|\/'), lambda x: ' ' + PUNC2words(x.group('id'))+ ' ', urle_string)
    urle_string = re.sub(r'(?P<id>\d)', lambda x: ' ' + NNUM2words(x.group('id'))+ ' ', urle_string)
    arr = urle_string.split()
    for i, word in enumerate(arr):
        if word not in list_vietnamese_words:
            arr[i] = LSEQ2words(word)

    result = ' '.join(arr)
    return result

def MONY2words(money_string):
    # tách đơn vị và số
    money_string = re.sub(r'(?P<id>\d)(?P<id1>{})'.format('VNĐ|\$|S\$'), lambda x: x.group('id')+ ' ' + x.group('id1'), money_string)
    # đọc số 
    money_string = re.sub(r'(?P<id>\d)\.', lambda x: x.group('id'), money_string)
    money_string = re.sub(r'\,', lambda x: '.', money_string)
    money_string = re.sub(r'(?P<id>(\w|\.)+)', lambda x: NNUM2words(x.group('id')), money_string)
    money_string = re.sub(r'(?P<id>{})'.format('VNĐ|\$|S\$'), lambda x: CURRENCY_DICT[x.group('id')], money_string)
    
    return money_string
