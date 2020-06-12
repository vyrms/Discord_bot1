# for searching in wiki API


import requests
import re


# command format = .wikisuggest n 言葉
def wiki_suggest(command=""):
    try:
        # tidy the command
        command = command.strip(".wikisuggest ").split(" ", maxsplit=1)
        # set word to search for
        searchpage = command[1]
        # set hwo many suggestions to get
        srlimit = command[0]

        # access the wiki API and get the "query" section of their response
        query = wiki_query(searchpage, srlimit)

        # get list of suggestions
        suggestions = ",\t".join([word['title'] for word in query['search']])
        # get the total hits on wiki
        totalhits = query['searchinfo']['totalhits']

        # see which is smaller. total or srlimit
        smaller = min(int(totalhits), int(srlimit))

        output = f"Wikipediaには{totalhits}件の{searchpage}のページがあったよ！\n" \
                 f"{smaller}件だけ見せてあげるね！\n" \
                 f"{suggestions}"
        return output

    except:
        return "エラーだよ！入力ミスかも？\n" \
               "↓こうやって入力してね！\n" \
               ".wikisuggest 10 言葉"


# command format = .wikisearch 言葉
def wiki_search(command=""):
    try:
        # tidy the command
        command = command.strip(".wikisearch ").split(" ", maxsplit=1)
        # set word to search for
        searchpage = command[0]
        # only get 1 result
        srlimit = "1"

        # access the wiki API and get the "query" section of their response
        query = wiki_query(searchpage, srlimit)

        # get the title of article
        title = query['search'][0]['title']
        # get a summary of the article, and clean up the html tags
        snippet = query['search'][0]['snippet']
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', snippet)
        cleantext = cleantext.replace("&quot;", "\"")

        output = f"{title}とは！！\n" \
                 f"{cleantext}"
        return output

    except:
        return "エラーだよ！入力ミスかも？\n" \
               "↓こんな感じで入力してね！\n" \
               ".wikisearch 言葉"


# a helper function
# performs the actual querying to API, returns the "query" part of response
def wiki_query(searchpage="", srlimit="10"):
    # url of wikipedia API
    url = "https://ja.wikipedia.org/w/api.php"
    # set query parameters
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": searchpage,
        "srlimit": srlimit,
        "srsort": "just_match"
    }

    # send request to API
    response = requests.get(url, params)

    # get just the query part of response
    query = response.json()['query']
    return query
