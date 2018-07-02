# Author(s): Joseph Hadley, Jonathan Hunt
# Created : 2018-22-03
# Modified: 2018-22-03
# Description: this file keeps all of the api keys in one place out of the data
#   gathering scripts
#------------------------------------------------------------------------------
# class to get/store authentication keys
class AuthKeys:
    def __init__(self, consumerKey,consumerSecret,accessToken,accessTokenSecret):
        self.consumerKey = consumerKey
        self.consumerSecret = consumerSecret
        self.accessToken = accessToken
        self.accessTokenSecret = accessTokenSecret

class MySQLLogin:
    def __init__(self, username, password):
        self.username = username
        self.password = password
#------------------------------------------------------------------------------
#                             Hadley keys/sql login
#------------------------------------------------------------------------------
joeTwitter = AuthKeys()

joeNYT = AuthKeys(,
                None,
                None,
                None)

joeSQL = MySQLLogin("root", "")
#------------------------------------------------------------------------------
#                               Hunt keys
#------------------------------------------------------------------------------
#jonTwitter = AuthKeys()
#jonNYT = AuthKeys()

#------------------------------------------------------------------------------
#                          Functions to get info
#------------------------------------------------------------------------------
def getTwitterAuth(user):
    if user == 'jkhadley':
        return joeTwitter
    elif user == 'jthunt':
        return jonTwitter
    else:
        print("No user: " + str(user))

def getNYTimesAuth(user):
    if user == 'jkhadley':
        return joeNYT.consumerKey
    elif user == 'jthunt':
        return jonNYT
    else:
        print("No user: " + str(user))

def getSQLLogin(user):
    if user == 'jkhadley':
        return joeSQL
    elif user == 'jthunt':
        return jonNYT
    else:
        print("No user: " + str(user))
