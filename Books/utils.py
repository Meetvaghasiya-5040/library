import urllib.request

from django.utils import timezone


def check_internet(host='8.8.8.8',port=53,timeout=3):
    try:
        urllib.request.urlopen("http://www.google.com",timeout=5)
        return True
    except Exception as e:
        print("internet is off!",repr(e))
        return False
print(check_internet())