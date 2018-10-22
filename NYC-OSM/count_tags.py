OSM = "/Users/liupengfei/Downloads/OSM/newyork_sample.osm"

import xml.etree.ElementTree as ET
import pprint
import re




def count_tags (file_name):
    tags = {}
    for event, elem in ET.iterparse(file_name):
        if elem.tag not in tags:
            tags[elem.tag]=1
        else:
            tags[elem.tag]+=1
    return tags

pprint.pprint(count_tags(OSM))
