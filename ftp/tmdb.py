# -*- coding: utf-8 -*-

import requests
from requests.compat import json, str

from resources.lib.modules import control
from resources.lib.modules import log_utils


USERNAME = control.setting('tmdb.user')
PASSWORD = control.setting('tmdb.pass')
SESSION_ID = control.setting('tmdb.session')
ACCOUNT_ID = control.setting('tmdb.id')

API_KEY = control.setting('tmdb.api')
if not API_KEY:
    API_KEY = '<<api_key>>'

API_URL = 'https://api.themoviedb.org/3/'
HEADERS = {'Content-Type': 'application/json;charset=utf-8'}


############################################
############################################


def authTMDb():
    try:
        if not SESSION_ID == '':
            if control.yesnoDialog('A Session Already Exists.' + '[CR]' + 'Delete Session?', heading='TMDB'):
                delete_session()
            raise Exception()
        if USERNAME == '' or PASSWORD == '':
            control.infoDialog('Check Account Credentials.', sound=True)
            raise Exception()
        request_token = create_request_token()
        if not request_token:
            raise Exception()
        request_token = create_session_with_login(request_token)
        if not request_token:
            raise Exception()
        session_id = create_session(request_token)
        if not session_id:
            raise Exception()
        control.setSetting(id='tmdb.session', value=session_id)
        control.infoDialog('TMDb Auth Successful.', sound=True)
        return get_account_details(session_id)
    except:
        log_utils.log('authTMDb', 1)
        control.infoDialog('TMDb Auth Failed.', sound=True)
        return


############################################
############################################


#Create Request Token
#get/authentication/token/new

#Create a temporary request token that can be used to validate a TMDB user login. 


#https://api.themoviedb.org/3/authentication/token/new?api_key=<<api_key>>


#{
  #"success": true,
  #"expires_at": "2016-08-26 17:04:39 UTC",
  #"request_token": "ff5c7eeb5a8870efe3cd7fc5c282cffd26800ecd"
#}


def create_request_token():
    try:
        url = API_URL + 'authentication/token/new?api_key=%s' % API_KEY
        result = requests.get(url, headers=HEADERS).json()
        if result.get('success') is True:
            request_token = result.get('request_token')
            return request_token
        else:
            control.infoDialog('TMDb create_request_token Failed', sound=True)
            return None
    except:
        control.infoDialog('TMDb create_request_token Failed', sound=True)
        log_utils.log('create_session_id', 1)
        return None


############################################
############################################


#Create Session With Login
#post/authentication/token/validate_with_login

#This method allows an application to validate a request token by entering a username and password.

#Not all applications have access to a web view so this can be used as a substitute.

#Please note, the preferred method of validating a request token is to have a user authenticate the request via the TMDB website.

#If you decide to use this method please use HTTPS.


#https://api.themoviedb.org/3/authentication/token/validate_with_login?api_key=<<api_key>>


#Request Body application/json
#{
  #"username": "johnny_appleseed",
  #"password": "test123",
  #"request_token": "1531f1a558c8357ce8990cf887ff196e8f5402ec"
#}


#Responses application/json
#{
  #"success": true,
  #"expires_at": "2018-07-24 04:10:26 UTC",
  #"request_token": "1531f1a558c8357ce8990cf887ff196e8f5402ec"
#}


def create_session_with_login(request_token):
    try:
        url = API_URL + 'authentication/token/validate_with_login?api_key=%s' % API_KEY
        post = {
            "username": "%s" % str(USERNAME),
            "password": "%s" % str(PASSWORD),
            "request_token": "%s" % str(request_token)
        }
        result = requests.post(url, data=json.dumps(post), headers=HEADERS).json()
        log_utils.log('create_session_with_login result: \n' + repr(result))
        if result.get('success') is True:
            request_token = result.get('request_token')
            return request_token
        else:
            control.infoDialog('TMDb create_session_with_login Failed', sound=True)
            return None
    except:
        control.infoDialog('TMDb create_session_with_login Failed', sound=True)
        log_utils.log('create_session_with_login', 1)
        return None



