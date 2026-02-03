from dataclasses import dataclass
import xml.etree.ElementTree as ET
from xml.dom import minidom

#do it one by one, start simple
#future code -  if tag does not exist then create that tag
#               for example, if you have the color tag, and 32768 and 32769 are present
#               and we are trying to add a new color, the code should dynamically add a
#               new color ID with all the parameters

#               Then i have to ensure that that ID is assigned to the row that needs the 
#               color

INPUT_XML_FILE = "MPB_1.2 Manage New Hires.xml"

tree = ET.parse(INPUT_XML_FILE)
root = tree.getroot()