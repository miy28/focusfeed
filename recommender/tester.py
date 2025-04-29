from recommender import SearchBar
from sql.db import DBManager
from sql.constants import *
from rich.pretty import pprint

if __name__ == "__main__":
	search = SearchBar(phrase="Ukraine")
	x = search.find_articles()
	print(x)

	# x = search.get_articleIds()
	# pprint(x[0])
	# y = search.get_keywords()
	# pprint(y[0])

	# ids_1 = set()
	# ids_2 = set()

	# # Collect keywordIds from y into ids_1
	# for item in y:
	# 	ids_1.add(item['keywordId'])
	# # Collect keywordIds from x into ids_2
	# for item in x:
	# 	ids_2.add(item['keywordId'])

	# # # Find matching IDs (intersection of sets)
	# # matching_ids = ids_1.intersection(ids_2)
	# matching_ids = ids_1.intersection(ids_2)


	# check = ['617', '1410', '2061', '1667', '609']
	# for a in check:
	# 	print(a in matching_ids)

	# # Print the result
	# # print("Matching keywordIds:", matching_ids)
	# print("Total matches found:", len(matching_ids))
	