############################################
############################################


#Create Session
#post/authentication/session/new

#You can use this method to create a fully valid session ID once a user has validated the request token.


#https://api.themoviedb.org/3/authentication/session/new?api_key=<<api_key>>


#Request Body application/json
#{
  #"request_token": "6bc047b88f669d1fb86574f06381005d93d3517a"
#}


#Responses application/json
#{
  #"success": true,
  #"session_id": "79191836ddaa0da3df76a5ffef6f07ad6ab0c641"
#}


def create_session(request_token):
    try:
        url = API_URL + 'authentication/session/new?api_key=%s' % API_KEY
        post = {"request_token": "%s" % str(request_token)}
        result = requests.post(url, data=json.dumps(post), headers=HEADERS).json()
        log_utils.log('create_session result: \n' + repr(result))
        if result.get('success') is True:
            session_id = result.get('session_id')
            return session_id
        else:
            control.infoDialog('TMDb create_session Failed', sound=True)
            return None
    except:
        control.infoDialog('TMDb create_session Failed', sound=True)
        log_utils.log('create_session', 1)
        return None



############################################
############################################


#Delete Session
#delete/authentication/session

#If you would like to delete (or "logout") from a session, call this method with a valid session ID.


#https://api.themoviedb.org/3/authentication/session?api_key=<<api_key>>


#Request Body application/json
#{
  #"session_id": "2629f70fb498edc263a0adb99118ac41f0053e8c"
#}


#Responses application/json
#{
  #"success": true
#}


def delete_session():
    try:
        if SESSION_ID == '':
            return
        url = API_URL + 'authentication/session?api_key=%s' % API_KEY
        post = {"session_id": "%s" % str(SESSION_ID)}
        result = requests.delete(url, data=json.dumps(post), headers=HEADERS).json()
        if result.get('success') is True:
            control.setSetting(id='tmdb.session', value='')
            control.infoDialog('TMDb delete_session Successful', sound=True)
        else:
            control.infoDialog('TMDb delete_session Failed', sound=True)
    except:
        control.infoDialog('TMDb delete_session Failed', sound=True)
        log_utils.log('delete_session', 1)
        pass


############################################
############################################


#Get Details
#get/account

#Get your account details.


#https://api.themoviedb.org/3/account?api_key=<<api_key>>&session_id=hhh


#Responses application/json
#{
  #"avatar": {
    #"gravatar": {
      #"hash": "c9e9fc152ee756a900db85757c29815d"
    #}
  #},
  #"id": 548,
  #"iso_639_1": "en",
  #"iso_3166_1": "CA",
  #"name": "Travis Bell",
  #"include_adult": true,
  #"username": "travisbell"
#}


def get_account_details(session_id):
    try:
        url = API_URL + 'account?api_key=%s&session_id=%s' % (API_KEY, session_id)
        result = requests.get(url, headers=HEADERS).json()
        account_username = result['username']
        account_name = result['name']
        account_id = result['id']
        account_include_adult = result['include_adult']
        account_iso_639_1 = result['iso_639_1']
        account_iso_3166_1 = result['iso_3166_1']
        control.setSetting(id='tmdb.id', value=str(account_id))
        message = ('username: %s' % str(account_username) + '[CR]' + 'name: %s' % str(account_name) + '[CR]' + 'id: %s' % str(account_id) + '[CR]' + 'include_adult: %s' % str(account_include_adult) + '[CR]' + 'iso_639_1: %s' % str(account_iso_639_1) + '[CR]' + 'iso_3166_1: %s' % str(account_iso_3166_1))
        return control.okDialog(message, heading='TMDB Account Details')
    except:
        log_utils.log('get_account_details', 1)
        pass


############################################
############################################


#https://api.themoviedb.org/3/movie/9600/videos?api_key=<<api_key>>&language=en-US


