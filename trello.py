import requests
import json

class trello():
    "Trello class"
    def __init__(self,key,token):
        self.auth_details = {'key':key,'token':token}
        self.boards = []
        self.account_name = None 
        self.fullname = None
        self.id = None
        self.organizations = None 
        self.member_type = None 
        self.account_details = {}

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
                print self.account_details
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







    
