import requests
from dateutil import parser

API_URL = "https://ll.thespacedevs.com/2.0.0/launch/upcoming/"

def get_upcoming_launches(limit=5):
    params = {"limit": limit}
    try:
        r = requests.get(API_URL, params=params, timeout=10)
        r.raise_for_status()  # if bad response, raise error
        data = r.json()
        results = data.get("results", [])
    except Exception as e:
        print("Error fetching launches:", e)
        return []

    launches = []
    for l in results:
        net = l.get("net")  # launch date/time in string
        try:
            net_dt = parser.parse(net) if net else None
        except Exception:
            net_dt = None

        launches.append({
            "id": l.get("id"),
            "name": l.get("name"),
            "net": net,
            "net_dt": net_dt,
            "status": l.get("status", {}).get("name"),
            "provider": l.get("launch_service_provider", {}).get("name"),
            "pad": l.get("pad", {}).get("name"),
            "location": l.get("pad", {}).get("location", {}).get("name"),
        })

    return launches

if __name__ == "__main__":
    launches = get_upcoming_launches(3)  # fetch 3 upcoming launches
    for launch in launches:
        print(f"🚀 {launch['name']} | {launch['net']} | {launch['location']}")