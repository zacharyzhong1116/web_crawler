import bs4 as bs
import urllib.request
import re
class Processor:

    def __init__(self,tag,url):
        self.url = url
        self.tag = tag



    def get_data(self):
        try:
            sauce = urllib.request.urlopen(self.url)
            soup = bs.BeautifulSoup(sauce,'lxml')
            s = str(soup.find('div', class_='abstr'))
            TAG_RE = re.compile(r'<[^>]+>')
            s = TAG_RE.sub('', s)
            print(s)
            #print(self.tag +'---->'+ s)


        except Exception as e:
            print(str(e))



