from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler

_AUTH_MESSAGES = {
    'No active account found with the given credentials': 'E-mail ou senha inválidos.',
    'Token is invalid or expired': 'Sessão expirada. Faça login novamente.',
    'Given token not valid for any token type': 'Sessão expirada. Faça login novamente.',
}


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    if isinstance(exc, ValidationError):
        message = _first_message(response.data)
    else:
        detail = response.data.get('detail', '')
        message = _AUTH_MESSAGES.get(str(detail), str(detail)) or str(exc)

    response.data['message'] = message
    return response


def _first_message(data):
    if isinstance(data, dict):
        for value in data.values():
            msg = _first_message(value)
            if msg:
                return msg
    elif isinstance(data, list):
        for item in data:
            msg = _first_message(item)
            if msg:
                return msg
    elif data:
        return str(data)
    return ''
