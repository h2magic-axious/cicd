import re

RE_WHITELIST = [
    r"/health",
    r"/user/login"
]

WHITELIST = [re.compile(i) for i in RE_WHITELIST]


def check_whitelist(path):
    for w in WHITELIST:
        if w.match(path):
            return True
    return False
