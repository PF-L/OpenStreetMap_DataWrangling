import xml.etree.ElementTree as ET
import pprint

OSM ="/Users/liupengfei/Documents/GitHub/Wrangle_OpenStreetMap_Data/newyork_sample.osm"


def get_users(element):
    uid = " "
    if element.tag == "node" or element.tag == "way" or element.tag == "relation":
        uid = element.get('uid')
        return uid


def process(file):
    users = set()
    for _, elem in ET.iterparse(file):
        if get_users(elem):
            users.add(get_users(elem))
    return users


user = process(OSM)
pprint.pprint(user)
    
        
    
