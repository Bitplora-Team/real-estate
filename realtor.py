import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
import json
import re
from datetime import datetime

cookies = {
    'split': 'n',
    '__vst': 'd9f18355-4e5f-44e1-b3ae-bb750ea02198',
    '__ssn': '4602554b-dfa2-4637-811d-31300a2ab569',
    '__ssnstarttime': '1748336410',
    '__bot': 'false',
    'isAuth0GnavEnabled': 'C',
    '_pbjs_userid_consent_data': '3524755945110770',
    '_lr_env_src_ats': 'false',
    'permutive-id': '21b575d6-94f9-4df3-8117-c245c14ac413',
    'pbjs-unifiedid': '%7B%22TDID%22%3A%22de30569f-47b3-41ff-a404-ac3ca4effe0a%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222025-04-27T09%3A00%3A12%22%7D',
    'pbjs-unifiedid_cst': 'VyxHLMwsHQ%3D%3D',
    'AMCVS_8853394255142B6A0A4C98A4%40AdobeOrg': '1',
    '__split': '26',
    'G_ENABLED_IDPS': 'google',
    's_ecid': 'MCMID%7C20907096253910688211450808722469687203',
    '_gcl_au': '1.1.1361242718.1748336176',
    'claritas_24hrexp_sitevisit': 'true',
    '__spdt': '732a1e63217f40fda88e8bff64d9d4d5',
    '_ga': 'GA1.1.2045649833.1748336177',
    'ajs_anonymous_id': 'cc2a0e27-6c0a-4d64-84c6-cf65c34e9fd7',
    'AMP_MKTG_c07a79acf5': 'JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5nb29nbGUuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5nb29nbGUuY29tJTIyJTdE',
    'crto_is_user_optout': 'false',
    'crto_mapped_user_id_NewsAndInsights': 'iAnEPV9vTGJmJTJGV2hDZUVSRE03Z1h5RnZ3TEhhdzBZdlk2ZWRMUm1xUiUyRk4wTlhYOCUzRA',
    'crto_mapped_user_id_ForSale': 'vg6u9l9vTGJmJTJGV2hDZUVSRE03Z1h5RnZ3TE1YQ2lNJTJGMFJYaSUyQnhhUEcxUUlETkV3JTNE',
    'crto_mapped_user_id_Rental': '8QBavl9vTGJmJTJGV2hDZUVSRE03Z1h5RnZ3TEJBb3VMRG9DVFBieEJlMEg5WlRKajglM0Q',
    'panoramaId_expiry': '1748941215624',
    '_cc_id': '3e05cd2e13fb4dd0b189aeb8795761db',
    'panoramaId': '224a9ab2f9d813806b5ae02afb28185ca02cbe95315064935bd24a47b206346c',
    '_lr_sampling_rate': '100',
    'kampyle_userid': '7e29-6ea6-0105-3f7d-1dea-aeb8-19d4-e3d0',
    'criteria': 'sprefix%3D%252Fnewhomecommunities%26area_type%3Dcity%26city%3DRolling%2520Hills%2520Estates%26pg%3D1%26state_code%3DCA%26state_id%3DCA%26loc%3DRolling%2520Hills%2520Estates%252C%2520CA%26locSlug%3DRolling-Hills-Estates_CA%26county_fips%3D06037%26county_fips_multi%3D06037',
    '__gsas': 'ID=f2d86d392544cbd9:T=1748336518:RT=1748336518:S=ALNI_MZvjh47F5jeg9d5hnaHncxfe6fGmA',
    'kampyleUserSession': '1748336336553',
    'kampyleUserSessionsCount': '2',
    'kampyleUserPercentile': '57.550650173609654',
    'claritas_24hrexp_ldp': 'true',
    'split_tcv': '128',
    '_lr_retry_request': 'true',
    'AMCV_8853394255142B6A0A4C98A4%40AdobeOrg': '-1124106680%7CMCIDTS%7C20236%7CMCMID%7C20907096253910688211450808722469687203%7CMCAAMLH-1748949525%7C12%7CMCAAMB-1748949525%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1748351925s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.2.0',
    'ab.storage.deviceId.7cc9d032-9d6d-44cf-a8f5-d276489af322': 'g%3A5348cf41-6235-95f5-3ad5-de177e1eb04d%7Ce%3Aundefined%7Cc%3A1748336175107%7Cl%3A1748344725751',
    'ab.storage.userId.7cc9d032-9d6d-44cf-a8f5-d276489af322': 'g%3Avisitor_d9f18355-4e5f-44e1-b3ae-bb750ea02198%7Ce%3Aundefined%7Cc%3A1748336175103%7Cl%3A1748344725752',
    'leadid_token-27789EFE-7A9A-DB70-BB9B-97D9B7057DBB-01836014-7527-FD48-9B7F-1A40A9705CFE': '7731D81C-3BA0-835C-B184-9E27DE1D3B64',
    '_parsely_session': '{%22sid%22:2%2C%22surl%22:%22https://www.realtor.com/realestateandhomes-detail/19471-SW-340-St_Homestead_FL_33034_M90537-00530%22%2C%22sref%22:%22https://www.realtor.com/realestateandhomes-detail/19471-SW-340-St_Homestead_FL_33034_M90537-00530%22%2C%22sts%22:1748344734533%2C%22slts%22:1748336235163}',
    '_parsely_visitor': '{%22id%22:%22pid=63174052-bbd4-4275-becb-5afdaca7cdc0%22%2C%22session_count%22:2%2C%22last_session_ts%22:1748344734533}',
    'spec-monthly-payment': 'true',
    'spec-property-history': 'true',
    'spec-neighborhood': 'true',
    'spec-environmental-risk': 'true',
    'spec-real-estimates': 'true',
    'ab.storage.sessionId.7cc9d032-9d6d-44cf-a8f5-d276489af322': 'g%3A02581b96-4656-2798-4f75-8e163ba0b865%7Ce%3A1748346755128%7Cc%3A1748344725750%7Cl%3A1748344955128',
    '_uetsid': '734e92e03ad811f099c6bd8c7e677ff6|1vgwgje|2|fw9|0|1973',
    'AMP_c07a79acf5': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI4NjZlOTJkYS1kNzA2LTQ0NzktOTkxYS05MmFmYjllNDg0NmElMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjJkOWYxODM1NS00ZTVmLTQ0ZTEtYjNhZS1iYjc1MGVhMDIxOTglMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzQ4MzQ0NzI2NzU0JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTc0ODM0NDk1OTM2MyUyQyUyMmxhc3RFdmVudElkJTIyJTNBMjclMkMlMjJwYWdlQ291bnRlciUyMiUzQTIlN0Q=',
    'cto_bundle': 'nC8-Al9ld2ROblAwTjlvRnlncXVDWXV3N1NxSnlCNnYlMkZIaUpkYjBmJTJCa041bHhPaGtLVDhEdzBHMm53eW1EYVpYOE5NdU9aME1vY05LZVU3JTJGdWlVeVQ1UFBDUFdhV2NjckkxZzZ2WWljTE10cUU3enl3Yk8lMkZyanVESU42ZWlLa1NRSmp1NmVVQWVJTzNyaiUyRnRVbXhzT2RrTFd3JTNEJTNE',
    'kampyleSessionPageCounter': '5',
    '__gads': 'ID=50f2c0850d5a5850:T=1748336412:RT=1748345727:S=ALNI_MbZJKQsIbe4S8d6DooS_n6vF0LFXA',
    '__gpi': 'UID=000010f4a33e0492:T=1748336412:RT=1748345727:S=ALNI_MYObkelSCqyu0zA6u55wc-N4UhZkA',
    '__eoi': 'ID=db32fbfd0a1c3d62:T=1748336412:RT=1748345727:S=AA-AfjapV-jUrghSJPqtNv1ZsLBx',
    '_uetvid': '734ef4b03ad811f0b5bd4ff703f87e9e|hc0fki|1748345490538|3|1|bat.bing.com/p/insights/c/l',
    '_ga_07XBH6XBNS': 'GS2.1.s1748344726$o2$g1$t1748345492$j0$l0$h1971240191',
    '_ga_MS5EHT6J6V': 'GS2.1.s1748344726$o2$g1$t1748345492$j0$l0$h0',
    'KP_UIDz-ssn': '02sly629vbV8ls6fJiXqCPVChKGr5ulSQJ6VpAA4tXtHFS4pyxDcWgy39At6bXe69u4qicpsM9jkMLJ6fuoNUnWbPYHspXu3ezyxWiCCCPfQMpvD88ApEfihV01gkk6MZ2hTOWUmcatR8jAh1cEn4bTvaW9zMTRyFs5Yaw3xyj',
    'KP_UIDz': '02sly629vbV8ls6fJiXqCPVChKGr5ulSQJ6VpAA4tXtHFS4pyxDcWgy39At6bXe69u4qicpsM9jkMLJ6fuoNUnWbPYHspXu3ezyxWiCCCPfQMpvD88ApEfihV01gkk6MZ2hTOWUmcatR8jAh1cEn4bTvaW9zMTRyFs5Yaw3xyj',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.realtor.com',
    'priority': 'u=1, i',
    'rdc-client-name': 'RDC_WEB_DETAILS_PAGE',
    'rdc-client-version': '2.1.699',
    'referer': 'https://www.realtor.com/realestateandhomes-detail/19471-SW-340-St_Homestead_FL_33034_M90537-00530',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'x-is-bot': 'false',
}



