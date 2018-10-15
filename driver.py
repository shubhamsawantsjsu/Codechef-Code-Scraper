import json as j
from scrape.scraper import *

def initialization():
    try:
        with open('config.json') as user_data_file:
            userData = j.load(user_data_file)
            if userData['codechef_username'] != '':
                return userData
            else:
                print('Configure userData.json and set credentials for Codechef or Codeforces Account. Thanks')
                return None
    except:
        print('Hello bud, It seems that you haven\'t configured userData.json file or there\'s some error. \n Please configure it and execute this later. Thanks.')
        return None

def main():
    userData = initialization()
    if userData is not None:
        if userData['codechef_username']!='':
            print(userData['codechef_username'])
            print(userData['codechef_username']+', I\'m scraping codechef for you.')
            test_cchef(userData['codechef_username'])
    else:
        print('Aborting....')
        return

def test_cchef(username):
    user = cchef(username, '')
    user.getSubmissions()

if __name__ == '__main__':
    main()
