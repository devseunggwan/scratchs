import hashlib
import hmac
import os
import time
import urllib.parse

import httpx

os.environ["TZ"] = "GMT+0"

accesskey = ""
secretkey = ""
vendor_id = ""

datetime = time.strftime("%y%m%d") + "T" + time.strftime("%H%M%S") + "Z"
method = "GET"
path = f"/v2/providers/openapi/apis/api/v4/vendors/{vendor_id}/returnRequests"
query = urllib.parse.urlencode({"createdAtFrom": "2025-07-01", "createdAtTo": "2025-07-03", "status": "UC"})

message = datetime + method + path + query
signature = hmac.new(secretkey.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()

authorization = (
    "CEA algorithm=HmacSHA256, access-key=" + accesskey + ", signed-date=" + datetime + ", signature=" + signature
)

url = "https://api-gateway.coupang.com" + path + "?%s" % query

headers = {"Content-type": "application/json;charset=UTF-8", "Authorization": authorization}

resp = httpx.get(url, headers=headers)

print(resp.json())
