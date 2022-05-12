from functools import wraps
from json import JSONDecodeError, loads

from django import forms
from django.core.validators import RegexValidator
from django.http import JsonResponse


def validation(form):
    def decorator(func):
        @wraps(func)
        def wrap(request, *args, **kwargs):
            _form = form(request.GET)
            if not _form.is_valid():
                print(_form)
                return JsonResponse({'error': 'Not valid data in form', 'result': []})
            fr = _form.loads()  # convert json to python
            if fr['error']:
                return JsonResponse({'error': fr['error'], 'result': []})
            return func(request, fr, *args, **kwargs)

        return wrap

    return decorator


class NotValidDate(Exception):
    pass


class CreatePassword(forms.Form):
    ti = forms.CharField(validators=[RegexValidator(r'^true|false$')])
    tl = forms.CharField(validators=[RegexValidator(r'^true|false$')])
    tp = forms.CharField(validators=[RegexValidator(r'^true|false$')])
    len = forms.IntegerField(validators=[RegexValidator(r'^[\d]{1,}$')])

    def loads(self):
        try:
            return {
                'ti':   loads(self.cleaned_data['ti']),
                'tl':   loads(self.cleaned_data['tl']),
                'tp':   loads(self.cleaned_data['tp']),
                'length': self.cleaned_data['len'],
                'error': None,
            }
        except JSONDecodeError as e:
            return {'error': 'Not valid json data, %s' % e}
        except NotValidDate:
            return {'error': 'Not valid date'}
