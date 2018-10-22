import xml.etree.cElementTree as ET
import pprint
OSM ="/Users/liupengfei/Documents/GitHub/Wrangle_OpenStreetMap_Data/newyork_sample.osm"



def audit_problem_node_key(osm, key):
    osm_file = open(osm, "r")
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node":
            for tag in elem.iter('tag'):
                if tag.attrib['k'] == key:
                    print (elem.attrib['id'], elem.attrib['uid'], tag.attrib)
    osm_file.close()

def audit_problem_attr(osm, node_id):
    osm_file = open(osm, "r")
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag=="node":
            if elem.attrib['id'] == node_id:
                for tag in elem.iter('tag'):
                    print (tag.attrib)
    osm_file.close()


def get_unique_users(osm):
    users = set()
    for event, elem in ET.iterparse(osm):
        if elem.get("uid"):
            users.add(elem.attrib["uid"])
    return users


pprint.pprint(audit_problem_node_key(OSM, "FIXME"))
pprint.pprint(audit_problem_node_key(OSM, "fixme"))

pprint.pprint(audit_problem_attr(OSM, "419360276"))
