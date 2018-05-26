# Credit to KINOCK SEBASTIAN for this code
import tweepy

# Reading Consumer key and secret from consumerKeys File

consumerKeyFile = open("consumerKeys", "r")
consumerKey = consumerKeyFile.readline().strip()
consumerSecret = consumerKeyFile.readline().strip()
consumerKeyFile.close()

# authenticating twitter consumer key
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.secure = True
authUrl = auth.get_authorization_url()

# go to this url
print("Please Visit This link and authorize the app ==> " + authUrl)
print("Enter The Authorization PIN")

# writing access tokes to file
pin = raw_input().strip()
token = auth.get_access_token(verifier=pin)
accessTokenFile = open("accessTokens", "w")
accessTokenFile.write(token[0] + '\n')
accessTokenFile.write(token[1] + '\n')
'''
Here we initialize our consumer key and consumer secret with auth = tweepy.OAuthHandler().
With the auth object just create we get the authorization url using get_authorization_url() method of tweepy.
Now user can got to this url and enter his/her login credentials and verify app.
After verifying a pin will be returned.
We accept this pin and calls method get_access_toke(verifier = pin) with pin as argument
and fetch access token and access token secret. We save this in a file and use it when ever needed.
This token wont expire until user revoke access or we delete the application.
'''