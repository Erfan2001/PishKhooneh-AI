import requests
import json
response=requests.get('https://api.ganje.ir/api/gis/neighbourhood/292')
with open('neighbors.json','w',encoding='utf-8') as f:
    f.write(json.dumps(response.json(),ensure_ascii=False,indent=4))