from concurrent import futures
import random
import datetime
import os
import logging
import grpc
# Configure the logging settings
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



from transaction_pb2 import * 

import transaction_pb2_grpc 


from pymongo.mongo_client import MongoClient
# uri = "mongodb+srv://waris:test1122@cluster0.jk2md4w.mongodb.net/?retryWrites=true&w=majority"
# uri = "mongodb://root:example@localhost:27017/"
db_host = os.getenv("DATABASE_HOST", "localhost")
uri = f"mongodb://root:example@{db_host}:27017/"

client = MongoClient(uri)
db = client['bank']
collection_accounts = db['accounts']
collection_transactions = db['transactions']





class TransactionService(transaction_pb2_grpc.TransactionServiceServicer):

    def __getAccount(self, account_num):
        r = None

        accounts = collection_accounts.find()
        # print(f"Accounts: {list(accounts)}") 
        for acc in accounts:
            if acc['account_number'] == account_num:
                r = acc
                break     
        # print(f"Account {r}")
        return r
    
    def __doTransaction(self, sender, receiver, amount, reason=""):
        if sender['balance'] < amount:
            return False
        
        sender['balance'] -= amount
        receiver['balance'] += amount

        # update sender account
        collection_accounts.update_one({"account_number": sender['account_number']}, {"$set": {"balance": sender['balance']}})
        
        # update receiver account
        collection_accounts.update_one({"account_number": receiver['account_number']}, {"$set": {"balance": receiver['balance']}})

        # add transaction
        collection_transactions.insert_one({"sender": sender['account_number'], "receiver": receiver['account_number'], "amount": amount, "reason":reason, 'time_stamp': datetime.datetime.now()})


        return True
    
    def __transfer(self, sender_account, receiver_account, amount, reason):
        if sender_account is not None or receiver_account is not None:
            result = self.__doTransaction(sender_account, receiver_account, amount, reason=reason)
            
            logging.debug(f"---> sender: {sender_account}" )
            logging.debug(f"--->receiver: {receiver_account}")
            if result: 
                return TransactionResponse(success=result, message="Transaction Successful")
            
        return TransactionResponse(success=False, message="Transaction Failed")


    def SendMoney(self, request, context):
        
        sender_account =  self.__getAccount(request.sender_account_number)
        receiver_account = self.__getAccount(request.receiver_account_number)
        return self.__transfer(sender_account, receiver_account, request.amount, request.reason)
        
        

    def getTransactionsHistory(self, request, context):
        account_number = request.account_number 
        # print(f"Account Number: {account_number}")
        
        # find based on account number only based on sender
        transactions_credit = collection_transactions.find({"sender":account_number})
        transactions_debit = collection_transactions.find({"receiver":account_number})
        
        # print(f"--------T: {transactions_itr}")
        t = Transaction()
        # print(f"--- t: {t}")

        transactions_list = []
        for t in transactions_credit:
            temp_t = Transaction(account_number=t['receiver'], amount=t['amount'], reason=t['reason'], time_stamp=f"{t['time_stamp']}", type= "credit")
            transactions_list.append(temp_t)
        
        for t in transactions_debit:
            temp_t = Transaction(account_number=t['sender'], amount=t['amount'], reason=t['reason'], time_stamp=f"{t['time_stamp']}", type= "debit")
            transactions_list.append(temp_t)
        
        # print(transactions_list)
        
        
        return GetALLTransactionsResponse(transactions=transactions_list)
    
    def __getAccountwithEmail(self, email):
        document = None
        checking_account = collection_accounts.find({'email': email, 'account_type': 'Checking'})
        # logging.debug(f"Checking Account: {checking_account}")

        if checking_account.count() == 1:
            document = checking_account[0]
            logging.debug(f"Checking Account: {document}")
            return document
        else:
            saving_account = collection_accounts.find({'email': email, 'account_type': 'Savings'})
            if saving_account.count() == 1:
                document = saving_account[0]
                logging.debug(f"Savings Account: {document}")
                return document

            # logging.debug(f"Savings Account: {document}")
        logging.debug('No Account Found')      
        return document
    
    def Zelle(self, request, context):
        sender_email = request.sender_email
        receiver_email = request.receiver_email
        amount = request.amount
        reason = request.reason

        sender_account = self.__getAccountwithEmail(sender_email)
        receiver_account = self.__getAccountwithEmail(receiver_email)

        return self.__transfer(sender_account, receiver_account, amount, reason)



        

         
        
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transaction_pb2_grpc.add_TransactionServiceServicer_to_server(TransactionService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()


