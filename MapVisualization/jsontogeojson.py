import json 
import sys

input_file = json.load(open(sys.args[1], "r", encoding="utf-8"))

geojs={
     "type": "FeatureCollection",
     "features":[
           {
                "type":"Feature",
                "geometry": {
                "type":"Point",
                "coordinates":[d["y"], d["x"]],
            },
                "properties": {
                    "name":d["name"],
                    "status":d["status"]
                }
        
         } for d in input_file 
    ]  
 }

output_file=open("./public/data/" + sys.args[2], "w", encoding="utf-8")
json.dump(geojs, output_file)


output_file.close()

