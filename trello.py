import requests
import json,pickle
import sh,sys,os
import pandas as pd


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
        self.current_dir = os.path.abspath(os.path.dirname('__file__'))
        self.data_dir = os.path.join(self.current_dir,'data')
        self.board_dir = os.path.join(self.data_dir,'board')
        self.card_dir = os.path.join(self.data_dir,'card')
        self.get_account_details()
        if self.if_first_time():
            self.get_board_card_details()
        self.create_data_dir()


    def get_account_details(self):
        "Get the details of the user"
        result_flag = False
        get_account_details_url = 'https://api.trello.com/1/members/me/'
        try:
            response = self.get(url=get_account_details_url,params=self.auth_details)
            #print response
            if response.status_code == 200:
                self.boards = response.json()['idBoards']
                #self.organizations = response.json()['organization']
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
            #print response
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
                board_filename = self.board_dir + '/'+ board
                print board_filename
                card_names = []
                card_sub_dir = self.card_dir + '/' + board + '/'
                if not os.path.isdir(card_sub_dir):
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
                with open(board_filename,'w') as board_fileobj:
                    pickle.dump(board_details,board_fileobj)
                    board_fileobj.close()
        except Exception as e:
            print str(e)
    

    def if_first_time(self):
        "Check if it is first time data being collected"
        result_flag = True
        result_flag = self.create_data_dir()
        try:
            if os.path.isdir(self.data_dir):
                check_if_board_exists = len(os.listdir(self.board_dir))
                check_if_card_exists = len(os.listdir(self.card_dir))
                if check_if_board_exists == 0 & check_if_card_exists == 0:
                    result_flag &= True
                else:
                    result_flag &= False
        except Exception as e:
            result_flag &= False
            print str(e)

        return result_flag

    
    def create_data_dir(self):
        "Create a new dir for data"
        result_flag = False
        try:
            if not os.path.isdir(self.data_dir):
                os.mkdir(self.data_dir)
                board_dir = os.path.join(self.data_dir,'board')
                card_dir = os.path.join(self.data_dir,'card')
                if not os.path.isdir(self.board_dir):
                    os.mkdir(self.board_dir)
                if not os.path.isdir(self.card_dir):
                    os.mkdir(self.card_dir)
            result_flag = True
        except Exception as e:
            print str(e)

        return result_flag


    def read_board_and_card_details(self):
        "Read the board and card details"
        board_details = {}
        card_details = {}
        try:
            boards = os.listdir(self.board_dir)
            print boards
            
            for board in boards:
                file_name = os.path.join(self.board_dir,board)
                print file_name
                with open(file_name,'r') as file_obj:
                    board_details[board] = pickle.load(file_obj)
                    file_obj.close()
                cards_dir = os.path.join(self.card_dir,board)
                print cards_dir
                cards = os.listdir(cards_dir)
            for card in cards:
                file_name = os.path.join(cards_dir,card)
                print file_name
                with open(file_name,'r') as file_obj:
                    card_details[card] = pickle.load(file_obj)
                    file_obj.close()
            print json.dumps(board_details,indent=4)
            print json.dumps(card_details,indent=4)

        except Exception as e:
            print str(e)


    def get_boards(self):
        "Get the boards"
        board_details = {}
        try:
            boards = os.listdir(self.board_dir)
            for board in boards:
                file_name = os.path.join(self.board_dir,board)
                with open(file_name,'r') as file_obj:
                    board_details[board] = pickle.load(file_obj)
                    file_obj.close()

        except Exception as e:
            print str(e)

        return board_details

    def get_cards(self):
        "Get the cards"
        organizations = []
        members = {}
        card_details = {}
        try:
            board_details = self.get_boards()
            for boardid,value in board_details.iteritems():
                cards_path = os.path.join(self.card_dir,boardid)
                cards = os.listdir(cards_path)
                for card in cards:
                    card_file_path = os.path.join(cards_path,card)
                    with open(card_file_path,'r') as file_obj:
                        card_details['card'] = pickle.load(file_obj)
                        file_obj.close()
                    
                    #membersid = card_details['card']['idMembers']
                    #print membersid
                    #for id in  membersid:
                        #print id
                        #url = "https://api.trello.com/1/members/" + id 
                        #get_members = requests.get(url=url,params=self.auth_details)
                        #print json.dumps(get_members.json(),indent=4)
                        
        except Exception as e:
            print str(e)

        return card_details


    def get_last_board(self,org):
        "Get the last board"
        #sprint self.boards[-1]
        last_board = None
        self.get_all_organizations()
        for name,value in self.organization_details.iteritems():
            if name == org:
                org_id = value['id']
        for i in range(len(self.boards),-1,-1):
            url = self.url + 'boards/' + self.boards[i-1]
            get_board = self.get(url=url,params=self.auth_details)
            #print json.dumps(get_board.json(),indent=4)
            if get_board.json()['idOrganization'] == org_id:
                last_board = get_board.json()
                break
        #url = self.url + 'organizations/'+ org_id + '/boards'
        #print url
        #get_last_board_details = self.get(url = url,params=self.auth_details)
        #print json.dumps(get_last_board_details.json(),indent=4)
        #members_url = self.url+ 'boards/' + self.boards[-2] + '/members'
        #get_members = self.get(url=members_url,params=self.auth_details)
        #print json.dumps(get_members.json(),indent=4)
        #print self.organizations
        #print self.organizations
        #for id in self.organizations:
            #url = self.url + 'organizations/' + id
            #get_org_details = self.get(url=url,params=self.auth_details)
            #print json.dumps(get_org_details.json(),indent=4)
        return last_board

    def get_all_organizations(self):
        "Get all the organizations"
        organization_details = {}
        organization_names = []
        try:
            for id in self.organizations:
                url = self.url + 'organizations/' + id
                get_org_details = self.get(url=url,params=self.auth_details)
                organization_details[get_org_details.json()['name']] = get_org_details.json()
                organization_names.append(get_org_details.json()['name'])
            self.organization_details = organization_details
        except Exception as e:
            print str(e)

        return organization_names


    def get_members_for_last_board(self,org_option):
        "Get members for the last board"
        last_board = self.get_last_board(org_option)
        url = self.url + 'boards/' + last_board['id'] + '/members'
        get_members = self.get(url=url,params=self.auth_details)
        return get_members.json()

    def return_name(self):
        "return the account name"

        return self.fullname

    def create_new_board(self,org_id,name):

        url = self.url + '/boards'
        self.auth_details['name'] = name
        self.auth_details['idOrganization'] = org_id 
        create_board = requests.post(url=url,params=self.auth_details)
        print create_board.status_code
        del self.auth_details['name']
        del self.auth_details['idOrganization']

    def add_members(self,board,members):

        self.auth_details['type'] = 'normal'
        for id in members:
            url = self.url + 'boards/' + board + '/members/' + id 
            print url 
            members_add = requests.put(url=url,params=self.auth_details)
            print members_add.status_code 
        del self.auth_details['type'] 
        

