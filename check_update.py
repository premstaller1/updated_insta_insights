import requests
import datetime
import json

# Function to make API calls
def makeApiCall(url, endpointParams, debug='no'):
    data = requests.get(url, endpointParams)
    response = dict()
    response['url'] = url
    response['endpoint_params'] = endpointParams
    response['json_data'] = data.json()
    return response

# Function to get a long-lived access token
def getLongLivedAccessToken(params):
    url = params['graph_domain'] + '/oauth/access_token'
    endpointParams = dict()
    endpointParams['grant_type'] = 'fb_exchange_token'
    endpointParams['client_id'] = params['client_id']
    endpointParams['client_secret'] = params['client_secret']
    endpointParams['fb_exchange_token'] = params['access_token']
    return makeApiCall(url, endpointParams, params['debug'])

# Function to debug the access token
def debugAccessToken(params):
    endpointParams = dict()
    endpointParams['input_token'] = params['access_token']
    endpointParams['access_token'] = params['access_token']
    url = params['graph_domain'] + '/debug_token'
    return makeApiCall(url, endpointParams, params['debug'])

# Function to print token expiration
def printTokenExpiration(creds):
    response = debugAccessToken(creds)
    expiration = datetime.datetime.fromtimestamp(response['json_data']['data']['expires_at'])
    profile = creds.get('profile_name', 'Unknown')
    print(f"\n{profile.capitalize()}: Token Expires at: {expiration}")

# Function to update the access token
def updateAccessToken(creds):
    response = getLongLivedAccessToken(creds)
    new_access_token = response['json_data'].get('access_token', None)
    profile = creds.get('profile_name', 'Unknown')
    if new_access_token:
        creds['access_token'] = new_access_token
        print(f"\n ---- {profile.capitalize()} ACCESS TOKEN INFO ----\n")
        print(f"{profile.capitalize()} Access Token:")
        print(new_access_token)
    return creds

# Function to fetch credentials for a given profile
def getCreds(profile='productminimal', file_path='data/metadata.json'):
    # Load JSON data from the file
    with open(file_path, 'r') as file:
        metadata = json.load(file)

    # Check if the profile exists in the metadata
    if profile not in metadata:
        raise ValueError(f"Invalid profile name. Available profiles: {list(metadata.keys())}")

    # Fetch the credentials for the given profile
    creds = metadata[profile]
    creds['profile_name'] = profile  # Add the profile name for reference
    creds['debug'] = 'yes'  # Enable debug mode
    return creds

# Example usage
try:
    creds_minimal = getCreds('productminimal')
    creds_design = getCreds('productsdesign')

    # Print token expiration for both profiles
    printTokenExpiration(creds_minimal)
    printTokenExpiration(creds_design)

    # Optionally update tokens (if needed)
    #updateAccessToken(creds_minimal)
    #updateAccessToken(creds_design)
except Exception as e:
    print(f"Error: {e}")