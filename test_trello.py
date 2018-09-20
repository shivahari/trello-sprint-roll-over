"""
Sample test to test trello class
"""
from trello import trello
from conf import key,token

def test_trello(key,token):
    test_obj = trello(key,token)
    test_obj.read_board_and_card_details()
    #read_board_and_card_details

if __name__ == '__main__':
    test_trello(key=key,token=token)


