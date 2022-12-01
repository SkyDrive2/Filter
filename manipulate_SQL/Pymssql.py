import pymssql

IP = "localhost"
PORT = "5000"
POST_URL = f"http://{IP}:{PORT}/api/activities"

conn = pymssql.connect(server = POST_URL,user = )