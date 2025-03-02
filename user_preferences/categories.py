import heapq

def get_top_categories(n=3):
    # actual logic goes here. (implement user history DB, keys are categories.)
    # keys ideas: keywords from user history of article titles + metadata?

    # bag of words NLP approach?
    categories_vocab = {} # holds user history. {keyword: count}

    # simulate user clicking on new article categories and filling in dict with frequencies
    categories_vocab["SpaceX"] = 4
    categories_vocab["Trump"] = 3
    categories_vocab["NBA"] = 2
    categories_vocab["Drake"] = 1
    categories_vocab["Cooking"] = 1
    categories_vocab["Matcha"] = 1

    vocab_size = len(set(categories_vocab.keys()))
    neg_size = sum(categories_vocab.values())

    # placeholder logic (no nlp)
    heap = [(-count, category) for category, count in categories_vocab.items()]
    heapq.heapify(heap)

    top_categories = list(item for _, item in heap)

    # top_categories = ["SpaceX", "Trump", "NBA", "Drake", "Cooking", "Matcha"]
    return top_categories[:n]