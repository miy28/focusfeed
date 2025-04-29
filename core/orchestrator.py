import random
import time
import sys
import pyfiglet
from pyfiglet import Figlet
import pymysql


from api.nytimes_api import fetch_nytimes_articles
from recommender.categories import get_top_categories
# from sql.db import new_interaction, create_table
from llm.gemini import gemini

# bag of words NLP approach?
categories_vocab = {} # holds user history. {keyword: count}

def fetch_articles():
    categories = get_top_categories(5, categories_vocab)
    feed = []

    for i, category in enumerate(categories): # fancy stuff :3
        sys.stdout.write(f'\nFetching articles from category "{category}"...\n')
        sys.stdout.write('\033[F\033[F') # ANSI (move cursor up twice)
        draw_bar(i+1, len(categories))
        # draw_fetch()
        # sys.stdout.write('\n')
        sys.stdout.flush()

        nytimes_notes = fetch_nytimes_articles(category) # list of notes
        # add the other apis here once they're implemented

        print("\n\n\nGot", len(nytimes_notes), "articles per call to nytimes.search")

        if nytimes_notes:
            note = random.choice(nytimes_notes) # pick one to display to the feedv 
            summary = gemini(note.desc)

            keyword_values = []
            for keyword in note.keywords:
                print(keyword['value'])
                keyword_values.append(keyword["value"])
            
            print(len(keyword_values))

            feed.append(f'Article: "{note.title}".') # display a few random articles from user's top k categories
            feed.append(f'Summary: {summary}') # gemini summary
            # new_interaction(note) # send this to the db (simulate an interaction)
        else:
            feed.append(f'Could not find articles about "{category}". Sorry about that!')

    print("[bold purple]\n\n\nHere is your starter NewsFeed![/bold purple]")

    return feed

def draw_bar(iteration, total, category="category", bar_length=50):
    total = max(total, 1)
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(bar_length * iteration // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rProgress: |{bar}| {percent}% complete.')
    sys.stdout.flush()

def draw_fetch():
    sys.stdout.write(f'\nFetching articles from category "{category}".\n')
    sys.stdout.flush()

if __name__ == "__main__":
    from rich import print
    from rich.pretty import pprint

    # create_table()

    # ascii_banner = pyfiglet.figlet_format("FocusFeed")
    # printf(ascii_banner)
    print(r""""[red]
            .,-:;//;:=,
          . :H@@@MM@M#H/.,+%;,
       ,/X+ +M@@M@MM%=,-%HMMM@X/,
     -+@MM; $M@@MH+-,;XMMMM@MMMM@+-
    ;@M@@M- XM@X;. -+XXXXXHHH@M@M#@/.
  ,%MM@@MH ,@%=             .---=-=:=,.
  =@#@@@MX.,                -%HX$$%%%:;
 =-./@M@M$                   .;@MMMM@MM:
 X@/ -$MM/                    . +MM@@@M$
,@M@H: :@:         FF         . =X#@@@@-
,@@@MMX, .                    /H- ;@M@M=
.H@@@@M@+,                    %MM+..%#$.
 /MMMM@MMH/.                  XM@MH; =;
  /%+%$XHH@$=              , .H@@@@MX,
   .=--------.           -%H.,@@@@@MX,
   .%MM@@@HHHXX$$$%+- .:$MMX =M@@MM%.
     =XMMM@MM@MM#H;,-+HMM@M+ /MMMX=
       =%@M@M#@$-.=$@MM@@@M; %M%=
         ,:+$+-,/H#MMMMMMM@= =,
               =++%%%%+/:-.
    [/red]""")

    print("[bold cyan]Welcome to FocusFeed homepage.[/bold cyan]")
    print("[bold cyan] To get things started, what are some of your favorite topics?\n Please give at least one string to get things started.[/bold cyan]")
    print("[bold cyan]Keep in mind, some topics may not yield any articles if they are not relevant enough.[/bold cyan]")

    init_categories = []
    while True:
        category = input()
        if category:
            init_categories.append(category)
        else:
            break
    
    for category in init_categories:
        if category in categories_vocab:
            categories_vocab[category] += 1
        categories_vocab[category] = 1
    
    pprint(fetch_articles())