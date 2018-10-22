import xml.etree.cElementTree as ET
import re
import pprint
OSM_file ="/Users/liupengfei/Documents/GitHub/Wrangle_OpenStreetMap_Data/newyork_sample.osm"



def audit_tags(osm_file):
    osmfile = open(osm_file, 'r')
    node_keys = set()
    node_values = set()
    way_keys = set()
    way_values = set()
    for event, elem in ET.iterparse(osmfile, events=('start',)):
        if elem.tag == "node":
            for tag in elem.iter("tag"):
                node_keys.add(tag.attrib['k'])
                node_values.add(tag.attrib['v'])
        if elem.tag == "way":
            for tag in elem.iter("tag"):
                way_keys.add(tag.attrib['k'])
                way_values.add(tag.attrib['v'])
    osmfile.close()
    return node_keys, node_values, way_keys, way_values

# audit nodes and ways <k, v>
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]') 

def audit_type(tag_keys):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other":0}
    for key in tag_keys:
        if re.search(lower,key):
            keys['lower']+=1
        elif re.search(lower_colon,key):
            keys['lower_colon']+=1
        elif re.search(problemchars,key):
            keys['problemchars']+=1
        else:
            keys['other']+=1
    return keys


node_k_type, node_v_type, way_k_type, way_v_type = audit_tags(OSM_file)
node_k = audit_type(node_k_type)
node_v = audit_type(node_v_type)
way_k = audit_type(way_k_type)
way_v = audit_type(way_v_type)

print ("problems of k in nodes:")
pprint.pprint(node_k)
print ("problems of v in node:")
pprint.pprint(node_v)
print ("problems of k in ways:")
pprint.pprint(way_k)
print ("problems of v in ways:")
pprint.pprint(way_v)
