import pandas as pd
import json
import requests as r
from dotenv import load_dotenv
import os
load_dotenv()

apiKey = os.environ.get('API-KEY')

popStops = [
10629, 
60105,
10562,
10543,
10542,
10541,
10582,
10545,
10707,
10583,
10619,
10638,
10581,
10615,
60674,
60673]

stopNames = {
    10629: "Northbound Main at James (Concert Hall)",
    60105: "Westbound Dafoe at Agriculture",
    10562: "Eastbound Portage at Tylehurst (Polo Park)",
    10543: "Westbound Portage at Edmonton (Portage Place)",
    10542: "Westbound Portage at Donald (Canada Life Centre)",
    10541: "Westbound Portage at Garry",
    10582: "Eastbound Portage at Donald (Canada Life Centre)",
    10545: "Westbound Portage at Colony",
    10707: "Northbound Vaughan at Portage North",
    10583: "Eastbound Portage at Fort",
    10619: "Westbound Graham at Vaughan (The Bay)",
    10638: "Southbound Main at Pioneer",
    10581: "Eastbound Portage at Edmonton (Portage Place)",
    10615: "Eastbound Graham at Smith",
    60674: "Westbound Dafoe at U of M Station (36, 47, 60)",
    60673: "Westbound Dafoe at U of M Station (74, 75, 78)"
}

data = r.get(f"https://api.winnipegtransit.com/v3/stops/10611/schedule.json?api-key={apiKey}&end=23:59:59").content.decode("UTF-8")

#test = pd.read_json("~/Downloads/superschedule.json")
test = json.loads(data)

df = pd.json_normalize(test['stop-schedule']['route-schedules'], record_path='scheduled-stops')

df['times.arrival.scheduled'] = pd.to_datetime(df['times.arrival.scheduled'])

df['times.arrival.estimated'] = pd.to_datetime(df['times.arrival.estimated'])

df['delay'] = df['times.arrival.estimated'] - df['times.arrival.scheduled']

df['delay'] = df['delay'].dt.seconds

cancelledCount = len(df[df["cancelled"]=="true"])
totalRows = len(df['key'])

df['avg.delay'] = df.groupby('variant.key')['delay'].mean()

print(f"Cancelled count: {cancelledCount}")
print(f"Total buses: {totalRows}")

