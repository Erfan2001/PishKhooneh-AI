import json
import pandas as pd
import numpy as np
import sqlite3,json as xx
import datetime
import sys
import traceback
from iteration_utilities import unique_everseen

with open('withoutTotal2.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
data=data.get('data')
with sqlite3.connect('Database/db.sqlite3') as connection:
    try:
            cur = connection.cursor()
            cur.execute(f'delete from estimate_home')
            cur.execute(f'delete from estimate_homes2')
            connection.commit();
            for index,item in enumerate(data):
                cur = connection.cursor()
                id1= item.get('identifier')
                title=item.get('title')
                date='2022-11-24T17:43:34.333+00:00'
                totalPrice=item.get('totalPrice')
                unitPrice=int(totalPrice//item.get('floorArea'))
                if item.get('unitPrice'):
                    unitPrice=item.get('unitPrice')
                province=item.get('bread_crumbs')[2]
                if item.get('location'):
                    address=item.get('location').get('locationName')
                locationX=item.get('location').get('longitude')
                locationY=item.get('location').get('latitude')
                if len(item.get('images')) <= 1:
                    if item.get('images')[0].get('photoSmallUrl')=="https://cdn.kilid.com/default-small.png":
                        main_image='https://foyr.com/learn/wp-content/uploads/2021/08/design-your-dream-home.jpg'
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
                category=item.get('type').get('propertyType').split('/')[0]
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
                source='کلید'
                isActive=True
                ownerId=''
                if item.get('contact'):
                    ownerId=item.get('contact').get('fullName')
                print('Number => ',data.index(item),' | Identifier:',id1)
                cur.execute(f'INSERT INTO estimate_homes2 VALUES ({index},"{title}",{totalPrice},{unitPrice},"{province}","{address}",{locationX},{locationY},"{main_image}","{image1}","{image2}","{image3}","{type1}","{category}","{status}","{seller}",{age},{floorArea},{numOfBeds},{parking},{lobby},{wareHouse},{sportHall},{guard},{elevator},{swimmingPool},{balcony},{roofGarden},{remoteDoor},"{description}",{region},"{neighbor}","{graph}","{phoneNumber}","{source}","{ownerId}","{date}","{date}",{isActive})')
                connection.commit()
    except sqlite3.Error as er:
        print('Total Error => ', er)