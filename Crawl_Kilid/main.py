import requests
import json
headers = {
    "authority": "server.kilid.com",
    "method": "POST",
    "path": "/glisting_api/v1.0/gListing/search?page=1&sort=DATE_DESC&lang=fa",
    "scheme": "https",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,fa;q=0.8",
    "country_id": "2",
    "locale": "FA",
    "organization": "1",
    "origin": "https://kilid.com",
    "referer": "https://kilid.com/",
    "sec-ch-ua": '`"Google Chrome`";v=`"107`", `"Chromium`";v=`"107`", `"Not = A?Brand`";v=`"24`"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '`"Windows`"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
}
payloads = {"action": "listingSearch", "content": {"listingTypeId": 1, "landUseTypeIds": None, "propertyTypeIds": None, "location": [
    272905], "similarLocation": None, "attributeFilters": {}, "propertyFeatureIds": None, "propertyTagIds": None, "geographicPolygon": None, "fromLegacyService": True}}
features = {
    'پارکینگ': 'parking',
    'لابی': 'lobby',
    'انباری': 'warehouse',
    'سالن ورزش': 'sports_hall',
    'نگهبان': 'guard',
    'آسانسور': 'elevator',
    'بالکن': 'balcony',
    'استخر': 'swimming_pool',
    'سونا': 'sauna',
    'تهویه مطبوع': 'air_conditioning',
    'سالن اجتماعات': 'conference_hall',
    'روف گاردن': 'roof_garden',
    'درب ریموت': 'remote_door',
    'جکوزی': 'jacuzzi',
    'آنتن مرکزی': 'central_antenna',
}
epochs=100
for epoch in range(97,epochs):
    print('-------------- Epoch %s Started --------------'%str(epoch+1))
    url = 'https://server.kilid.com/listing_api/v1.0/listing/search?page=%s&sort=DATE_DESC&lang=fa'%str(epoch)
    response = requests.post(url, json=payloads, headers=headers)
    content = response.json().get('content')
    totalData = []
    for item in content:
        print(item.get('identifier'))
        print('-------------- Epoch %s: Item Number %s/%s Started --------------'%(str(epoch+1),str(content.index(item)+1),str(len(content))))
        newRecord = {}
        singleURL = 'https://server.kilid.com/listing_api/v1.0/gListing/single?sourceId=0&Identifier=%s&lang=fa' % item.get(
            'identifier')
        contactURL = 'https://server.kilid.com/listing_api/v1.0/gListing/contactInfo?Identifier=%s&mode=FULL_VIEW' % item.get(
            'identifier')
        graphURL = 'https://server.kilid.com/insight_global_api/trends/v1.0?globalLocationId=246690&durationMonths=12&mode=RAW&trendTypeIdentifier=3'
        try:
            singleResponse = requests.get(singleURL, headers=headers)
        except:
            print('Error')
        print('-------------- Epoch %s: Item Number %s/%s : Single Request --------------'%(str(epoch+1),str(content.index(item)+1),str(len(content))))
        try:
            contactResponse = requests.get(contactURL, headers=headers)
        except:
            print('Error')
        print('-------------- Epoch %s: Item Number %s/%s : Contact Request --------------'%(str(epoch+1),str(content.index(item)+1),str(len(content))))
        try:
            graphResponse = requests.get(graphURL, headers=headers)
        except:
            print('Error')
        print('-------------- Epoch %s: Item Number %s/%s : Graph Request --------------'%(str(epoch+1),str(content.index(item)+1),str(len(content))))
        singleData = singleResponse.json()
        newRecord['identifier'] = item.get('identifier')
        newRecord['title'] = item.get('title')
        newRecord['totalPrice'] = item.get('pricing').get('price')
        newRecord['unitPrice'] = item.get('pricing').get('unitPrice')
        newRecord['location'] = singleData.get('location')
        images = []
        if len(singleData.get('media')):
            for image in singleData.get('media'):
                images.append({'photoSmallUrl': image.get('photoSmallUrl'),
                            'photoLargeUrl': image.get('photoLargeUrl')})
        newRecord['images'] = images.copy()
        newRecord['type'] = {
            'landuseType': singleData.get('attributes').get('landuseType'),
            'propertyType': singleData.get('attributes').get('propertyType')
        }
        newRecord['age'] = singleData.get('attributes').get('age')
        newRecord['floorArea'] = item.get('attributes').get('floorArea')
        newRecord['floorAreaUnit'] = item.get('attributes').get('floorAreaUnit')
        newRecord['numOfBeds'] = item.get('attributes').get('numOfBeds')
        newRecord['numberOfParking'] = item.get(
            'attributes').get('numberOfParking')
        singleFeatures = {}
        for eachItem in features.items():
            singleFeatures[eachItem[1]] = False
        if len(singleData.get('attributes').get('specifics')):
            for feature in singleData.get('attributes').get('specifics'):
                singleFeatures[features.get(feature.get('type'))] = True
        newRecord['features'] = singleFeatures.copy()
        newRecord['description'] = singleData.get('description')
        newRecord['seoDescription'] = singleData.get('seoDescription')
        breadCrumbs = []
        if len(singleData.get('breadcrumbLinks')):
            for breadCrumb in singleData.get('breadcrumbLinks'):
                breadCrumbs.append(breadCrumb.get('name'))
        newRecord['bread_crumbs'] = breadCrumbs.copy()
        if contactResponse.status_code==400:
            newRecord['contact']=None
        else:
            newRecord['contact'] = contactResponse.json()
        newRecord['graph'] = graphResponse.json()
        totalData.append(newRecord)
    with open("data/houses_%s.json"%str(epoch), "w", encoding='utf-8') as outfile:
        outfile.write(json.dumps({'data': totalData},indent=4, ensure_ascii=False))
print(' --- Finished Successfully --- ')
