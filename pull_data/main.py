import insights_api
from cardParser import CardParser
import json


pages = insights_api.getAllPages(4)
stories = insights_api.getAllStories(pages)
# ['id', 'title', 'topLine', 'cardCount', 'cards', 'themes', 'assetClasses', 'opub', 'publishedAt']
# cardTypes: body, quote, stat, chart, bottom_line
#   body, stat, quote, bottom_line: inside <p>
#   chart: inside <main>
cardParser = CardParser()
stories_text = []
for story in stories:
    story_text = {'title': story['title'], 'topLine': story['topLine'], 'id': story['id'], 'publishedAt': story['publishedAt']}
    cardParser.clear()
    for card in story['cards']:
        if card['cardType'] in ['body', 'quote', 'stat', 'bottom_line']:
            cardParser.feed(card['html'])
    story_text['text'] = cardParser.text
    stories_text.append(story_text)


with open('stories.json', 'w') as out:
    json.dump(stories_text, out)
        