def fetch_html_content(url: str, headers, cookies) -> Optional[str]:
    """
    Fetches HTML content from a URL
    
    Args:
        url: URL to fetch
        headers: Optional request headers
    
    Returns:
        HTML content as string or None if request fails
    """
    try:
        response = requests.get(
            url,
            cookies=cookies,
            headers=headers,
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def extract_script_content(html: str) -> Optional[str]:
    """
    Extracts content from script tag containing specific identifier
    
    Args:
        html: HTML content
        identifier: String that identifies the target script tag
    
    Returns:
        Script content or None if not found
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find(id="__NEXT_DATA__").string.strip()
    except Exception as e:
        print(f"HTML parsing failed: {e}")
        return None

def extract_data_from_url(url: str, headers, cookies) -> Optional[Dict[str, Any]]:
    """
    Complete pipeline: Fetch HTML → Extract Script → Parse JSON
    
    Args:
        url: Target URL
        script_identifier: String identifying the target script
    
    Returns:
        Parsed JSON data or None if any step fails
    """
    html = fetch_html_content(url, headers, cookies)
    if not html:
        return None
        
    script_content = extract_script_content(html)

    if not script_content:
        return None
    
    script_content = json.loads(script_content)
        
    return script_content


def parse_walk_score_data(outer_data):
    """
    Parses a JSON string containing nested walk score data.
    
    Args:
        json_string (str): The JSON string containing the walk score data
        
    Returns:
        dict: A dictionary containing the parsed walk score data
    """
    try:
        # Extract and clean the inner JSON string
        if 'res' in outer_data and 'text' in outer_data['res']:
            # Split on '&&' and take the second part (the actual JSON)
            inner_json_str = outer_data['res']['text'].split('&&')[1]
            
            # Parse the inner JSON
            inner_data = json.loads(inner_json_str)
            
            return inner_data
        else:
            raise ValueError("Invalid JSON structure - missing 'res.text' field")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing walk score data: {str(e)}")

def get_nested_value(data, keys):
    """
    Safely retrieves a nested value from a dictionary using a list of keys.

    Args:
        data (dict): The dictionary to search within.
        keys (list): A list of keys representing the path to the desired value.

    Returns:
        The value if found, otherwise None.
    """
    current_value = data
    for key in keys:
        if isinstance(current_value, dict) and key in current_value:
            current_value = current_value[key]
        elif isinstance(current_value, list) and key.isdigit() and int(key) < len(current_value):
            current_value = current_value[int(key)]
        else:
            return None
    return current_value

def convert_timestamp_to_dd_mm_yyyy(timestamp_ms):
    """Convert a Unix timestamp in milliseconds to dd-mm-yyyy format."""
    # Convert milliseconds to seconds
    timestamp_seconds = timestamp_ms / 1000
    
    # Create a datetime object from the timestamp
    dt = datetime.fromtimestamp(timestamp_seconds)
    
    # Format the date as dd-mm-yyyy
    return dt.strftime('%d-%m-%Y')


def fetch_school_data(property_id: str, cookies, headers) -> requests.Response:
    params = {
        'operationName': 'GetSchoolData',
        'variables': f'{{"propertyId":"{property_id}"}}',
        'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"ee4267d9cd64801da16099587142fc163d2e04fc6525f2b67924440a90b5f638"}}',
    }

    response = requests.get('https://www.realtor.com/frontdoor/graphql', params=params, cookies=cookies, headers=headers)
    return response

def extract_school_data(data):
    """
    Extracts specific fields (id, name, parent_rating, slug_id) from school data.
    
    Args:
        data: Dictionary containing school data in the provided format
        
    Returns:
        List of dictionaries with only the specified school fields
    """
    cleaned_schools = []
    
    # Navigate through the nested structure to get to the schools list
    schools = data.get("data", {}).get("home", {}).get("schools", {}).get("schools", [])
    
    for school in schools:
        cleaned_school = {
            "id": school.get("id"),
            "name": school.get("name"),
            "parent_rating": school.get("parent_rating"),
            "slug_id": school.get("slug_id")
        }
        cleaned_schools.append(cleaned_school)
    
    return cleaned_schools



def fetch_property_history(property_id, cookies, headers):
    """
    Fetches property and tax history from realtor.com GraphQL API
    
    Args:
        property_id (str): The property ID to query
        
    Returns:
        dict: JSON response from the API
    """
    query = """
    query PropertyAndTaxHistory($propertyId: ID!) {
      home(property_id: $propertyId) {
        status
        property_history {
          date
          event_name
          price
          price_change
          price_sqft
          source_listing_id
          source_name
          price_change_percentage
          days_after_listed
          listing {
            list_price
            last_status_change_date
            last_update_date
            status
            list_date
            listing_id
            __typename
          }
          __typename
        }
        tax_history {
          assessment {
            building
            land
            total
            __typename
          }
          market {
            building
            land
            total
            __typename
          }
          tax
          year
          __typename
        }
        building_permits_history {
          project_name
          permit_type_of_work
          permit_project_type_1
          permit_project_type_2
          permit_project_type_3
          permit_effective_date
          permit_status
          __typename
        }
        __typename
      }
    }
    """

    json_data = {
        'operationName': 'PropertyAndTaxHistory',
        'variables': {
            'propertyId': property_id,
        },
        'query': query,
    }

    try:
        response = requests.post(
            'https://www.realtor.com/frontdoor/graphql',
            cookies=cookies,
            headers=headers,
            json=json_data
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching property history: {e}")
        return None

def extract_price_history(json_data):
    property_history = json_data["data"]["home"]["property_history"]
    price_history = []

    for record in property_history:
        price = record.get("price")
        date_str = record.get("date")

        # Skip records with invalid or missing data
        if price is None or date_str is None or price == 0:
            continue

        # Convert "YYYY-MM-DD" to "DD-MM-YYYY"
        try:
            formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d-%m-%Y")
        except ValueError:
            continue

        price_history.append({
            "price": price,
            "date": formatted_date
        })

    return price_history

def fetch_env_data(property_id, cookies, headers):
    params = {
        'operationName': 'EnvironmentRiskSummary',
        'variables': f'{{"propertyId":"{property_id}"}}',
        'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"5fc865b6b73271a8407db86a7fe4713c0de14d415e3df086c8f88102c53f028f"}}',
    }

    try:
        response = requests.get('https://www.realtor.com/frontdoor/graphql', params=params, cookies=cookies, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching environmental data: {e}")
        return None


def extract_env_data(data):
    """
    Extracts specific fields (id, name, parent_rating, slug_id) from env data.
    
    Args:
        data: Dictionary containing environmental data in the provided format
        
    Returns:
        List of dictionaries with only the specified school fields
    """
    cleaned_envs = []
    
    # Navigate through the nested structure
    envs = data.get("data", {}).get("home", {}).get("local", {})
    
    # Remove the __typename key and process each environmental factor
    for factor_name, factor_data in envs.items():
        if factor_name != "__typename":  # Skip the __typename field
            # Create a cleaned version of each factor's data
            cleaned_factor = {
                "factor": factor_name,
                "severity": factor_data.get(f"{factor_name}_factor_severity"),
                "trend": factor_data.get(f"{factor_name}_trend")
            }
            cleaned_envs.append(cleaned_factor)
    
    return cleaned_envs


def safe_get(data, path, default=None):
    """Helper to safely get nested values from dict."""
    keys = path.split('.')
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return default
    return data


def extract_property_data(payload, school_data, property_history_data):
    """
    Extracts property information from a JSON payload and returns a structured dictionary.
    
    Args:
        payload (dict): A dictionary containing property data (props from the page).
        
    Returns:
        dict: A structured dictionary containing extracted property fields.
    """
    # Initialize the result structure with all possible fields
    extracted_data = {
        "zpid": None,
        "propertyType": None,
        "listingType": None,
        "listingStatus": None,
        "address": {
            "community": None,
            "city": None,
            "state": None,
            "neighborhood": None,
            "subdivision": None,
            "streetAddress": None,
            "zipcode": None,
            "unitNumber": None
        },
        "countyFIPS": None,
        "mlsId": None,
        "parcelNumber": None,
        "lat": None,
        "lng": None,
        "images": [],
        "virtualTourUrl": None,
        "googleMapsStreetView": None,
        "floorPlanImages": [],
        "videoWalkthroughs": [],
        "price": None,
        "pricePerSqFt": None,
        "priceHistory": [],
        "estimatedValue": None,
        "monthlyRentEstimate": None,
        "livingAreaValue": None,
        "lotSize": None,
        "lotUnits": None,
        "bedrooms": None,
        "bathrooms": {
            "full": None,
            "half": None,
            "total": None
        },
        "yearBuilt": None,
        "lastRenovatedYear": None,
        "stories": None,
        "basement": None,
        "garageSpaces": None,
        "parkingType": None,
        "foundationType": None,
        "constructionMaterials": None,
        "roofType": None,
        "roofCondition": None,
        "heatingType": None,
        "coolingType": None,
        "energyEfficiency": None,
        "flooring": [],
        "interiorFeatures": [],
        "exteriorFeatures": [],
        "hasGarage": None,
        "petsAllowed": None,
        "restrictions": [],
        "monthlyHoaFee": None,
        "hoaIncludes": [],
        "taxHistory": None,
        "assessedValue": None,
        "dateSold": None,
        "previousSalePrice": None,
        "mortgageInfo": None,
        "homeInsuranceEstimate": None,
        "propertyTaxEstimate": None,
        "creditScoreRequirement": None,
        "contactRecipients": {
            "agentName": None,
            "displayName": None,
            "badgeType": None,
            "reviewCount": None,
            "phoneNumber": None,
            "email": None,
            "businessName": None,
            "licenseNumber": None,
            "agentRatings": None,
            "recentSales": None,
            "agencyWebsite": None
        },
        "schoolDistrict": None,
        "transportation": None,
        "walkScore": None,
        "transitScore": None,
        "bikeScore": None,
        "buildingPermits": None,
        "Section 8 acceptance": None,
        "rentalTerms": None,
        "furnishedStatus": None,
        "climate": None,
        "naturalHazardRisk": {
            "fireZone": None,
            "floodZone": None,
            "windRisk": None,
            "heatRisk": None,
            "airQualityIndex": None,
            "earthquakeRisk": None
        },
        "climateChangeProjection": None,
        "nearByHomes": None,
        "sources": []
    }

    # Get the property details section
    property_details = safe_get(payload, "props.pageProps.initialReduxState.propertyDetails", {})

    if not property_details:
        return extracted_data

    # Basic property info
    extracted_data["zpid"] = safe_get(property_details, "property_id")
    extracted_data["propertyType"] = safe_get(property_details, "description.type").replace('_', ' ').title()
    extracted_data["listingType"] = safe_get(property_details, "status").replace('_', ' ').title()
    extracted_data["listingStatus"] = safe_get(property_details, "source.raw.status")

    # Address info
    address = safe_get(property_details, "location.address", {})
    extracted_data["address"].update({
        "city": address.get("city"),
        "state": address.get("state"),
        "streetAddress": address.get("line"),
        "zipcode": address.get("postal_code"),
        "unitNumber": address.get("unit")
    })

    # Location info
    extracted_data["countyFIPS"] = safe_get(property_details, "location.county.fips_code")
    extracted_data["lat"] = safe_get(property_details, "location.latitude")
    extracted_data["lng"] = safe_get(property_details, "location.longitude")
    extracted_data["googleMapsStreetView"] = safe_get(property_details, "location.street_view_url")

    # Load Photos
    if gallery := safe_get(property_details, "augmented_gallery", []):
        for collection in gallery:
            if collection['key'] == "all_photos":
                for photo in collection['photos']:
                    if "tag" == "floor_plan":
                        extracted_data["floorPlanImages"].append(photo['href'])
                    else:
                        extracted_data['images'].append(photo['href'])

    # Virtual tours
    if virtual_tours := safe_get(property_details, "virtual_tours"):
        extracted_data["virtualTourUrl"] = virtual_tours[0].get("url") if virtual_tours else None
    elif home_tours := safe_get(property_details, "home_tours.virtual_tours"):
        extracted_data["virtualTourUrl"] = home_tours[0].get("url") if home_tours else None
    
    # Video Walkthroughs
    if videos := safe_get(property_details, "community.videos"):
        for vdo in videos:
            extracted_data['videoWalkthroughs'].append(vdo['href'])

    # Pricing info
    extracted_data["price"] = safe_get(property_details, "list_price")
    extracted_data["pricePerSqFt"] = safe_get(property_details, "price_per_sqft")
    extracted_data['monthlyRentEstimate'] = safe_get(property_details, "mortgage.estimate.monthly_payment")

    # Mortgage Info
    mortgage_data = safe_get(property_details, "mortgage", {})
    if mortgage_data:
        extracted_data["mortgageInfo"] = {
            "property_tax_rate": mortgage_data.get("property_tax_rate"),
            "average_rates": [
                {
                    "rate": rate.get("rate"),
                    "loan_type": {
                        "display_name": safe_get(rate, "loan_type.display_name"),
                        "term": safe_get(rate, "loan_type.term")
                    }
                }
                for rate in mortgage_data.get("average_rates", [])
                if rate.get("rate") is not None
            ],
            "closing_cost": mortgage_data.get("closing_cost")
        }

        extracted_data['homeInsuranceEstimate'] = mortgage_data.get("insurance_rate")
        

    # Garage Details
    n_garage = int(safe_get(property_details, "description.garage").strip())
    extracted_data['garageSpaces'] = n_garage
    extracted_data['hasGarage'] = n_garage > 0

    # Category Details
    if categories := safe_get(property_details, "details", []):
        for cat in categories:
            if "interior" in cat['category'].lower():
                extracted_data['interiorFeatures'] = cat['text']

                # look for flooring
                for intr_val in cat['text']:
                    if "flooring" in intr_val.lower():
                        extracted_data['flooring'] = intr_val.split(':')[-1].strip()
                    elif "furnished" in intr_val.lower():
                        extracted_data['furnishedStatus'] = intr_val
            elif "construction" in cat['category'].lower():
                for txt_val in cat['text']:
                    if "foundation" in txt_val.lower():
                        extracted_data['foundationType'] = txt_val.split(':')[-1].strip()
                    elif "construction" in txt_val.lower():
                        extracted_data['constructionMaterials'] = txt_val.split(':')[-1].strip()
            elif "heating and cooling" in cat['category'].lower():
                for txt_val in cat['text']:
                    if "cooling features:" in txt_val.lower():
                        extracted_data['coolingType'] = txt_val.split(':')[-1].strip()
                    elif "heating features:" in txt_val.lower():
                        extracted_data['heatingType'] = txt_val.split(':')[-1].strip()
            if "exterior" in cat['category'].lower():
                extracted_data['exteriorFeatures'] = cat['text']
    
    # Property tax estimate
    property_tax = safe_get(property_details, "mortgage.property_tax_rate")
    if property_tax is not None:
        extracted_data["propertyTaxEstimate"] = property_tax

    # Contact recipients
    agents = safe_get(property_details, "source.agents", {})
    if agents:
        contact_recipients = {}
        agent = agents[0]
        agent_name = safe_get(agent, "agent_name")
        if agent_name is not None:
            contact_recipients["agentName"] = agent_name
        
        phone = safe_get(agent, "agent_phone")
        if phone is not None:
            contact_recipients["phoneNumber"] = phone
        
        email = safe_get(agent, "agent_email")
        if email is not None:
            contact_recipients["email"] = email
    
    extracted_data['contactRecipients'] = contact_recipients
        
    # Nearby homes
    nearby_homes = safe_get(property_details, "other_listings")
    if nearby_homes is not None:
        extracted_data["nearByHomes"] = nearby_homes

    # Remove empty objects
    if not extracted_data["contactRecipients"]:
        del extracted_data["contactRecipients"]
    if not extracted_data["naturalHazardRisk"]:
        del extracted_data["naturalHazardRisk"]
    if extracted_data["sources"] == []:
        del extracted_data["sources"]
    
    extracted_data["dateSold"] = safe_get(property_details, "last_sold_date")
    extracted_data["previousSalePrice"] = safe_get(property_details, "last_sold_price")
    
    # Property description
    description = safe_get(property_details, "description", {})
    extracted_data.update({
        "lotSize": description.get("lot_sqft"),
        "bedrooms": description.get("beds"),
        "bathrooms": description.get("baths"),
        "yearBuilt": description.get("year_built"),
        "stories": description.get("stories"),
        "livingAreaValue": description.get("sqft"),
        "lastRenovatedYear": description.get("year_renovated"),
        "heatingType": description.get("heating"),
        "coolingType": description.get("cooling"),
        "exteriorFeatures": description.get("exterior"),
        "monthlyHoaFee": safe_get(description, "hoa.fee"),
    })

    return extracted_data


def scrape_url(target_url: str):    
    data = extract_data_from_url(target_url, headers, cookies)

    print("Realtor page data extracted.")

    if data:
        property_id = safe_get(data, "props.pageProps.initialReduxState.propertyDetails.property_id")

        headers['referer'] = target_url

        school_data_response = fetch_school_data(property_id, cookies, headers)
        school_data = json.loads(school_data_response.text)
        school_data = extract_school_data(school_data)
        print("School data extracted.")
        
    
        price_history_response = fetch_property_history(property_id, cookies, headers)
        price_history = json.loads(price_history_response.text)
        price_history = extract_price_history(price_history)
        print("Price history extracted.")

        env_data_response = fetch_env_data(property_id, cookies, headers)
        env_data = json.loads(env_data_response.text)
        env_data = extract_env_data(env_data)
        print("Env data extracted.")
        
        mapped_data = extract_property_data(data, school_data, price_history)

        mapped_data['schoolDistrict'] = school_data
        mapped_data['priceHistory'] = price_history
        mapped_data['naturalHazardRisk'] = env_data
        mapped_data['url'] = target_url

        with open('realtor-output.json', 'w') as f:
            json.dump(mapped_data, f)
        
        return mapped_data
    else:
        print("Failed to extract data")
    
    return None

if __name__ == "__main__":
    target_url = "https://www.realtor.com/realestateandhomes-detail/27649-Palos-Verdes-Dr-E_Rolling-Hills-Estates_CA_90275_M20714-41985?from=srp-list-card"

    scraped_data = scrape_url(target_url)

    print(scraped_data)
