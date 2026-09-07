import os
import time
import requests
import base64

from dotenv import load_dotenv

load_dotenv()

url = os.getenv("GRAFANA_URL")
user = os.getenv("GRAFANA_USER")
token = os.getenv("GRAFANA_TOKEN")


def send_metric(name, value):
    data = {
        "resourceMetrics": [
            {
                "scopeMetrics": [
                    {
                        "metrics": [
                            {
                                "name": name,
                                "gauge": {
                                    "dataPoints": [
                                        {
                                            "asDouble": value,
                                            "timeUnixNano": str(
                                                int(time.time() * 1_000_000_000)
                                            )
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }

    auth_pair = f"{user}:{token}"
    encoded = base64.b64encode(auth_pair.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        json=data,
        headers=headers,
        timeout=10
    )

    return response.status_code