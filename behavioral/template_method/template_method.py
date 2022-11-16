import abc
import html
import urllib.request
import xml.etree.ElementTree as ET


class AbstractNewsParser(abc.ABC):

    def print_top_news(self):
        """Template method. Returns 3 latest news for every website"""
        url = self.get_url()
        raw_content = self.get_raw_content(url)
        content = self.parse_content(raw_content)

        cropped = self.crop(content)

        for item in cropped:
            print('-'*80)
            print('Title: ', item['title'])
            print('Content: ', item['content'])
            print('Link: ', item['link'])
            print('Published: ', item['published'])
            print('Id: ', item['id'])

    @abc.abstractmethod
    def get_url(self):
        pass

    def get_raw_content(self, url):
        return urllib.request.urlopen(url).read()

    @abc.abstractmethod
    def parse_content(self, raw_content):
        pass

    def crop(self, parsed_content, max_items=3):
        return parsed_content[:max_items]


class YahooParser(AbstractNewsParser):

    def get_url(self):
        return 'https://finance.yahoo.com/news/rssindex'

    def parse_content(self, raw_content):
        parsed_content = []

        root = ET.fromstring(raw_content)

        for element in root.iter('item'):

            parsed_item = {}

            parsed_item['title'] = element.find('title').text
            parsed_item['link'] = element.find('link').text
            parsed_item['content'] = element.find(
                'guid').text if element.find('guid') else "N/A"
            parsed_item['id'] = element.find(
                'guid').text if element.find('guid') else "N/A"
            parsed_item['published'] = element.find('pubDate').text

            parsed_content.append(parsed_item)

        return parsed_content
        title = root.find('title')


class PolsatNewsParser(AbstractNewsParser):

    def get_url(self):
        return 'https://www.polsatnews.pl/rss/polska.xml'

    def parse_content(self, raw_content):
        parsed_content = []

        root = ET.fromstring(raw_content)

        for element in root.iter('item'):

            parsed_item = {}

            parsed_item['title'] = element.find('title').text
            parsed_item['link'] = element.find('link').text
            parsed_item['content'] = html.unescape(
                element.find('description').text)
            parsed_item['id'] = 'N/A'
            parsed_item['published'] = 'N/A'

            parsed_content.append(parsed_item)

        return parsed_content


class NewsReader:

    def top_news(self, head_title, news_provider):
        print(head_title)
        news_provider.print_top_news()


if __name__ == '__main__':

    news_reader = NewsReader()

    bing = BingParser()
    news_reader.top_news('Bing: \n', bing)

    print('#'*40)

    news_reader.top_news('Yahoo: \n', YahooParser())
