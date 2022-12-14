import socket
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

def validate_number(fields_text): #валидация пропускает только числа
    reg_ex = QRegExp('^-?(0|[1-9]\d*)(\.[0-9]{1,4})?$')
    for field in fields_text:
        field.setValidator(QRegExpValidator(reg_ex, field))

def internet():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        return False
