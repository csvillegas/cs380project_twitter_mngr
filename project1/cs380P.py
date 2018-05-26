import tweepy
import re


def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)


def menu():
    print('This program gives limited access to an authenticated twitter account.\n'
          'With it you can post and delete your tweets, check your timeline,\n'
          'find others and follow them. You can even tweet an image.\n\n'

          'To use this program, enter any number of switches on the first input line.\n'
          'They can be in any order but must be accompanied by arguments properly formatted\n\n'

          '            [--help] : Man page. Looks like you found it already.\n\n'
          '         [--summary] : A quick synopsis.\n\n'
          '       [--bat=token] : Does nothing with this but will accept it.\n'
          '             EXAMPLE { --bat=cv.12345XXXXX\n\n'
          '     [--tweet] "STR" : Will post the text STR as your latest tweet. Please couch string in double quotes " "\n'
          '             EXAMPLE { --tweet "Hello Twitter! #myfirsttweet"\n\n'
          '    [--del] tweet_id : Delete a tweet you posted. Must provide the tweet\'s id. Use -u or -h to find these.\n'
          '             EXAMPLE { --del 999594070228975616\n\n'
          '      [--find] "STR" : Find another user on twitter. This provides their user id. You can search for other users by name or twitter handle. Make sure to couch in double quotes.\n'
          '             EXAMPLE { --find "ChrisVillegas" or --find "@my_handle"\n\n'
          '  [--follow] user_id : Follow the user with that id. Use -u ,-h, or --find to find these.\n'
          '             EXAMPLE { --follow 466648619\n\n'
          '[--unfollow] user_id : Unfollow the user with that id. Use -u ,-h, or --find to find these.\n'
          '             EXAMPLE { --unfollow 466648619\n\n'
          '   [-i] path/to/file : Tweets an image you have stored on your machine.\n'
          '             EXAMPLE { -i img.jpg\n\n'
          '       [-r] tweet_id : Retweet the tweet with that id. Use -u or -h to find these.\n'
          '             EXAMPLE { -r 999594070228975616\n\n'
          '        [-t] user_id : Prints timeline of user with that id. Timline shows 20 most recent tweets, their id, and the user who posted.\n'
          '             EXAMPLE { -t 466648619\n\n'
          '                [-u] : Prints authenticated user\'s timeline. Timline shows 20 most recent tweets, their id, and the user who posted. \n\n'
          '                [-h] : Print authenticated users home timeline. Timline shows 20 most recent tweets, their id, and the user who posted.\n\n')


def summary():
    print("SUMMARY: This program helps you manage your Twitter profile from the command line.")


def batstr():
    print("Your bat token is " + switchargs[0])
    switchargs.remove(switchargs[0])


# Post a new tweet with text provided
def post_tweet():
    tweet = textargs[0]
    textargs.remove(tweet)
    api.update_status(status=tweet)
    print("Your tweet has been posted.")


# Delete a tweet you posted by its id
def delete_tweet():
    tweet_id = switchargs[0]
    switchargs.remove(tweet_id)
    api.destroy_status(tweet_id)
    print("Tweet " + str(tweet_id) + " has been deleted.")


# Search for twitter profiles based on name or twitter handle
def find_user():
    user_name = textargs[0]
    textargs.remove(user_name)
    try:
        usr = api.get_user(user_name)
    except:
        print("Could not find who you were looking for. Try again.")
        return
    print("User name: " + usr.name)
    print("User id: " + str(usr.id))


# Follow another twitter profile by its id
def follow():
    friend_id = switchargs[0]
    switchargs.remove(friend_id)
    api.create_friendship(friend_id)
    friend = api.get_user(friend_id)
    print("You now follow @" + friend.screen_name + ".")


# Unfollow another twitter profile by its id
def unfollow():
    xfriend_id = switchargs[0]
    switchargs.remove(xfriend_id)
    api.destroy_friendship(xfriend_id)
    xfriend = api.get_user(xfriend_id)
    print("You no longer follow @" + xfriend.screen_name + ".")


# Tweet an image file saved on your local machine
def tweet_image():
    imagePath = switchargs[0]
    switchargs.remove(switchargs[0])
    api.update_with_media(imagePath, "")
    print("Your image tweet has been posted.")


# Retweet a post based on its id
def retweet():
    tweet_id = switchargs[0]
    switchargs.remove(tweet_id)
    api.retweet(tweet_id)
    print("You retweeted tweet " + str(tweet_id) + ".")


# produces text output of a user's page, specified by their id
def timeline():
    user_id = switchargs[0]
    switchargs.remove(user_id)
    tl = api.user_timeline(user_id)
    for s in tl:
        print("User name: " + s.user.name)
        print("User screen name: " + s.user.screen_name)
        print("User id: " + str(s.user.id))
        print("Tweet id: " + str(s.id))
        print("Tweet text: " + s.text)
        print('\n')


# produces text output of user page
def user_timeline():
    tl = api.user_timeline()
    for s in tl:
        print("Tweet id: " + str(s.id))
        print("Tweet text: " + s.text)
        print('\n')


# produces text output of home page
def home_timeline():
    tl = api.home_timeline()
    for s in tl:
        print("User name: " + s.user.name)
        print("User screen name: " + s.user.screen_name)
        print("User id: " + str(s.user.id))
        print("Tweet id: " + str(s.id))
        print("Tweet text: " + s.text)
        print('\n')


def main():
    for s in opts:
        if s in options:
            switchQ.append(s)
        else:
            switchargs.append(s)
    # Execute all switches
    for s in switchQ:
        options[s]()


# Global Variables
switchQ = []
switchargs = []
options = {
    '--help': menu,
    '--summary': summary,
    '--bat': batstr,
    '--tweet': post_tweet,
    '--del': delete_tweet,
    '--find': find_user,
    '--follow': follow,
    '--unfollow': unfollow,
    '-i': tweet_image,
    '-r': retweet,
    '-t': timeline,
    '-u': user_timeline,
    '-h': home_timeline
}

#  Accept two lines of input from user to start program. Second line must be .eot
args = raw_input()  # First line is for switches
textargs = re.findall('".+?"', args)  # Separate all "text" string switch arguments
for t in textargs:
    args = args.replace(t, '')  # Remove all textargs
textargs = [f[1:-1] for f in textargs]  # Remove quotations
opts = args.replace('=', ' ').split()  # Split options into tokens
# eot = ".eot"
eot = raw_input()

# Start program if switch args were entered correctly
if eot == ".eot":
    try:
        with open('consumerKeys', 'r') as consumerKeyFile, open('accessTokens', 'r') as accessTokenFile:
            consumerKey = consumerKeyFile.readline().strip()
            consumerSecret = consumerKeyFile.readline().strip()
            accessToken = accessTokenFile.readline().strip()
            accessSecret = accessTokenFile.readline().strip()
    except IOError as e:
        print('Operation failed: %s' % e.strerror)
    cfg = {
        "consumer_key": consumerKey,
        "consumer_secret": consumerSecret,
        "access_token": accessToken,
        "access_token_secret": accessSecret
    }
    consumerKeyFile.close()
    api = get_api(cfg)
    main()
else:
    print("Invalid Input. Please use .eot to end transmission.")
