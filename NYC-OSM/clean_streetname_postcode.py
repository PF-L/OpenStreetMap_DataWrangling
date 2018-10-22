import xml.etree.cElementTree as ET
import re

OSM = "/Users/liupengfei/Documents/GitHub/Wrangle_OpenStreetMap_Data/newyork_sample.osm"
NEW = "/Users/liupengfei/Downloads/sample.osm"

street_number_re = re.compile(r'((1\s*st)|(2\s*nd)|(3\s*rd)|([0,4,5,6,7,8,9]\s*th))$')

direction_re = re.compile(r'(\s(S|N|W|E)$)')
direction_mapping = {
                 " S" : "South",
                 " N" : "North",
                 " W" : "West",
                 " E" : "East"}

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Alley","Plaza","Commons","Broadway","Expressway","Terrace","Center","Circle",
            "Crescent","Highway","Way"]
street_mapping = { 
                  "Ave":"Avenue",
                  "Ave.":"Avenue",
                  "Avene":"Avenue",
                  "Aveneu":"Avenue",
                  "ave":"Avenue",
                  "avenue":"Avenue",
                  "Blv.":"Boulevard",
                  "Blvd":"Boulevard",
                  "blvd":"Boulevard",
                  "Broadway.":"Broadway",
                  "Ctr":"Center",
                  "Pkwy":"Parkway",
                  "Plz":"Plaza",
                  "Rd":"Road",
                  "ST":"Street",
                  "St":"Street",
                  "St.":"Street",
                  "Steet":"Street",
                  "Streeet":"Street",
                  "st":"Street",
                  "street":"Street"
                  }
def get_element(osm_file, tags=('node', 'way', 'relation')):
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def update_name(name):
    m1 = street_number_re.search(name)
    m2 = direction_re.search(name)
    m3 = street_type_re.search(name)

    if m1 and ('street' not in name and 'Street' not in name):
        street_number = m1.group()
        start = m1.start()
        end = start + len(street_number)
        name = name[: end] + ' Street'
        return name
    elif m2:
        direction = m2.group()
        name = name[:-2] + direction_mapping[direction]
        return name
    elif m3:
        street_type = m3.group()
        if street_type in street_mapping:
            start = m3.start()
            name = name[:start] + street_mapping[street_type]
            return name
    else:
        return name

def is_postcode(elem):
    return(elem.attrib['k'] == "addr:postcode" or elem.attrib['k'] == "postal_code")

def update_postcode(postcode):
    if re.findall(r'^\d{5}$', postcode):
        new_postcode = postcode
        return new_postcode
    elif re.findall(r'(^\d{5})-\d{4}$', postcode):
        new_postcode = re.findall(r'(^\d{5})-\d{4}$', postcode)[0]
        return new_postcode
    elif re.findall(r'NY\s*\d{5}', postcode):
        new_postcode = re.findall(r'\d{5}', postcode)[0]
        return new_postcode
    else:
        return None


def clean_streetname_postcode(osm, new):
    with open(osm, "r") as inputfile, open (new, "w") as outputfile:
        outputfile.write('<?xml version="1.0"encoding="utf-8"?>\n')
        outputfile.write('<osm>\n  ')
        for elem in get_element(inputfile):
            if elem.tag == "node" or elem.tag == "way":
                if elem.find("tag") != -1:
                    for tag in elem.iter("tag"):
                        if is_street_name(tag):
                            street_name = tag.attrib['v']
                            street_name = update_name(street_name)
                            tag.attrib['v'] = street_name
                        elif is_postcode(tag):
                            ny_postcode = tag.attrib['v']
                            if update_postcode(ny_postcode) == None:
                                elem.remove(tag)
                            else:
                                ny_postcode = update_postcode(ny_postcode)
                                tag.attrib['v'] = ny_postcode
        outputfile.write(ET.tostring(elem).decode("utf-8"))
        outputfile.write('</osm>')
    
clean_streetname_postcode(OSM, NEW)      
