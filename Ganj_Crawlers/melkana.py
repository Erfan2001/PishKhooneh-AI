import requests
import json
import time

jsonData = {"city": ["تهران"], "category": "فروش مسکونی",
        "sub_category": "آپارتمان", "source": ["6"]}
totalData=[]
for i in range(1,102):
    print('Request Number =>',str(i),'/','101')
    response=requests.post('https://api.ganje.ir/api/search_test/home/%s/'%str(i),json=jsonData)
    data=response.json().get('result')
    for item in data:
        title=item.get('title')
        identifier=item.get('token')
        category=item.get('category')
        sub_category=item.get('sub_category')
        city=item.get('city')
        province=item.get('province')
        neighborhood=item.get('neighbourhood')
        area=item.get('area')
        price=item.get('price')
        year=item.get('production')
        room=item.get('room')
        image=item.get('thumbnail')
        timex=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(item.get('time'))))
        totalData.append({'title':title,'identifier':identifier,'category':category,'sub_category':sub_category,
                          'city':city,'province':province,'neighborhood':neighborhood,'area':area,
                          'price':price,'year':year,'room':room,'image':image,'time':timex})

with open('melkana.json','w',encoding='utf-8') as f:
    f.write(json.dumps({'data':totalData},ensure_ascii=False,indent=4))