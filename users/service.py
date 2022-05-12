import string
import random

from rest_framework.filters import SearchFilter

LETTERS = string.ascii_letters
NUMBERS = string.digits
PUNCTUATION = string.punctuation


def password_generator(cbl, length=10):
    """
    Generates a random password having the specified length
    :length -> length of password to be generated. Defaults to 8
        if nothing is specified
    :cbl-> a list of boolean values representing a user choice for
        string constant to be used to generate password.
        0 item ---> digits
             True to add digits to constant False otherwise
        1 item ---> letters
             True to add letters to constant False otherwise
        2 item ---> punctuation
             True to add punctuation to constant False otherwise
    :returns string <class 'str'>
    """
    # create alphanumerical by fetching string constant
    printable = fetch_string_constant(cbl)

    # convert printable from string to list and shuffle
    printable = list(printable)
    random.shuffle(printable)

    # generate random password
    random_password = random.choices(printable, k=length)

    # convert generated password to string
    random_password = ''.join(random_password)
    return random_password


def fetch_string_constant(choice_list):
    """
    Returns a string constant based on users choice_list.
    string constant can either be digits, letters, punctuation or
    combination of them.
    : choice_list --> list <class 'list'> of boolean
        0 item ---> digits
            True to add digits to constant False otherwise
        1 item ---> letters
            True to add letters to constant False otherwise
        2 item ---> punctuation
            True to add punctuation to constant False otherwise
    """
    string_constant = ''

    string_constant += NUMBERS if choice_list[0] else ''
    string_constant += LETTERS if choice_list[1] else ''
    string_constant += PUNCTUATION if choice_list[2] else ''

    return string_constant


class UserFilter(SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('name_first'):
            return ['name_first']
        if request.query_params.get('name_last'):
            return ['name_last']
        if request.query_params.get('position'):
            return ['position__name']
        if request.query_params.get('filial'):
            return ['filial__name']
        if request.query_params.get('status'):
            return ['status__name']
        if request.query_params.get('account'):
            return ['account__item']
        if request.query_params.get(''):
            return ['name_last', 'name_first', 'filial__name', 'account__item', 'position__name', 'status']
        return super(UserFilter, self).get_search_fields(view, request)

