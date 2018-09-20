import requests
import json,pickle
import sh,sys,os


class trello():
    "Trello class"
    def __init__(self,key,token):
        self.url = "https://api.trello.com/1/"
        self.auth_details = {'key':key,'token':token}
        self.boards = []
        self.account_name = None 
        self.fullname = None
        self.id = None
        self.organizations = None 
        self.member_type = None 
        self.account_details = {}
        self.all_board_details = {}
        self.all_card_details = {}
        if self.if_first_time():
            self.get_account_details()
            self.get_board_card_details()
        self.create_data_dir()


    def get_account_details(self):
        "Get the details of the user"
        result_flag = False
        get_account_details_url = 'https://api.trello.com/1/members/me/'
        try:
            response = self.get(url=get_account_details_url,params=self.auth_details)
            print response
            if response.status_code == 200:
                self.boards = response.json()['idBoards']
                self.account_name = response.json()['username']
                self.fullname = response.json()['fullName']
                self.id = response.json()['id']
                self.organizations = response.json()['idOrganizations']
                self.member_type = response.json()['memberType']
                self.account_details = {'boards':self.boards,'account_name':self.account_name,'fullname':self.fullname,'id':self.id,'organization':self.organizations,'member_type':self.member_type}
                result_flag = True
        except Exception as e:
            print str(e)
    
        return result_flag


    def get(self,url,params=None,data=None,headers=None):
        "Make a GET request"
        response = None
        try:
            response = requests.get(url=url,params=params,data=data,headers=headers)
            print response
        except Exception as e:
            print str(e)

        return response


    def get_board_card_details(self):
        "Get the board details"
        all_board_details = {}
        all_card_details = {}
        board_details = {}
        card_details = {}
        boards = self.boards 
        try:
            # Iterate through the boards to get the details
            for board in boards:
                # Get the board details
                board_url = self.url + '/boards/' + board
                get_board_details = requests.get(url=board_url,params=self.auth_details)
                board_details =  get_board_details.json()
                # Get the card details
                card_url = board_url + '/cards'
                get_card_details = requests.get(url=card_url,params=self.auth_details)
                card_details = get_card_details.json()
                board_filename = './data/board/'+ board
                print board_filename
                with open(board_filename,'w') as board_fileobj:
                    pickle.dump(board,board_fileobj)
                    board_fileobj.close()
                card_names = []
                card_sub_dir = './data/card/'+ board + '/'
                os.mkdir(card_sub_dir)
                for card in card_details:
                    card_names.append(card['name'])
                    all_card_details[card['id']] = card
                    card_filename = card_sub_dir + card['id']
                    print card_filename
                    with open(card_filename,'w') as card_filobj:
                        pickle.dump(card,card_filobj)
                        card_filobj.close()
                board_details['cards'] = card_names
                all_board_details[board] = board_details 
        except Exception as e:
            print str(e)
    

    def if_first_time(self):
        "Check if it is first time data being collected"
        result_flag = True
        result_flag = self.create_data_dir()
        try:
            if os.path.isdir('./data'):
                board_dir = './data/board/'
                check_if_board_exists = sh.ls(board_dir)
                card_dir  = './data/card/'
                check_if_card_exists = sh.ls(card_dir)
                if not check_if_board_exists:
                    result_flag &= True
                if not check_if_card_exists:
                    result_flag &= True
        except Exception as e:
            result_flag &= False
            print str(e)

        return result_flag

    
    def create_data_dir(self):
        "Create a new dir for data"
        result_flag = False
        try:
            current_dir = os.path.abspath(os.path.dirname('__file__'))
            data_dir = os.path.join(current_dir,'data')
            if not os.path.isdir(data_dir):
                os.mkdir(data_dir)
                board_dir = os.path.join(data_dir,'board')
                card_dir = os.path.join(data_dir,'card')
                if not os.path.isdir(board_dir):
                    os.mkdir(board_dir)
                if not os.path.isdir(card_dir):
                    os.mkdir(card_dir)
            result_flag = True
        except Exception as e:
            print str(e)

        return result_flag



