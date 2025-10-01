import os

import re

import requests

import datetime

from dotenv import load\_dotenv



\# ✅ Load .env first

load\_dotenv(dotenv\_path="D:/MAGIC/.env")

print("🔁 DEBUG: .env loaded")



\# ✅ Read token and DB ID after loading

NOTION\_TOKEN = os.getenv("NOTION\_TOKEN")

DATABASE\_ID = os.getenv("NOTION\_DATABASE\_ID")



\# ✅ Show partial values

print(f"🔁 DEBUG TOKEN: {NOTION\_TOKEN\[:10] if NOTION\_TOKEN else 'None'}")

print(f"🔁 DEBUG DB ID: {DATABASE\_ID\[:10] if DATABASE\_ID else 'None'}")



\# ✅ Abort early if missing

if not NOTION\_TOKEN or not DATABASE\_ID:

&nbsp;   print("❌ ERROR: Please set NOTION\_TOKEN and NOTION\_DATABASE\_ID in your .env file.")

&nbsp;   exit(1)



\# ✅ Other constants

MAGIC\_ROOT = r"D:\\MAGIC\\scripts"



HEADERS = {

&nbsp;   "Authorization": f"Bearer {NOTION\_TOKEN}",

&nbsp;   "Content-Type": "application/json",

&nbsp;   "Notion-Version": "2022-06-28"

}



def extract\_metadata(filename: str):

&nbsp;   match = re.match(r"(\\d{2})(\[A-Z])\_.\*\_READY\\.py", filename)

&nbsp;   if match:

&nbsp;       phase = int(match.group(1))

&nbsp;       module = match.group(2)

&nbsp;       prefix = f"{phase:02}{module}\_"

&nbsp;       return {

&nbsp;           "Phase": phase,

&nbsp;           "Module": module,

&nbsp;           "Prefix": prefix,

&nbsp;           "Status": "Ready"

&nbsp;       }

&nbsp;   return None



def find\_ready\_scripts():

&nbsp;   file\_data = \[]

&nbsp;   for root, \_, files in os.walk(MAGIC\_ROOT):

&nbsp;       for file in files:

&nbsp;           if file.endswith("\_READY.py"):

&nbsp;               metadata = extract\_metadata(file)

&nbsp;               if metadata:

&nbsp;                   metadata\["Filename"] = file

&nbsp;                   metadata\["Path"] = os.path.join(root, file)

&nbsp;                   metadata\["Last Updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

&nbsp;                   file\_data.append(metadata)

&nbsp;   return file\_data



def notion\_search(filename):

&nbsp;   url = f"https://api.notion.com/v1/databases/{DATABASE\_ID}/query"

&nbsp;   payload = {

&nbsp;       "filter": {

&nbsp;           "property": "Filename",

&nbsp;           "title": {

&nbsp;               "equals": filename

&nbsp;           }

&nbsp;       }

&nbsp;   }

&nbsp;   response = requests.post(url, headers=HEADERS, json=payload)

&nbsp;   return response.json().get("results", \[None])\[0]



def create\_notion\_page(data):

&nbsp;   url = "https://api.notion.com/v1/pages"

&nbsp;   payload = {

&nbsp;       "parent": {"database\_id": DATABASE\_ID},

&nbsp;       "properties": format\_notion\_props(data)

&nbsp;   }

&nbsp;   response = requests.post(url, headers=HEADERS, json=payload)

&nbsp;   return response.ok



def update\_notion\_page(page\_id, data):

&nbsp;   url = f"https://api.notion.com/v1/pages/{page\_id}"

&nbsp;   payload = {

&nbsp;       "properties": format\_notion\_props(data)

&nbsp;   }

&nbsp;   response = requests.patch(url, headers=HEADERS, json=payload)

&nbsp;   return response.ok



def format\_notion\_props(data):

&nbsp;   return {

&nbsp;       "Filename": {"title": \[{"text": {"content": data\["Filename"]}}]},

&nbsp;       "Phase": {"number": data\["Phase"]},

&nbsp;       "Module": {"rich\_text": \[{"text": {"content": data\["Module"]}}]},

&nbsp;       "Prefix": {"rich\_text": \[{"text": {"content": data\["Prefix"]}}]},

&nbsp;       "Status": {"select": {"name": data\["Status"]}},

&nbsp;       "Path": {"rich\_text": \[{"text": {"content": data\["Path"]}}]},

&nbsp;       "Last Updated": {"date": {"start": data\["Last Updated"]}},

&nbsp;   }



def sync\_to\_notion():

&nbsp;   scripts = find\_ready\_scripts()

&nbsp;   print(f"🔍 Found {len(scripts)} READY scripts...")



&nbsp;   for script in scripts:

&nbsp;       existing = notion\_search(script\["Filename"])

&nbsp;       if existing:

&nbsp;           page\_id = existing\["id"]

&nbsp;           if update\_notion\_page(page\_id, script):

&nbsp;               print(f"🔁 Updated: {script\['Filename']}")

&nbsp;           else:

&nbsp;               print(f"❌ Failed to update: {script\['Filename']}")

&nbsp;       else:

&nbsp;           if create\_notion\_page(script):

&nbsp;               print(f"🆕 Created: {script\['Filename']}")

&nbsp;           else:

&nbsp;               print(f"❌ Failed to create: {script\['Filename']}")



if \_\_name\_\_ == "\_\_main\_\_":

&nbsp;   sync\_to\_notion()
