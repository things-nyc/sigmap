import re
import sys
import json
from base64 import b64decode

def load_ttn_rx(fn):
  with open(fn,'r') as f:
    ds = []
    for line in f:
      m = re.match(r"([\d]+) (.*)",line)
      if m == None:
        continue
      t = int(m.group(1))
      d = json.loads(m.group(2))
      d['server_time'] = t
      payload = b64decode(d['data'])
      d['payload_seq'] = ord(payload[0])*256 + ord(payload[1])
      d['payload_dr'] = ord(payload[2])*256 + ord(payload[3])
      ds.append(d)
  return ds

def load_gps_rx(fn):
  with open(fn,'r') as f:
    ds = []
    ot = 0
    for line in f:
      m = re.match(r"([\d]+) (.*)",line)
      if m == None:
        continue
      t = int(m.group(1))
      s = line.split(',')
      lat = int(s[3][0:2]) + float(s[3][2:])/60
      lat_dir = s[4]
      lon = int(s[5][0:2]) + float(s[5][2:])/60
      lon_dir = s[6]
      d = {}
      d['server_time'] = t
      print t - ot
      ot = t
      d['gps'] = "%f%s,%f%s"%(lat,lat_dir,lon,lon_dir)
      ds.append(d)
  return ds

# find matches in time
def match_ttn_gps(ttn_ds,gps_ds):
  # add gps data to ttn entries
  # damages ttn_ds, and returns merged data
  merged_ds = []
  for td in ttn_ds:
    min_dt = -1
    min_gd = None
    for gd in gps_ds:
      dt = abs(td['server_time'] - gd['server_time'])
      if (min_dt == -1) or (dt < min_dt):
        min_dt = dt
        min_gd = gd
    if min_dt > 10:
      print "ERROR: Unmatched TTN record: %s"%td
    else:
      td['gps'] = min_gd['gps']
      merged_ds.append(td)
  return merged_ds

def to_csv(ttn_ds,fn):
  # render an augmented ttn data set to csv for google sheets
  with open(fn,'w') as f:
    pass

if len(sys.argv) < 4:
  print "Usage: python proc.py <ttn.data> <gps.data> <output.json>"
  exit(-1)

ttn_ds = load_ttn_rx(sys.argv[1])
gps_ds = load_gps_rx(sys.argv[2])
merged_ds = match_ttn_gps(ttn_ds,gps_ds) 
with open(sys.argv[3],'w') as f:
  f.write(json.dumps(merged_ds,sort_keys=True,indent=4,separators=(',', ': ')))

