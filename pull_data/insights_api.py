import requests

baseURL = 'https://storytelling.blackrock.com/insights/api/stories/'

def getAllPages(cnt):
    pages = []
    for i in range(1, cnt+1):
        params = {'page': i}
        resp = requests.get(baseURL, params=params)
        pages.append(resp.json())
    return pages

def getAllStories(pages):
    return [story for page in pages for story in page['results']]

if __name__ == "__main__":
    pass