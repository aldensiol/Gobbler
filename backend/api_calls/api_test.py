import json

with open('C:/repos/NCS/backend/api_calls/trafficflow.json', 'r') as file:
    data = json.load(file)


clementi_road_data = [record for record in data["Value"] if record["RoadName"] == "CLEMENTI ROAD"]

with open('C:/repos/NCS/backend/api_calls/clementi_road_data.json', 'w') as file:
    json.dump(clementi_road_data, file, indent=4)