import requests
import json
import time
import sqlite3
import random
requests.adapters.DEFAULT_RETRIES = 5
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
def crawler():
    lastItem="0"
    while 1:
        for epoch in range(0,1):
            print('-------------- Epoch %s Started --------------'%str(epoch+1))
            url = 'https://server.kilid.com/listing_api/v1.0/listing/search?page=%s&sort=DATE_DESC&lang=fa'%str(epoch)
            response = requests.post(url, json=payloads, headers=headers, timeout=(2, 5))
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
                time.sleep(1)
                print('singleResponse',singleResponse)
                print('contactResponse',contactResponse)
                print('graphResponse',graphResponse)
                singleData = singleResponse.json()
                newRecord['identifier'] = item.get('identifier')
                newRecord['title'] = item.get('title')
                newRecord['date'] = item.get('searchDate')
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
                if contactResponse.status_code!=200:
                    newRecord['contact']=None
                else:
                    newRecord['contact'] = contactResponse.json()
                if graphResponse.status_code!=200:
                    newRecord['graph']=None
                else:
                    newRecord['graph'] = graphResponse.json()
                totalData.append(newRecord)
        print(' --- Finished Successfully --- ')
        haveTotalPrice=[]
        for item in totalData:
            if item.get('totalPrice'):
                haveTotalPrice.append(item)
        haveTotalPrice.reverse()
        currentIndex=0
        if lastItem != "0":
            for item in haveTotalPrice:
                if str(item.get('identifier'))==lastItem:
                    currentIndex=haveTotalPrice.index(item)
        lastItem=str(haveTotalPrice[-1].get('identifier'))
        if currentIndex != len(haveTotalPrice)-1:
            newData=haveTotalPrice[currentIndex:]
        else:
            newData=[]
        data=[]
        for item in newData:
            if item.get('identifier') in [x.get('identifier') for x in data]:
                continue
            else:
                data.append(item)
        totalData.clear()
        haveTotalPrice.clear()
        newData.clear()
        print(currentIndex,'currentIndex',lastItem)
        # with sqlite3.connect('Pishkhooneh_Bot/db.sqlite3') as connection:
        #         try:
        #             cur = connection.cursor()
        #             rows = cur.fetchall()
        #         except sqlite3.Error as er:
        #             print('Total Error => ', er)
        print('------------------ Length of total data for process in SQLITE : %s ------------------'%len(data))
        if len(data):
            with sqlite3.connect('db.sqlite3') as connection:
                try:

                        for item in data:
                            cur = connection.cursor()
                            id1= item.get('identifier')
                            title=item.get('title')
                            date=item.get('date')
                            totalPrice=item.get('totalPrice')
                            unitPrice=int(totalPrice//item.get('floorArea'))
                            if item.get('unitPrice'):
                                unitPrice=item.get('unitPrice')
                            province=item.get('bread_crumbs')[2]
                            if item.get('location'):
                                address=item.get('location').get('locationName')
                                print(address)
                            locationX=item.get('location').get('longitude')
                            locationY=item.get('location').get('latitude')
                            if len(item.get('images')) <= 1:
                                if item.get('images')[0].get('photoSmallUrl')=="https://cdn.kilid.com/default-small.png":
                                    main_image='https://www.simplilearn.com/ice9/free_resources_article_thumb/what_is_image_Processing.jpg'
                                else:
                                    main_image=item.get('images')[0].get('photoLargeUrl')
                                image1=''
                                image2=''
                                image3=''
                            else:
                                if len(item.get('images')) == 2:
                                    main_image=item.get('images')[0].get('photoLargeUrl')
                                    image1=item.get('images')[1].get('photoLargeUrl')
                                    image2=''
                                    image3=''
                                elif len(item.get('images')) == 3:
                                    main_image=item.get('images')[0].get('photoLargeUrl')
                                    image1=item.get('images')[1].get('photoLargeUrl')
                                    image2=item.get('images')[2].get('photoLargeUrl')
                                    image3=''
                                else:
                                    main_image=item.get('images')[0].get('photoLargeUrl')
                                    image1=item.get('images')[1].get('photoLargeUrl')
                                    image2=item.get('images')[2].get('photoLargeUrl')
                                    image3=item.get('images')[3].get('photoLargeUrl')
                            type1=item.get('type').get('landuseType')
                            category=item.get('type').get('propertyType')
                            status='فروشی'
                            seller='شخصی'
                            if item.get('contact'):
                                if item.get('contact').get('type')=='AGENT':
                                    seller='شخصی'
                                elif item.get('contact').get('type')=='AGENCY':
                                    seller='املاک'
                            age=0
                            if item.get('age'):
                                age=item.get('age')
                            floorArea=item.get('floorArea')
                            numOfBeds=1
                            if item.get('numOfBeds'):
                                numOfBeds=item.get('numOfBeds')
                            parking=item.get('features').get('parking')
                            lobby=item.get('features').get('lobby')
                            wareHouse=item.get('features').get('warehouse')
                            sportHall=item.get('features').get('sports_hall')
                            guard=item.get('features').get('guard')
                            elevator=item.get('features').get('elevator')
                            swimmingPool=item.get('features').get('swimming_pool')
                            balcony=item.get('features').get('balcony')
                            roofGarden=item.get('features').get('roof_garden')
                            remoteDoor=item.get('features').get('sports_hall')
                            description=item.get("description")
                            description=description.replace('\"','')
                            region=int(item.get('bread_crumbs')[3].split(' ')[1])
                            neighbor=item.get('bread_crumbs')[4]
                            graph=item.get('graph')
                            phoneNumber='09999999999'
                            if item.get('contact'):
                                phoneNumber=item.get('contact').get('callNumber')
                            isActive=True
                            owner=''
                            if item.get('contact'):
                                owner=item.get('contact').get('fullName')
                            print('Number => ',data.index(item),' | Identifier:',id1)
                            cur.execute(f'INSERT INTO estimate_homes2 VALUES ({id1},"{title}",{totalPrice},{unitPrice},"{province}","{address}",{locationX},{locationY},"{main_image}","{image1}","{image2}","{image3}","{type1}","{category}","{status}","{seller}",{age},{floorArea},{numOfBeds},{parking},{lobby},{wareHouse},{sportHall},{guard},{elevator},{swimmingPool},{balcony},{roofGarden},{remoteDoor},"{description}",{region},"{neighbor}","{str(graph)}","{phoneNumber}","کلید","{owner}","{date}","{date}",{isActive})')
                            connection.commit()
                except sqlite3.Error as er:
                    print('Total Error => ', er)
        data.clear()
        print('--------  Finished SQLITE Process   ---------')
        randomNumber=random.randint(50, 60)
        time.sleep(randomNumber)
        print('----------- Finish Sleep Time : %s  ---------------'%randomNumber)
# crawler()

