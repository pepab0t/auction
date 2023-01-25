

_m = []

def set_messages(*messages):
    for message in messages:
        _m.append(message)

def get_messages():
    try:
        return _m.copy()
    finally:
        _m.clear()