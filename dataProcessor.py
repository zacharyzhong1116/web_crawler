import bs4 as bs
import urllib.request
import re
import time
from boto3.session import Session


class Processor:
    def __init__(self, tag, url):
        self.url = url
        self.tag = tag

    def get_data(self):
        try:
            res = dict()
            sauce = urllib.request.urlopen(self.url)
            soup = bs.BeautifulSoup(sauce, 'lxml')
            abstract = str(soup.find('div', class_='abstr'))

            if abstract is not None:
                TAG_RE = re.compile(r'<[^>]+>')
                title = TAG_RE.sub("", str(soup.find('title')))
                abstract = TAG_RE.sub('', abstract)
                keyWords = str(soup.find('div', class_='keywords'))

                if keyWords is not None:
                    keyWords = TAG_RE.sub('', keyWords.replace("KEYWORDS: ", ""))
                else:
                    keyWords = 'keyWords_404'
                date = time.strftime('%m-%d-%Y', time.localtime())
                paper_id = self.url.split('/')[-1]
                res['id'] = paper_id
                res['tag'] = self.tag
                res['title'] = title
                res['abstrcat'] = abstract
                res['keyWords'] = keyWords
                res['link'] = self.url
                res['date'] = date

                return res

        except Exception as e:
            print(str(e))

    def upload_data(self):

        res = self.get_data()

        asw_key_id = "***"
        aws_secret_access_key = "***+9"
        region = "***"
        session = Session(aws_access_key_id=asw_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)
        dynamodb = session.resource('dynamodb')
        table = dynamodb.Table("test")
        table.put_item(
            Item={
                'id': res['id'],
                "tag": res['tag'],
                "title": res['title'],
                "abstract": res['abstrcat'],
                "keyWords": res['keyWords'],
                "link": res['link'],
                "date": res['date']
            }
        )








