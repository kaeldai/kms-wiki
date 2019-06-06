from html.parser import HTMLParser
import pprint
import datetime
import json


class BookMarkParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super(BookMarkParser, self).__init__(*args, **kwargs)
        self._header = 'Start'
        self._link = None
        self.bookmarks = []
        self._datetime = datetime.datetime.now()
        self._datetime_fmt = self._datetime.strftime('%Y%m%d%I%M%S000')
        self._create_date = self._datetime.strftime('%Y-%m-%d')
        self._categoryLU = {
            'Books': 'Book',
            'Courses': 'Course',
            'Papers': 'Paper',
            'Articles': 'Article',
            'Tutorials and Practice Sets': 'Tutorial'
        }

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr_name, attr_val in attrs:
                if attr_name == 'href':
                    self._link = attr_val

    def handle_data(self, data):
        self._data = data

    def handle_endtag(self, tag):
        if tag == 'h3':
            self._header = self._data
        elif tag == 'a':
            category = self._header
            if category in ['saved', 'KEEPING']:
                return
            elif category == 'references':
                tiddler = self._create_reference()
            else:
                tiddler = self._create_reading()

            self.bookmarks.append(tiddler)

    def _create_reading(self):
        title = self._data
        url = self._link
        category = self._categoryLU.get(self._header, 'Article')
        if 'youtube' in url:
            category = 'Video'

        return {
            "text": "''description'': {{!!desc}} <br>\n''status:'' <<StatusDropDown>> <br> \n''level-of-effort:'' <<LOEDropDown>> <br>\n",
            "tags": "Task [[Reading Task]]",
            "desc": self._link,
            "creation-date": self._create_date,
            "status": "Unprocessed",
            "LOE": "-1",
            "task-type":self._header,
            "setting": "",
            "title": title,
            "created": self._datetime_fmt,
            "modified": self._datetime_fmt
        }

    def _create_reference(self):
        title = self._data
        url = self._link
        return {
            "text": "''link'': {{!!desc}} <br>\n'",
            "tags": "Reference",
            "desc": self._link,
            "creation-date": self._create_date,
            "title": title,
            "created": self._datetime_fmt,
            "modified": self._datetime_fmt
        }


parser = BookMarkParser()
parser.feed(open('bookmarks/bookmarks.html', 'r').read())
# print(parser.dl_stack)
#pprint.pprint(parser._root)
#pprint.pprint(parser.bookmarks)
json.dump(parser.bookmarks, open('bookmarks.json', 'w'), indent=4)
