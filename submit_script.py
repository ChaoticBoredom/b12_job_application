from datetime import datetime, timezone
import hashlib
import hmac
import json
import os
import urllib.request

signing_secret = os.environ["B12_SIGNING_SECRET"].encode("utf-8")
email = os.environ["B12_EMAIL"]
resume_link = os.environ["B12_RESUME"]

url = "https://b12.io/apply/submission"

data = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "name": "Susan Wright",
    "email": email,
    "resume_link": resume_link,
    "repository_link": "https://github.com/ChaoticBoredom/b12_job_application",
    "action_run_link": "https://github.com/ChaoticBoredom/b12_job_application/actions/runs/25028663956"
}

request_body = json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")

digest = hmac.new(signing_secret, request_body, hashlib.sha256).hexdigest()
signature = f"sha256={digest}"

req = urllib.request.Request(url, data=request_body, method="POST")
req.add_header("Content-Type", "application/json")
req.add_header("X-Signature-256", signature)

with urllib.request.urlopen(req) as response:
    response_body = response.read().decode()
    print(response_body)

