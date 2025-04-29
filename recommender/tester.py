from recommender import SearchBar, TinderInteraction
from sql.db import DBManager
from sql.constants import *
from rich.pretty import pprint
import random

if __name__ == "__main__":
    tinder = TinderInteraction()
    tinder.setup_article_stats_trigger()
    
    # # Test inserting a single interaction
    tinder.record_interaction(191, 'like')
    print(f"Recorded 'like' for article 1")
    
    # # Check the stats
    # stats = tinder.get_article_stats(1)
    # if stats:
    #     print(f"Article 1 stats: {stats['likes_count']} likes, {stats['dislikes_count']} dislikes")
    # else:
    #     print("No stats found for article 1")

	# tinder.setup_article_stats_trigger()

	# tinder.record_interaction(note_id=300, interaction_type="like")
	# interactions = tinder.get_user_interactions(user_id=1)
	# # pprint(interactions)

	# x = tinder.db_manager.get_tables()
	# for y in x:
	# 	if y in ["ArticleStats", "Interactions"]:
	# 		pprint(tinder.db_manager.get_columns(y))
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	


	############ RANDOM TESTING HERE DONT USE ###############
	
	# dbm = DBManager(host=HOST, database=DATBASE, user=USER, password=PASSWORD)
	# query = "SELECT * FROM articlesKeywords"
	# dbm.connect()

	# # Use fetch_all() instead of execute_query() for SELECT statements
	# results = dbm.fetch_all(query=query, params=None)
	# print(results)  # This will print the actual results

	# dbm.disconnect()
	# print(dbm.execute_query(query=query, params=None))

	# try:
	# 	print("Initializing TinderInteraction class...")
	# 	interaction = TinderInteraction()
	# 	interaction.setup_trigger(force=True)
	# except:
	# 	pass

	# dbm = DBManager(host=HOST, database=DATBASE, user=USER, password=PASSWORD)
	# query = "SELECT * FROM articlesKeywords"
	# dbm.execute_query(query=query, params=None)
        
    #     # Generate a test note ID
    #     test_note_id = random.randint(1000, 9999)
        
    #     # Record a 'like' interaction
    #     print(f"\nRecording 'like' for note {test_note_id}")
    #     interaction.record_interaction(test_note_id, "like")
        
        # # Get the interaction we just created
        # query = "SELECT * FROM Interactions WHERE noteId = %s AND interactionType = 'like'"
        # result = interaction.db_manager.fetch_one(query, (test_note_id,))
        
        # if result:
        #     pprint(result)
        #     print(f"Success! Found interaction with ID: {result['interactionId']}")
        #     print(f"Interaction duration: {result['interactionDuration']}")
            
        #     # Now test an update by recording the same interaction again
        #     print("\nRecording the same interaction again to test update functionality...")
        #     interaction.record_interaction(test_note_id, "like")
            
        #     # Get the interaction again to see if it was updated
        #     updated_result = interaction.db_manager.fetch_one(query, (test_note_id,))
            
        #     if updated_result:
        #         print(f"Updated interaction: {updated_result['interactionId']}")
        #         print(f"Updated timestamp: {updated_result['timestamp']}")
        #         print(f"Duration still: {updated_result['interactionDuration']}")
                
        #         # Check if ID stayed the same (should be the same since trigger updates instead of inserts)
        #         if result['interactionId'] == updated_result['interactionId']:
        #             print("\nSUCCESS: Trigger is working correctly! It updated the existing record.")
        #         else:
        #             print("\nFAIL: Trigger did not update correctly. A new record was created.")
        #     else:
        #         print("Failed to find the updated interaction")
        # else:
        #     print("Failed to find the initial interaction")
        
        # # Test different interaction type
        # print("\nTesting a different interaction type ('dislike') for the same note...")
        # interaction.record_interaction(test_note_id, "dislike")
        
        # # Get both interactions for this note
        # query = "SELECT * FROM Interactions WHERE noteId = %s ORDER BY interactionType"
        # results = interaction.db_manager.fetch_all(query, (test_note_id,))
        # print(f"Found {len(results)} interactions for note {test_note_id}")
        
        # # Display all interactions for this test note
        # for i, interaction_record in enumerate(results):
        #     print(f"\nInteraction {i+1}:")
        #     for key, value in interaction_record.items():
        #         print(f"  {key}: {value}")
        
        # # Get all interactions for user 1
        # print("\nGetting all interactions for user 1...")
        # all_interactions = interaction.get_user_interactions()
        # print(f"Found {len(all_interactions)} total interactions for user 1")
        
    # except Exception as e:
    #     print(f"Error occurred: {str(e)}")

	# search = SearchBar2()
	# articles_list = search.search_articles(key_phrase="Ukraine", top_n=3)
	# pprint(articles_list)
	# x = search.search_articles(key_phrase="Ukraine")
	# pprint(x)

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
	
