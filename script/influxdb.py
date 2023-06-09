from datetime import datetime
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "hMaex1gRslj0XkTvvsxAQFOkQ25V0dFY40d8X1LlyK2v84Hx5LFpL_GgjomJSS-s6enIaEeLQN2MymAOO9YBHw=="
org = "Polytech"
bucket = "Temperature"

client = InfluxDBClient(url="http://localhost:8086", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)

data = "mem,host=host1 used_percent=23.43234543"
write_api.write(bucket, org, data)

point = Point("mem")\
  .tag("host", "host1")\
  .field("used_percent", 23.43234543)\
  .time(datetime.utcnow(), WritePrecision.NS)

write_api.write(bucket, org, point)

sequence = ["mem,host=host1 used_percent=23.43234543",
            "mem,host=host1 available_percent=15.856523"]
write_api.write(bucket, org, sequence)

query = f'from(bucket: \\"{bucket}\\") |> range(start: -1h)'
tables = client.query_api().query(query, org=org)