def tmdb_trailer(tmdb):
    try:
        url = API_URL + 'movie/%s/videos?api_key=%s&language=en-US' % (tmdb, API_KEY)
        result = requests.get(url, headers=HEADERS).json()
        items = result['results'] #{"id":9600,"results":[
        for item in items:
            iso_639_1 = item['iso_639_1'] #"iso_639_1":"en",
            iso_3166_1 = item['iso_3166_1'] #"iso_3166_1":"US",
            name = item['name'] #"name":"Big Momma's House - Trailer HQ",
            key = item['key'] #"key":"njhwlzuPXv4",
            id = item['id'] #"id":"533ec666c3a3685448001712"
            published_at = item['published_at'] #"published_at":"2011-06-23T00:53:41.000Z",
            site = item['site'] #"site":"YouTube",
            size = item['size'] #"size":480,
            type = item['type'] #"type":"Trailer",
            official = item['official'] #"official":false,
    except:
        log_utils.log('tmdb_trailer', 1)
        pass


############################################
############################################


#Get Created Lists
#get/account/{account_id}/lists

#Get all of the lists created by an account. Will invlude private lists if you are the owner.


#https://api.themoviedb.org/3/account/{account_id}/lists?api_key=<<api_key>>&language=en-US&session_id=<session_id>&page=1


#Responses application/json
#{
  #"page": 1,
  #"results": [
    #{
      #"description": "Name pretty much says it all, here's the top 50 grossing films of all time.",
      #"favorite_count": 0,
      #"id": 10,
      #"item_count": 0,
      #"iso_639_1": "en",
      #"list_type": "movie",
      #"name": "Top 50 Grossing Films of All Time (Worldwide)",
      #"poster_path": null
    #}
  #],
  #"total_pages": 4,
  #"total_results": 61
#}


############################################
############################################


#Get Favorite Movies
#get/account/{account_id}/favorite/movies

#Get the list of your favorite movies.


#https://api.themoviedb.org/3/account/{account_id}/favorite/movies?api_key=<<api_key>>&session_id=<session_id>&language=en-US&page=1
#https://api.themoviedb.org/3/account/{account_id}/favorite/movies?api_key=<<api_key>>&session_id=<session_id>&language=en-US&sort_by=created_at.asc&page=1
#https://api.themoviedb.org/3/account/{account_id}/favorite/movies?api_key=<<api_key>>&session_id=<session_id>&language=en-US&sort_by=created_at.desc&page=1


#Responses application/json
#{
  #"page": 1,
  #"results": [
    #{
      #"adult": false,
      #"backdrop_path": null,
      #"genre_ids": [
        #16
      #],
      #"id": 9806,
      #"original_language": "en",
      #"original_title": "The Incredibles",
      #"overview": "PLOT",
      #"release_date": "2004-11-04",
      #"poster_path": null,
      #"popularity": 0.167525,
      #"title": "The Incredibles",
      #"video": false,
      #"vote_average": 6.8,
      #"vote_count": 1584
    #}
  #],
  #"total_pages": 4,
  #"total_results": 77
#}


############################################
############################################


#Get Favorite TV Shows
#get/account/{account_id}/favorite/tv

#Get the list of your favorite TV shows.


#https://api.themoviedb.org/3/account/{account_id}/favorite/tv?api_key=<<api_key>>&session_id=<session_id>&language=en-US&page=1
#https://api.themoviedb.org/3/account/{account_id}/favorite/tv?api_key=<<api_key>>&session_id=<session_id>&language=en-US&sort_by=created_at.asc&page=1
#https://api.themoviedb.org/3/account/{account_id}/favorite/tv?api_key=<<api_key>>&session_id=<session_id>&language=en-US&sort_by=created_at.desc&page=1


