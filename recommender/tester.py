# import sys
# print(sys.path)

from recommender import SearchBar
from sql.db import DBManager
from sql.constants import *
from rich.pretty import pprint

if __name__ == "__main__":
	search = SearchBar()
	pprint(search.find_articles(key_phrase="Ukraine"))
