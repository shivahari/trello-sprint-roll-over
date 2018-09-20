"""
Sample test to test trello class
"""
from trello import trello
from conf import key,token

def test_trello(key,token):
    test_obj = trello(key,token)

if __name__ == '__main__':
    test_trello(key=key,token=token)


