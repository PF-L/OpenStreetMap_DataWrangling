import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSM = "/Users/liupengfei/Documents/GitHub/Wrangle_OpenStreetMap_Data/newyork_sample.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Alley","Plaza","Commons","Broadway","Expressway","Terrace","Center","Circle",
            "Crescent","Highway","Way"]

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit(osm):
    osm_file = open(osm, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events =("start",)):
        if elem.tag == "way" or elem.tag=="node":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

st_types = audit(OSM)
pprint.pprint(dict(st_types))

mapping = { "AVENUE": "Avenue",
            "AVenue": "Avenue",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Avene": "Avenue",
            "Blvd": "Boulevard",
            "Ct": "Court",
            "DRIVE": "Drive",
            "Dr": "Drive",
            "Pkwy": "Parkway",
            "Plz": "Plaza",
            "ROAD": "Road",
            "Rd": "Road",
            "STREET": "Street",            
            "St": "Street",
            "St.": "Street",
            "Steet": "Street",
            "Trce": "Terrace",
            "Tpke": "Turnpike",
            "avenue": "Avenue",
            "street": "Street",
             "N": "North",
            "n" : "North",
            "S": "South",
            "s": "South",
            "W": "West",
            "w" : "West",
            "E": "East",
            "e" : "East"
            }
def update_streetname(street_name, mapping):
    m = street_type_re.search(street_name)
    better_name = street_name
    if m:
        if m.group() in mapping.keys():
            better_street_types = mapping[m.group()]
            better_name = street_type_re.sub(better_street_types, street_name)
    return better_name


for street_type, way in st_types.items():
    for name in way:
        better_names = update_streetname(name, mapping)
        print (name, "=>", better_names)
        
        
            
            
            
        
    
    
