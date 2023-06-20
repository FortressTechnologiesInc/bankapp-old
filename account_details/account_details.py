from concurrent import futures
import random
import datetime

import grpc


from account_details_pb2 import *

import account_details_pb2_grpc


# creat a list of accounts and fill with dummy data

from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://waris:test1122@cluster0.jk2md4w.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['bank']
collection = db['accounts']





class AccountDetailsService(account_details_pb2_grpc.AccountDetailsServiceServicer):

    def getAccountDetails(self, request, context):
        accounts = collection.find()
        for account in accounts:
            if account['account_number'] == request.account_number:
                return GetAccountDetailResponse(account=Account(account_number=account['account_number'], account_holder_name=account['account_holder_name'], balance=account['balance'], currency=account['currency']))
        return GetAccountDetailResponse()
    
    # Todo: check if the account already exist or not
    
    def createAccount(self, request, context):

        account = {
            "email_id": request.email_id,
            "account_type": request.account_type,
            "address": request.address,
            "govt_id_number": request.govt_id_number,
            "government_id_type": request.government_id_type,
            # "account_holder_name": request.account_holder_name,
            'name' : request.name,
            "balance": 0,
            "currency": "USD"

        }

        # assign a random 16 digit account number
        account["account_number"] = f"IBAN{random.randint(1000000000000000, 9999999999999999)}" 
        # timestamp  the account creation
        account['created_at'] = datetime.datetime.now()
        # insert the account into the list of accounts
        collection.insert_one(account)
        return CreateAccountResponse(result=True)
    
    def getAccounts(self, request, context):
        
        email_id = request.email_id
        accounts = collection.find({"email_id": email_id})
        account_list = []
        for account in accounts:
            account_list.append(Account(account_number=account['account_number'], email_id=account['email_id'], account_type=account['account_type'], address=account['address'], govt_id_number=account['govt_id_number'], government_id_type=account['government_id_type'], name =account['name'], balance=account['balance'], currency=account['currency']))

  
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    account_details_pb2_grpc.add_AccountDetailsServiceServicer_to_server(AccountDetailsService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
