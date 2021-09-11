from firebase_admin import db
from flask import Flask, request, send_file, Response
from fireBaseClient import firebaseClient
from ipfsClient import IpfsClient
from fireBaseUserClient import fireBaseUserClient
import json
from datetime import datetime
import sys
app = Flask(__name__)

connect_addr = '/ip4/127.0.0.1/tcp/5001'
db_url = 'https://ikmr-ce98c-default-rtdb.firebaseio.com/'
ipfs_client = IpfsClient(connect_addr)
fb_client = firebaseClient('creds.json', db_url)
actual_client = fb_client.getClient()
user_client = fireBaseUserClient(actual_client)
standard_format = '%Y-%m-%d %H:%M:%S.%f'

@app.route('/api/v1/files/uploadFile', methods=['Post'])
#Token
def upload_file():
    file = request.files['file']
    file_name = request.form['fileName']
    country_name = request.form['countryName']
    # user_token = request.form['token']
    file_type = request.form['fileType']
    ratifiedTime = request.form.get('ratifiedTime')
    expiredTime = request.form.get('expiredTime')
    
    # user_id = user_client.getCurrentUserId(user_token)
    # current_user = fb_client.getUserById(user_id)
    #currentPermissionLevel = current_user["PermissionLevel"]
    currentPermissionLevel = "SuperAdmin"
    isAuthenticated = True
    countryId = fb_client.getCountryIdByName(country_name)
    # if(currentPermissionLevel.equals("SuperAdmin")):
    #     isAuthenticated = True
    # elif (currentPermissionLevel.equals("Admin")):
        
    #     isAuthenticated = (current_user["CountryId"] == countryId)
    # else:
    #     return json.dumps({'success':False}), 401, {'ContentType':'application/json'} 
    

    if(not isAuthenticated):
        return json.dumps({'success':False}), 401, {'ContentType':'application/json'} 


    cid = ipfs_client.add_file(file)

    file_id = fb_client.addFile(file_name, countryId, cid, file_type, ratifiedTime, expiredTime)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/api/v1/files/deleteFile', methods = ['Delete'])
#Token
def delete_file():
    return

@app.route('/api/v1/files/listFiles', methods = ['Get'])
#Filters
#Effective
#Future
#Expired
#All
def list_files():
    country_name = request.args.get('countryName')
    filter = request.args.get('filter')
    countryId = fb_client.getCountryIdByName(country_name)
    country = fb_client.getCountryById(countryId)
   
    if not "FileIds" in country:
        return Response(status=200)
    print(country["FileIds"])
    
    fileIds = country["FileIds"].values()
    print(fileIds)
    fileList = []
    for id in fileIds:
        print(id)
        file = fb_client.getFileById(id)
        print(file)
        currentTime = datetime.utcnow().timestamp()


        
        expiredString = None
        ratifiedString = None

        if("TimeStampRatified" in file):
            ratifiedString = (file["TimeStampRatified"])
        
        if("TimeStampExpired" in file):
            expiredString = file["TimeStampExpired"]
        ratifiedTime = 0
        expiredTime = sys.float_info.max
        if ratifiedString is not None:
            ratifiedTime = datetime.strptime(ratifiedString, standard_format).timestamp()
        if expiredString is not None:
            expiredTime = datetime.strptime(expiredString, standard_format).timestamp()
        


        if filter == 'All':
            fileList.append(file)
        elif filter == ('Expired'):
            if(expiredTime < currentTime):
                fileList.append(file)
        elif filter == ('Future'):
            if(currentTime < ratifiedTime):
                fileList.append(file)
        elif filter == 'Effective':
            if(currentTime > ratifiedTime and currentTime < expiredTime):
                fileList.append(file)
        else:
            return json.dumps({'success':False}), 400, {'ContentType':'application/json'} 

        if(fileList is not None):
            sortedFileList = sorted(fileList, key = lambda f: (f['FileName']))
        else:
            sortedFileList = []

        response = app.response_class(
            response=json.dumps(sortedFileList),
            status=200,
            mimetype='application/json'
            )
        return response
    


