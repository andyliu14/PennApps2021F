import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import uuid
from datetime import datetime
# cred_obj = firebase_admin.credentials.Certificate('creds.json')
# default_app = firebase_admin.initialize_app(cred_obj, {
#     'databaseURL': 'https://ikmr-ce98c-default-rtdb.firebaseio.com/'
# })
# ref = db.reference("/")

# countryJson = {
#     "Name": "United States of America",
#     "Id": str(uuid.uuid4())
# }

class firebaseClient:
    def __init__(self, credPath, dbUrl):
        self.creds = firebase_admin.credentials.Certificate(credPath)
        self.params = {
            'databaseURL': dbUrl
        }
        self.client = firebase_admin.initialize_app(self.creds, self.params)
        self.ref = db.reference("/")

    def onFirstConnect(self):
        self.ref = db.reference("/")
        initJson = {
            "Countries": {},
            "Files": {},
            "Users": {},
            "Accounts": {},
            "Contracts": {},
            "Networks": {}
        }

    def initCountry(self, countryName):
        countryJson = {
            "CountryId": str(uuid.uuid4()),
            "CountryName": countryName,
            "TimeStampCreated": str(datetime.utcnow()),
            "FileIds": [
            ],
            "AccountIds": [],
            "ContractIds": [],
            "UserIds": []
        }
        self.ref = db.reference("/Countries/" + countryJson["CountryId"])
        self.ref.set(countryJson)
        return countryJson["CountryId"]


    def getAllCountries(self):
        self.ref = db.reference("/Countries")
        return self.ref.get()
    def getCountryById(self, countryId):
        self.ref = db.reference("/Countries/" + str(countryId))
        return self.ref.get()
    
    def addCountrySubId(self, subId, countryId, subIdLocation):
        self.ref = db.reference("/Countries/" + str(countryId) + "/" + subIdLocation)
        if self.ref.get() is None:
            self.ref.set([str(subId)])
        else: 
            currentIds = list(self.ref.get())
            currentIds.append(str(subId))
            self.ref.set(currentIds)

    
    def removeCountrySubId(self, subId, countryId, subIdLocation):
        self.ref = db.reference("/Countries/" + str(countryId) + "/" + subIdLocation)
        if self.ref.get() is None:
            return
        currentIds = list(self.ref.get())
        if subId in currentIds:
            currentIds.remove(subId)
            self.ref.set(currentIds)

    def getCountrySubIds(self, countryId, subIdLocation):
        self.ref = db.reference("/Countries/" + str(countryId) + "/" + subIdLocation)
        subIds = self.ref.get()
        if subIds is None:
            return []
        else:
            return subIds

    def getCountryIdByName(self, countryName):
        self.ref = db.reference("/Countries")
        id = list(self.ref.order_by_child("CountryName").equal_to(countryName).limit_to_first(1).get().keys())[0]
        return id

    def addFile(self, fileName, countryId, cid, fileType, ratifiedTime = None, expiredTime = None):
        fileId = uuid.uuid4()
        self.ref = db.reference("/Files/" + str(fileId))
        fileJson = {
            "FileId": str(fileId),
            "FileName": fileName,
            "CountryId": str(countryId),
            "TimeStampCreated": str(datetime.utcnow()),
            "TimeStampExpired": expiredTime,
            "TimeStampRatified": ratifiedTime,
            "CID": str(cid),
            "FileType": fileType
        }
        self.ref.set(fileJson)
        self.addCountrySubId(str(fileId), str(countryId), "FileIds")
        return str(fileId)

    def getFileIdByName(self, fileName):
        self.ref = db.reference("/Files")
        id = list(self.ref.order_by_child("FileName").equal_to(fileName).limit_to_first(1).get().keys())[0]
        return id



    def getFileById(self, fileId):
        self.ref = db.reference("/Files/" + str(fileId))
        return self.ref.get()

    def addUser(self, name, userId, countryId, accountAddr, accountKey, permissionLevel):
        self.ref = db.reference("/Users/" + str(userId))
        userJson = {
            "UserId": str(userId),
            "Name": name,
            "PermissionLevel": permissionLevel,
            "CountryId": str(countryId),
            "AccountAddress": str(accountAddr),
            "AccountKey": str(accountKey)
        }
        self.ref.set(userJson)

        self.addCountrySubId(userId, countryId, "UserIds")
    
    def getUserById(self, userId):
        self.ref = db.reference("/Users/" + str(userId))
        return self.ref.get()

    def deleteUserById(self, userId):
        self.ref = db.reference("/Users/" + str(userId))
        user = self.ref.get()
        countryId = user["CountryId"]
        self.ref.set({})

        country = self.getCountryById(countryId)
        for key, value in country["UserIds"]:
            if value == str(userId):
                del country["UserIds"][key]
                break
        self.ref = db.reference("/Countries/" + str(countryId) + "/UserIds")
        self.ref.set(country["UserIds"])
        return userId
    def getClient(self):
        return self.client
    
    def addContract(self, name, address, abi, fileCID, countryId, fileType, ratifiedTime = None, expiredTime = None):
        contractId = uuid.uuid4()
        self.ref = db.reference("/Contracts/" + str(contractId))
        contractJson = {
            "Addresss": address,
            "Abi": str(abi),
            "CID": str(fileCID),
            "Name": name,
            "CountryId": str(countryId),
            "TimeStampCreated": str(datetime.utcnow()),
            "TimeStampExpired": expiredTime,
            "TimeStampRatified": ratifiedTime,
            "FileType": fileType
        }

        self.addCountrySubId(str(contractId), str(countryId), "ContractIds")
        self.ref.set(contractJson)
        return str(contractId)
    
    def deleteContract(self, contractId):
        self.ref = db.reference("/Contracts/" + str(contractId))
        self.ref.set({})
        return str(contractId)

    def getContractIdByName(self, contractName):
        self.ref = db.reference("/Contracts")
        id = list(self.ref.order_by_child("ContractName").equal_to(contractName).limit_to_first(1).get().keys())[0]
        return id

    def getContractById(self, contractId):
        self.ref = db.reference("/Contracts/" + str(contractId))
        return self.ref.get()



