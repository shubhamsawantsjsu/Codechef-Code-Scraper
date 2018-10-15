import json
import codecs
import requests
from bs4 import BeautifulSoup

extensions = {
    'JAVA': 'java',
    'CPP 4.3.2':'cpp',
    'CPP 4.9.2':'cpp',
    'C++11':'cpp',
}

class cchef():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.submissions = {}

    def getSubmissions(self):
        url = 'https://www.codechef.com/users/'+self.username
        response = self.session.get(url)
        parsed_response = BeautifulSoup(response.text, 'lxml')
        #print(parsed_response)
        submission_section = parsed_response.find('section', {'class': 'rating-data-section problems-solved'})
        #print(submission_section)
        for article in submission_section.findAll('article'):
            plist = article.findAll('p')
            for p in plist:
                problem = {}
                uid = p.find('a').text
                problem['submissions_link'] = p.find('a')['href']
                problem['submissions'] = []
                response = self.session.get('https://www.codechef.com' + problem['submissions_link'] + '?status=15')
                parsed_response = BeautifulSoup(response.text, 'lxml')
                for s in parsed_response.find('tbody').findAll('tr'):
                    submission = {}
                    tds = s.findAll('td')
                    submission['id'] = tds[0].text
                    submission['lang'] = tds[-2].text
                    submission['ext'] = 'txt'
                    if submission['lang'] in extensions:
                        submission['ext'] = extensions[submission['lang']]
                    submission['link'] = tds[-1].find('a')['href']
                    self.session.headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate, sdch, br',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive',
                        'Cookie': '_hjIncludedInSample=1; poll_time=1492695114844; notification=0; SESS6e579b771ca1747c067c1551742708ad=09db97cc6e5699f5c6b3ee06535b8bfd; __utmt=1; __asc=df2e6cf215b8b8fe49c49e8984b; __auc=b288342e157376f26b19b410a82; __utma=100380940.203442932.1474435759.1492664051.1492695035.182; __utmb=100380940.7.10.1492695035; __utmc=100380940; __utmz=100380940.1492409091.180.22.utmcsr=homebar|utmccn=sd17|utmcmd=banner',
                        'Host': 'www.codechef.com',
                        'Upgrade-Insecure-Requests': '1'
                    }
                    response = self.session.get('https://www.codechef.com' + submission['link'])
                    parsed_response = BeautifulSoup(response.text, 'lxml')
                    print(parsed_response)
                    submission['code'] = ''
                    try:
                        for li in parsed_response.find('div', {'id': 'solutiondiv'}).find('ol').findAll('li'):
                            submission['code'] += li.text.strip('\n') + '\n'
                    except:
                        print('Exception occurred')
                        pass
                    problem['submissions'].append(submission)
                self.submissions[uid] = problem
