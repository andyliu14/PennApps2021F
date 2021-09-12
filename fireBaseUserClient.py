import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import db
import json
import uuid
from datetime import datetime
from fireBaseClient import firebaseClient
import uuid

class fireBaseUserClient:
    def __init__(self, inputClient):
        #self.client  = firebaseClient('creds.json', 'https://ikmr-ce98c-default-rtdb.firebaseio.com/')
        self.client = inputClient
    def getCurrentUserId(self, token):
        decoded_token = auth.verify_id_token(str(token))
        uid = decoded_token['uid']
        return uid

    def createUser(self, email, password, name, countryName, accountAddr, accountKey, permissionLevel):

        countryId = self.client.getCountryIdByName(countryName)
       

        userId = uuid.uuid4()
        auth.create_user(email = email, 
            uid = str(userId),
            password = password,
            display_name = name
        )
        
    
        self.client.addUser(name, userId, countryId, str(accountAddr), str(accountKey), permissionLevel)
        return userId

    
    def deleteUser(self, userId):

        auth.delete_user(str(userId))
        self.client.deleteUser(userId)
    
    def createSuperUser(self, email, password, name):
        unId = self.client.initCountry("United Nations")
        userId = uuid.uuid4()
        auth.create_user(email = email, 
            uid = str(userId),
            password = password,
            display_name = name
        )
        return userId


# superId = client.createSuperUser("test14@gmail.com", "test12351", "United Nations User")

# print(superId)
# print(auth.get_user(str(superId)).email)

    
        


    
    
