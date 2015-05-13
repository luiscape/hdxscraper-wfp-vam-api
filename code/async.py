
import os
import json
import grequests

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

urls = [
    'https://data.hdx.rwlabs.org/api/action/package_show?id=syria-border-crossings',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=ebola-cases-2014',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=openstreetmap-shapefiles-for-gis-softwares-daily-updates',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=syria-border-crossings',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=syria-border-crossings',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=ebola-cases-2014',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=openstreetmap-shapefiles-for-gis-softwares-daily-updates',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=syria-border-crossings',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=syria-border-crossings',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=ebola-cases-2014',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=openstreetmap-shapefiles-for-gis-softwares-daily-updates',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=syria-border-crossings',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=syria-border-crossings',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=ebola-cases-2014',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=openstreetmap-shapefiles-for-gis-softwares-daily-updates',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=syria-border-crossings',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=syria-border-crossings',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=ebola-cases-2014',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=ebola-cases-2014',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=openstreetmap-shapefiles-for-gis-softwares-daily-updates',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=syria-border-crossings',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=syria-border-crossings',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=ebola-cases-2014',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=openstreetmap-shapefiles-for-gis-softwares-daily-updates',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=syria-border-crossings',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=syria-border-crossings',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=ebola-cases-2014',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=ebola-cases-2014',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=openstreetmap-shapefiles-for-gis-softwares-daily-updates',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=syria-border-crossings',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=syria-border-crossings',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=ebola-cases-2014',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=openstreetmap-shapefiles-for-gis-softwares-daily-updates',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=syria-border-crossings',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=syria-border-crossings',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=ebola-cases-2014',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=openstreetmap-shapefiles-for-gis-softwares-daily-updates',
    'https://data.hdx.rwlabs.org/api/action/package_show?id=syria-border-crossings'
]

rs = (grequests.get(u) for u in urls)
responses = grequests.map(rs)

index = 1
for response in responses:
  # print "Writing data for %s/%s" % (index, len(responses))
  
  data = response.json()

  j_path = os.path.join(dir, 'data/') + str(index) + '.json'
  with open(j_path, 'w') as outfile:
    json.dump(data, outfile)

  index += 1