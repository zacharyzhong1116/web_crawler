
from general import *
from dataProcessor import *


class Spider:

    project_name = ''
    base_url = ''
    # the file where we store the link we need to crawl
    queue_file = ''
    # the file we have crawled
    crawled_file = ''
    # the taget we need to search
    target_path = ''
    queue = set()
    crawled = set()


    def __init__(self, project_name, base_url,target_path):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.target_path = target_path
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page(Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Updates user display, fills queue and updates files

    @staticmethod
    def crawl_page(page_url):
        if page_url not in Spider.crawled:
            print(' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.process_links(page_url)

            Spider.update_files()

    #assemble url
    @staticmethod
    def assemble_first_layer_urls(base_rul):
        res = dict()
        with open(Spider.target_path) as f:
            for tag in f:
                res[tag] = base_rul + tag
        return res

    @staticmethod
    def assemble_second_layer_urls(base_url):
        res = dict()
        first_layer_links = Spider.assemble_first_layer_urls(Spider.base_url)
        for tag,link in first_layer_links.items():
            print('111111111')
            print(link)
            sauce = urllib.request.urlopen(link)
            soup = bs.BeautifulSoup(sauce, 'lxml')
            second_links = set()
            for pp in soup.find_all('p', class_='title'):
                num = pp.find('a').get('href').split('/')[2]
                second_links.add(base_url+ num)
            res[tag] = second_links
        return res

    @staticmethod
    def process_links(page_url):
        second_layer_links = Spider.assemble_second_layer_urls('https://www.ncbi.nlm.nih.gov/pubmed/')
        for tag,links in second_layer_links.items():
            try:
                for link in links:
                    print(link)
                    processor = Processor(tag,link)
                    processor.get_data()
                    Spider.add_links_to_queue(link)
                    Spider.queue.remove(link)
                    Spider.crawled.add(link)
            except Exception as e:
                print(str(e))
                return set()



    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(url):

        if (url not in Spider.queue) and (url not in Spider.crawled):
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
print("11111")
s = Spider('sjsu','https://www.ncbi.nlm.nih.gov/pubmed/?term=','target.txt')
s.crawl_page('http://www.sjsu.edu/')


