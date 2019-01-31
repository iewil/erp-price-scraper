import requests
from bs4 import BeautifulSoup
import json
from dateutil.parser import parse
from dateutil.tz import gettz

# Setting variables
url = "https://www.mytransport.sg/content/mytransport/home/myconcierge/erprates.html"

# Helper functions
def parseGantry(item):
    [ id, zone_id, road_name, road_type, area_name, lat, lon, last_updated ] = item.split(',')
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(lat), float(lon)]
        },
        "properties": {
            "id": int(id),
            "zone_id": zone_id,
            'road_name': road_name,
            'road_type': road_type,
            'area_name': area_name,   
            'last_updated': last_updated         
        }
    }

def parseErpRates(item):
    time = item.select('.erp_result_ti')[0].get_text()
    price = item.select('.erp_result_pr')[0].get_text()
    [start_date, end_date] = time.split(' - ')
    tzinfos = { "CST" : gettz("Asia/Singapore")}
    return {
        "start_date": parse(start_date, tzinfos=tzinfos).strftime('%H:%M'),
        "end_date": parse(end_date, tzinfos=tzinfos).strftime('%H:%M'),
        "price": float(price[1:]),
    }

def getRates(id, zone_id, vcc_type, day_type):
    print 'getting rates for: id:' + str(id) + '; zone_id: ' + zone_id + '; vcc_type: ' + str(vcc_type) + '; day_type: ' + str(day_type) 
    rates_url = "https://www.mytransport.sg/content/mytransport/home/myconcierge/erprates/jcr:content/par/erprates.rates?id=" + str(id) + "&zoneId=" + zone_id + "&vccType=" + str(vcc_type) + "&dayType=" + str(day_type)
    r = requests.get(rates_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    items = soup.select('.erp_result_cont')
    parsed_rates = map(parseErpRates, items)
    return parsed_rates

def saveGantryFile(data):
    with open('data/'+ str(data['properties']['id']) + '.json', 'w') as outfile:
        json.dump(data, outfile,
            indent=4, separators=(',', ': '))

# Main function
def start():
    print 'starting scraper...'
    print 'url: ' + url
    r = requests.get(url)

    r.raise_for_status()

    soup = BeautifulSoup(r.content, 'html.parser')

    # Getting list of gantries
    gantry_data = map(parseGantry, soup.select("#erp_list")[0].attrs['value'].split(';'))
    print 'number of gantries found: ' + str(len(gantry_data))

    # Getting list of vehicle types

    # == Vehicle types available
    # 1: Passenger Cars/Light Goods Vehicles/Taxis
    # 2: Motorcycles
    # 3: Heavy Goods Vehicles/Small Buses
    # 4: Very Heavy Goods Vehicles/Big Buses

    # == Day types available
    # 0: Weekdays
    # 1: Saturday

    vehicle_types = soup.select("#erp_vcc_day option")
    vehicle_data = []
    for vehicle_type in vehicle_types:
        if (vehicle_type.attrs['value'] != '0'):
            s = vehicle_type.get_text()
            item = {
                'vehicle': s[:s.find("(")-1],
                'vcc_type': int(vehicle_type.attrs['value'][0]),
                'day_type': int(vehicle_type.attrs['value'][1]),
            }
            vehicle_data.append(item)
    print 'number of vehicle types: ' + str(len(vehicle_data))

    print 'begin retrieving rates for all gantries and vehicle types'

    output_data = {
        "type": "FeatureCollection",
        "features": []
    }

    for i in gantry_data:
        gantry_rates = []
        for j in vehicle_data:
            vehicle_rates = getRates(i['properties']['id'], i['properties']['zone_id'], j['vcc_type'], j['day_type'])
            j['rates'] = vehicle_rates
            gantry_rates.append(j)
        i['properties']['rates'] = gantry_rates
        output_data['features'].append(i)
        # saveGantryFile(i)
    with open('data/erp_rates.json', 'w') as outfile:
        json.dump(output_data, outfile,
            indent=4, separators=(',', ': '))
    print 'complete...'

start()