@app.route('/api/v1/files/getFile', methods = ['Get'])
def get_file():

    file_name = request.args.get('fileName')
    fileId = fb_client.getFileIdByName(file_name)
    file = fb_client.getFileById(fileId)
    cid = file["cid"]
    file_data = ipfs_client.retrieve_file(cid)
    return send_file(file_data, as_attachment = False)


@app.route('/api/v1/countries/getCountries', methods = ['Get'])
def get_countries():
    allCountriesData = fb_client.getAllCountries()
    response = app.response_class(
            response=json.dumps(allCountriesData),
            status=200,
            mimetype='application/json'
            )
    return response

@app.route('/api/v1/countries/createCountry', methods = ['Post'])
def create_country():
    country_name = request.form['countryName']
    # user_token = request.form['token']

    # user_id = user_client.getCurrentUserId(user_token)
    # current_user = fb_client.getUserById(user_id)
    # currentPermissionLevel = current_user["PermissionLevel"]
    # currentPermissionLevel = "SuperAdmin"
    # if(not currentPermissionLevel == ("SuperAdmin")):
    #     return json.dumps({'success':False}), 401, {'ContentType':'application/json'} 
    
    fb_client.initCountry(country_name)
    
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/api/v1/countries/deleteCountry', methods = ['Delete'])
def delete_country():
    country_name = request.args.get('countryName')
    # user_token = request.args.get('token')

    # user_id = user_client.getCurrentUserId(user_token)
    # current_user = fb_client.getUserById(user_id)
    # currentPermissionLevel = current_user["PermissionLevel"]
    # currentPermissionLevel = "SuperAdmin"
    # if(not currentPermissionLevel == ("SuperAdmin")):
    #     return json.dumps({'success':False}), 401, {'ContentType':'application/json'} 

    return


@app.route('/api/v1/users/registerUser', methods = ['Post'])
def register_user():
    country_name = request.args.get('countryName')
    user_token = request.args.get('token')

    user_id = user_client.getCurrentUserId(user_token)
    current_user = fb_client.getUserById(user_id)
    currentPermissionLevel = current_user["PermissionLevel"]
    currentPermissionLevel = "SuperAdmin"
    if(not currentPermissionLevel == ("SuperAdmin")):
        return json.dumps({'success':False}), 401, {'ContentType':'application/json'} 
    
    email = request.form["Email"]
    password = request.form["Password"]
    name = request.form["Name"]
    countryName = request.form["CountryName"]
    permissionLevel = "Admin"
    
    new_id = user_client.createUser(email, password, name, countryName, permissionLevel)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/api/v1/users/deleteUser', methods = ['Delete'])
def delete_user():
    userId = request.args.get('userId')
    token = request.args.get('token')
    currentUserId = user_client.getCurrentUserId(token)
    currentUser = fb_client.getUserById(currentUserId)
    currentPermissionLevel = currentUser["PermissionLevel"]
    isAuthenticated = False

    if(currentPermissionLevel.equals("SuperAdmin")):
        isAuthenticated = True
    elif (currentPermissionLevel.equals("Admin")):
        isAuthenticated = (currentUser["CountryId"] == fb_client.getUserById(userId)["CountryId"])
    else:
        return json.dumps({'success':False}), 401, {'ContentType':'application/json'} 
    
    if(not isAuthenticated):
        return json.dumps({'success':False}), 401, {'ContentType':'application/json'} 
    
    user_client.deleteUser(userId)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/api/v1/users/listUsers', methods = ['Get'])
def list_users():
    countryName = request.args.get('countryName')
    
    countryId = fb_client.getCountryIdByName(countryName)
    country = fb_client.getCountryById(countryId)

    if("UserIds" not in country):
        return Response(status=200)

    userIds = country["UserIds"]
    users = []
    for id in userIds:
        user = fb_client.getUserById(id)
        users.append(user)


    if(users is not None):
        sortedUsers = sorted(users, key = lambda f: (f['Name']))
    else:
        sortedUsers = []

    response = app.response_class(
        response=json.dumps(sortedUsers),
        status=200,
        mimetype='application/json'
        )
    return response

app.run()
