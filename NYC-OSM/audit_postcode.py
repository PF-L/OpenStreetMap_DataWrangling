
import xml.etree.cElementTree as ET
import re
import pprint
from collections import defaultdict

OSM_FILE = "/Users/liupengfei/Documents/GitHub/udacity-data-analyst-nanodegree/P3-Wrangle-OpenStreetMap-Data/sample.osm"
postcode_re = re.compile(r'^\d{5}([\-]?\d{4})?$', re.IGNORECASE)


def audit (osm):
    osm_file = open(osm, "r")
    post_codes = defaultdict(int)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postcode(tag):
                    audit_postcode(post_codes, tag.attrib['v'])
    osm_file.close()
    return post_codes


def audit_postcode(post_codes, codes):
    m = postcode_re.search(codes)
    if m:
        post = m.group()
        if codes not in post:
            post_codes[codes] += 1

def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode" or elem.attrib['k'] == "postal_code")



        
postcodes = audit(OSM_FILE)
pprint.pprint(postcodes)
