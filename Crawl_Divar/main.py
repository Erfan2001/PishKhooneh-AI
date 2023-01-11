import requests
from bs4 import BeautifulSoup
import re
headers2 = {
    "scheme": "https",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,fa;q=0.8",
    "country_id": "2",
    "locale": "FA",
    "organization": "1",
    "sec-ch-ua": '`"Google Chrome`";v=`"107`", `"Chromium`";v=`"107`", `"Not = A?Brand`";v=`"24`"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '`"Windows`"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
page = requests.get(
    'https://divar.ir/s/isfahan/buy-residential', headers=headers)
print('First Request =>', page)
if page.status_code!=200:
    print(page.text)
soup = BeautifulSoup(page.text, 'html.parser')
regex = re.compile('post-card-item*')
items = soup.find_all('div', {'class': regex})
for item in items:
    identifier = item.find('a').get('href').split('/')[-1]
    identifier='wYLeIkOM'
    data = requests.get('https://api.divar.ir/v8/posts-v2/web/%s' %
                        identifier, headers=headers)
    print('Second Request =>', data)
    print('Identifier =>', identifier)
    print('Image =>',(item for item in data.json().get('sections')if item["section_name"] == "IMAGE"))
    if len(list(item for item in data.json().get('sections')if item["section_name"] == "IMAGE")):
        images = (next(item for item in data.json().get('sections')
                if item["section_name"] == "IMAGE")).get('widgets')[0].get('data').get('items')

    title = (next(item for item in data.json().get('sections')
             if item["section_name"] == "TITLE")).get('widgets')[0].get('data').get('title')

    subTitle = (next(item for item in data.json().get(
        'sections') if item["section_name"] == "TITLE")).get('widgets')[0].get('data').get('subtitle')

    description = (next(item for item in (next(item for item in data.json().get(
        'sections') if item["section_name"] == "DESCRIPTION")).get('widgets') if item["widget_type"] == "DESCRIPTION_ROW")).get('data').get('text')
    if len(list(item for item in data.json().get('sections')if item["section_name"] == "TAGS")):
        tags = (next(item for item in data.json().get(
            'sections') if item["section_name"] == "TAGS")).get('widgets')[0].get('data').get('chip_list').get('chips')
    if len(list(item for item in data.json().get('sections')if item["section_name"] == "MAP")):
        maps = (next(item for item in data.json().get(
            'sections') if item["section_name"] == "MAP")).get('widgets')[0].get('data').get('location')
    kk = []
    res1 = (xx for xx in (next(item for item in data.json().get('sections') if item["section_name"] == "LIST_DATA")).get(
        'widgets') if xx["widget_type"] == "UNEXPANDABLE_ROW")
    for d in res1:
        kk.append((d.get('data').get('title'), d.get('data').get('value')))
    
    zz=[]
    res2 = (xx for xx in (next(item for item in data.json().get('sections') if item["section_name"] == "LIST_DATA")).get(
        'widgets') if xx["widget_type"] == "GROUP_FEATURE_ROW")
    if len(list(res2)):
        print(res2)
        for vv in res2:
            print(vv,'VVV')
        cc=(next(res2)).get('data').get('items')
    break
