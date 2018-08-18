import os, json
from conf import settings


def save(user):
    path = os.path.join(settings.USER_DB, '%s.json' % user['name'])
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(user, f)
        f.flush()


def select(name):
    path = os.path.join(settings.USER_DB, '%s.json' % name)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return False
