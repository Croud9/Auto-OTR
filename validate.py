import requests

def internet():
    try:
        response = requests.get("http://www.google.com")
        return True
    except requests.ConnectionError:
        return False