#Responses application/json
#{
  #"page": 1,
  #"results": [
    #{
      #"backdrop_path": null,
      #"first_air_date": "2007-09-24",
      #"genre_ids": [
        #10759
      #],
      #"id": 1404,
      #"original_language": "en",
      #"original_name": "Chuck",
      #"overview": "PLOT",
      #"origin_country": [
        #"US"
      #],
      #"poster_path": null,
      #"popularity": 0.125125,
      #"name": "Chuck",
      #"vote_average": 8.2,
      #"vote_count": 37
    #}
  #],
  #"total_pages": 3,
  #"total_results": 52
#}


############################################
############################################


#Mark as Favorite
#post/account/{account_id}/favorite

#This method allows you to mark a movie or TV show as a favorite item.


#header = 'Content-Type: application/json;charset=utf-8'

#https://api.themoviedb.org/3/account/{account_id}/favorite?api_key=<<api_key>>&session_id=<session_id>


#Request Body application/json
#{
  #"media_type": "movie",
  #"media_id": 550,
  #"favorite": true
#}


#Responses application/json
#{
  #"status_code": 12,
  #"status_message": "The item/record was updated successfully."
#}


############################################
############################################


#Get Movie Watchlist
#get/account/{account_id}/watchlist/movies

#Get a list of all the movies you have added to your watchlist.


#https://api.themoviedb.org/3/account/{account_id}/watchlist/movies?api_key=<<api_key>>&language=en-US&session_id=<session_id>&sort_by=created_at.asc&page=1


#Responses application/json
#{
  #"page": 1,
  #"results": [
    #{
      #"adult": false,
      #"backdrop_path": null,
      #"genre_ids": [
        #18
      #],
      #"id": 76726,
      #"original_language": "it",
      #"original_title": "Chronicle",
      #"overview": "PLOT",
      #"release_date": "2012-02-02",
      #"poster_path": null,
      #"popularity": 0.237951,
      #"title": "Chronicle",
      #"video": false,
      #"vote_average": 6.2,
      #"vote_count": 545
    #}
  #],
  #"total_pages": 14,
  #"total_results": 277
#}


############################################
############################################


#Get TV Show Watchlist
#get/account/{account_id}/watchlist/tv

#Get a list of all the TV shows you have added to your watchlist.


#https://api.themoviedb.org/3/account/{account_id}/watchlist/tv?api_key=<<api_key>>&language=en-US&session_id=<session_id>&sort_by=created_at.asc&page=1


#Responses application/json
#{
  #"page": 1,
  #"results": [
    #{
      #"backdrop_path": null,
      #"first_air_date": "2013-09-26",
      #"genre_ids": [
        #35
      #],
      #"id": 58932,
      #"original_language": "en",
      #"original_name": "The Crazy Ones",
      #"overview": "PLOT",
      #"origin_country": [
        #"US"
      #],
      #"poster_path": null,
      #"popularity": 0.075407,
      #"name": "The Crazy Ones",
      #"vote_average": 5.3,
      #"vote_count": 4
    #}
  #],
  #"total_pages": 4,
  #"total_results": 64
#}


############################################
############################################


#Add to Watchlist
#post/account/{account_id}/watchlist

#Add a movie or TV show to your watchlist.

#header 'Content-Type: application/json;charset=utf-8'


#https://api.themoviedb.org/3/account/{account_id}/watchlist?api_key=<<api_key>>&session_id=<session_id>


#Request Body application/json
#{
  #"media_type": "movie",
  #"media_id": 11,
  #"watchlist": true
#}


#Responses application/json
#{
  #"status_code": 1,
  #"status_message": "Success."
#}


############################################
############################################


#Get Account States
#get/movie/{movie_id}/account_states

#Grab the following account states for a session:

    #Movie rating
    #If it belongs to your watchlist
    #If it belongs to your favourite list


#https://api.themoviedb.org/3/movie/{movie_id}/account_states?api_key=<<api_key>>&session_id=hhh


#Responses application/json

#{
  #"id": 550,
  #"favorite": true,
  #"rated": {
    #"value": 8
  #},
  #"watchlist": false
#}



