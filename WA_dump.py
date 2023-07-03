import urllib.request
import gzip
import xml.etree.ElementTree as ET
import ssl
import os

try:
    os.remove("output.txt")
except Exception:
    pass

# Disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

# Set the User-Agent header
opener = urllib.request.build_opener()
opener.addheaders = [("User-Agent", "9006")]
urllib.request.install_opener(opener)

# Download and unzip the file
url = "https://www.nationstates.net/pages/nations.xml.gz"
filename = "nations.xml.gz"
urllib.request.urlretrieve(url, filename)
with gzip.open(filename, "rb") as f_in:
    with open("nations.xml", "wb") as f_out:
        f_out.write(f_in.read())

# Parse the XML data
tree = ET.parse("nations.xml")
root = tree.getroot()

# Initialize a dictionary to store nation details
nations = {}

# Iterate over each nation
for nation in root.findall("./NATION"):
    region = nation.find("REGION").text
    unstatus = nation.find("UNSTATUS").text
    if region == "The Wellspring" and (
        unstatus == "WA Delegate" or unstatus == "WA Member"
    ):
        name = nation.find("NAME").text
        name = name.lower().replace(" ", "_")
        endorsements = nation.find("ENDORSEMENTS").text
        endorsement_count = len(endorsements.split(","))
        endorsement_list = endorsements.split(",")
        nations[name] = (endorsement_count, endorsement_list)

# Output the results
for name, (endorsement_count, endorsement_list) in nations.items():
    endorsement_str = "\t".join(endorsement_list)
    print(f"{name}\t{endorsement_count}\t{endorsement_str}")
    with open("output.txt", "a") as f:
        f.write(f"{name}\t{endorsement_count}\t{endorsement_str}\n")

os.remove("nations.xml")
os.remove("nations.xml.gz")
