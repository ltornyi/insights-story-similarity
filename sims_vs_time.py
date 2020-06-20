import similars
import csv
import datetime as dt
import pandas as pd

PUBLISHED_AT_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'

def human_readable(stories, tools):
    for i, sims in enumerate(tools['index']):
        for j, score in enumerate(sims):
            print('Story {}, id:{}, publishedAt:{} to Story {}, id:{}, publishedAt:{}, similarity: {}'.format(
                i, stories[i]['id'], stories[i]['publishedAt'],
                j, stories[j]['id'], stories[j]['publishedAt'],
                score
            ))

def get_story_data(story):
    return ( story['id'], dt.datetime.strptime(story['publishedAt'], PUBLISHED_AT_FORMAT) )

def row_for_story_pair(index1, index2, score, stories):
    id1, d1 = get_story_data(stories[index1])
    id2, d2 = get_story_data(stories[index2])
    day_diff = abs((d1-d2).days)
    return [index1, id1, index2, id2, score, day_diff]


def csv_export(stories, tools, writer):
    writer.writerow(['index1','id1','index2','id2','similarity','day_diff'])
    index = tools['index']
    for i, sims in enumerate(index):
        for j, score in enumerate(sims):
            writer.writerow(row_for_story_pair(i, j, score, stories))


def export_similarity():
    stories = similars.read_stories('stories.json')
    tools = similars.generate_tools(stories)
    # all-vs-all similarities
    with open('all-to-all.csv', 'w', newline='') as f:
        writer = csv.writer(f, dialect='excel-tab')
        csv_export(stories, tools, writer)


# Consider similarities above 0.15 only
df = pd.read_csv("all-to-all.csv", sep="\t")
similars_df = df[ (df['id1'] != df['id2']) & (df['similarity'] > 0.15)]

# Doesn't make too much sense
# similars_df['similarity'].corr(similars_df['day_diff'])

similars_sorted = similars_df.sort_values(by=['index1','similarity'],ascending=(True,False))

by_index1 = similars_sorted.groupby('index1')
top5 = by_index1.head(5)
top5[top5['day_diff'] > 100 ]

similars_sorted.to_csv('similars.csv', sep='\t', index=False)
top5.to_csv('similars_top5.csv', sep='\t', index=False)

# Not enough data
# by_index1[['similarity','day_diff']].corr()
