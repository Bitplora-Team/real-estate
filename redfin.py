import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
import json
import re
from datetime import datetime

def fetch_html_content(url: str, headers: Optional[Dict] = None) -> Optional[str]:
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
            headers=headers or {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            timeout=10
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def extract_script_content(html: str, identifier: str) -> Optional[str]:
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
        for script in soup.find_all('script'):
            if script.string and identifier in script.string:
                return script.string.strip()
        return None
    except Exception as e:
        print(f"HTML parsing failed: {e}")
        return None

def parse_json_from_script(script_content: str) -> Optional[Dict[str, Any]]:
    """
    Extracts JSON data from script content containing reactServerState
    
    Args:
        script_content: The full script content with JS wrapper
        
    Returns:
        Parsed JSON data as dictionary or None if parsing fails
    """
    try:
        # Find the start of the JSON data
        start_marker = "__reactServerState.InitialContext ="
        start_idx = script_content.find(start_marker)
        if start_idx == -1:
            return None
        
        # Adjust start index to beginning of JSON
        start_idx += len(start_marker)
        
        # Find the end of the JSON data
        end_marker = "root.__reactServerState.Config"
        end_idx = script_content.find(end_marker, start_idx)

        json_str = script_content[start_idx:end_idx].strip()

        if json_str.endswith(';'):
            json_str = json_str[:-1]
            
        return json.loads(json_str)
    except (ValueError, AttributeError, json.JSONDecodeError) as e:
        print(f"JSON parsing failed: {e}")
        print(f"Problematic content: {json_str[:200]}...")  # Print first 200 chars for debugging
        return None

def extract_data_from_url(url: str, script_identifier: str) -> Optional[Dict[str, Any]]:
    """
    Complete pipeline: Fetch HTML → Extract Script → Parse JSON
    
    Args:
        url: Target URL
        script_identifier: String identifying the target script
    
    Returns:
        Parsed JSON data or None if any step fails
    """
    html = fetch_html_content(url)
    if not html:
        return None
        
    script_content = extract_script_content(html, script_identifier)

    if not script_content:
        return None
        
    return parse_json_from_script(script_content)


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


def extract_property_data(payload):
    """
    Extracts property information from a JSON payload and returns a structured dictionary.
    
    Args:
        payload (dict): A dictionary containing property data.
        
    Returns:
        dict: A structured dictionary containing extracted property fields.
    """
    # Initialize the result structure with all possible fields
    extracted_data = {
        "zpId": None,
        "propertyType": None,
        "listingStatus": None,
        "address": {
            "community": None, "city": None, "state": None,
            "subdivision": None, "streetAddress": None, "zipcode": None, "unitNumber": None
        },
        "countyFIPS": None, "mlsId": None, "parcelNumber": None,
        "lat": None, "lng": None, "images": [], "virtualTourUrl": None,
        "googleMapsStreetView": None, "floorPlanImages": None, "videoWalkthroughs": [],
        "price": None, "pricePerSqFt": None, "priceHistory": None,
        "monthlyRentEstimate": None, "lotSize": None, "lotUnits": None,
        "bedrooms": None, "bathrooms": {"full": None, "half": None, "total": None},
        "yearBuilt": None, "lastRenovatedYear": None, "stories": None,
        "basement": None, "garageSpaces": None, "parkingType": None,
        "foundationType": None, "constructionMaterials": None,
        "roofType": None, "roofCondition": None, "heatingType": None,
        "coolingType": None, "energyEfficiency": None, "flooring": [],
        "interiorFeatures": [], "exteriorFeatures": [], "hasGarage": None,
        "petsAllowed": None, "restrictions": [], "monthlyHoaFee": None,
        "hoaIncludes": [], "taxHistory": None, "assessedValue": None,
        "dateSold": None, "previousSalePrice": None, "mortgageInfo": None,
        "homeInsuranceEstimate": None, "propertyTaxEstimate": None,
        "creditScoreRequirement": None, "contactRecipients": {
            "agentName": None, "displayName": None, "badgeType": None,
            "reviewCount": None, "phoneNumber": None, "email": None,
            "businessName": None, "licenseNumber": None, "agentRatings": None,
            "recentSales": None, "agencyWebsite": None
        },
        "schoolDistrict": None, "transportation": None, "walkScore": None,
        "transitScore": None, "bikeScore": None, "buildingPermits": None,
        "Section 8 acceptance": None, "rentalTerms": None, "furnishedStatus": None,
        "climate": None, "naturalHazardRisk": {
            "fireZone": None, "floodZone": None, "windRisk": None,
            "heatRisk": None, "airQualityIndex": None, "earthquakeRisk": None
        },
        "climateChangeProjection": None, "nearByHomes": None, "sources": []
    }

    def safe_get(data, path, default=None):
        """Helper to safely get nested values from dict."""
        for key in path:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return default
        return data

    # Extract from mainHouseInfo
    main_house = safe_get(payload, ["mainHouseInfo"], {})
    if main_house:
        extracted_data["mlsId"] = safe_get(main_house, ["mlsId"])
        extracted_data["listingStatus"] = safe_get(main_house, ["mlsStatusDisplay", "displayValue"])
        
        # Sources
        sources = []
        if desc := safe_get(main_house, ["source", "dataSourceDescription"]):
            sources.append(f"Data Source: {desc}")
        if name := safe_get(main_house, ["source", "dataSourceName"]):
            sources.append(f"Data Source Name: {name}")
        extracted_data["sources"].extend(sources)
        
        # Address
        addr = safe_get(main_house, ["propertyAddress"], {})
        if addr:
            extracted_data["address"].update({
                "city": addr.get("city"),
                "state": addr.get("stateOrProvinceCode"),
                "zipcode": addr.get("postalCode"),
                "streetAddress": " ".join(filter(None, [
                    addr.get("streetNumber"),
                    addr.get("directionalPrefix"),
                    addr.get("streetName"),
                    addr.get("streetType"),
                    addr.get("directionalSuffix")
                ])).strip(),
                "unitNumber": addr.get("unitValue")
            })
                
        # Agent info
        if agents := safe_get(main_house, ["listingAgents"], []):
            if agents and (agent := agents[0]):
                extracted_data["contactRecipients"].update({
                    "agentName": safe_get(agent, ["agentInfo", "agentName"]),
                    "businessName": agent.get("brokerName")
                })
        
        # Marketing remarks
        if remarks := safe_get(main_house, ["marketingRemarks"], []):
            if remarks and (remark := remarks[0].get("marketingRemark", "").lower()):
                # Interior features
                for feature in ["skylight", "built-in", "eat-in area", "in-unit laundry"]:
                    if feature in remark:
                        extracted_data["interiorFeatures"].append(feature.title())
                
                # Exterior features
                for feature in ["fenced backyard", "concrete side driveway", "metal railings", "vinyl fence"]:
                    if feature in remark:
                        extracted_data["exteriorFeatures"].append(feature.title())
                
                # Construction materials
                if "brick" in remark:
                    extracted_data["constructionMaterials"] = "Brick"
                
                # Garage spaces
                if "garage" in remark and extracted_data["garageSpaces"] is None:
                    if match := re.search(r'(\d+\.?\d*)-car garage', remark):
                        try:
                            spaces = float(match.group(1))
                            extracted_data["garageSpaces"] = spaces
                            extracted_data["hasGarage"] = spaces > 0
                        except ValueError:
                            pass

    # Price History
    extracted_data['priceHistory'] = []
    if price_history := safe_get(payload, ['propertyHistoryInfo', 'events'], []):
        for event in price_history:
            if event.get('price'):
                extracted_data['priceHistory'].append({
                    'price': event.get('price'),
                    'date': convert_timestamp_to_dd_mm_yyyy(event.get('eventDate')) if event.get('eventDate') else ''
                })


    # Extract from selectedAmenities
    for amenity in safe_get(payload, ["mainHouseInfo", "selectedAmenities"], []):
        header, content = amenity.get("header"), amenity.get("content")
        if not header or not content:
            continue
            
        if header == "Community":
            extracted_data["address"]["community"] = content
        elif header == "MLS#" and not extracted_data["mlsId"]:
            extracted_data["mlsId"] = content
        elif header == "Built":
            extracted_data["yearBuilt"] = content
        elif header == "Property Type":
            extracted_data["propertyType"] = content
        elif header == "Heating & cooling":
            extracted_data["heatingType"] = content
            if "a/c" in content.lower():
                extracted_data["coolingType"] = "Has A/C"
        elif header == "Laundry":
            extracted_data["interiorFeatures"].append(content)
        elif header == "Parking":
            content_lower = content.lower()
            if "garage" in content_lower:
                extracted_data["parkingType"] = "Garage"
                if match := re.search(r'(\d+\.?\d*)\s*car garage', content_lower):
                    try:
                        spaces = float(match.group(1))
                        extracted_data["garageSpaces"] = spaces
                        extracted_data["hasGarage"] = spaces > 0
                    except ValueError:
                        pass
            elif "driveway" in content_lower and not extracted_data["parkingType"]:
                extracted_data["parkingType"] = "Driveway"

    # Fallback property type and status
    addr_info = safe_get(payload, ["addressSectionInfo"], {})
    extracted_data["propertyType"] = extracted_data["propertyType"] or addr_info.get("propertyType")
    extracted_data["listingStatus"] = extracted_data["listingStatus"] or safe_get(addr_info, ["status", "displayValue"])

    # Fallback address info
    addr_data = extracted_data["address"]
    street_addr = safe_get(addr_info, ["streetAddress", "assembledAddress"])
    addr_data.update({
        "streetAddress": addr_data["streetAddress"] or street_addr,
        "city": addr_data["city"] or addr_info.get("city"),
        "state": addr_data["state"] or addr_info.get("state"),
        "zipcode": addr_data["zipcode"] or addr_info.get("zip"),
        "unitNumber": addr_data["unitNumber"] or safe_get(addr_info, ["streetAddress", "unitValue"])
    })

    # Basic property info
    lat_long = addr_info.get("latLong", {})
    extracted_data.update({
        "countyFIPS": addr_info.get("fips"),
        "parcelNumber": addr_info.get("apn"),
        "lat": lat_long.get("latitude"),
        "lng": lat_long.get("longitude"),
        "price": safe_get(addr_info, ["latestPriceInfo", "amount"]),
        "pricePerSqFt": addr_info.get("pricePerSqFt"),
        "lotSize": extracted_data["lotSize"] or addr_info.get("lotSize"),
        "bedrooms": addr_info.get("beds"),
        "bathrooms": {
            "full": addr_info.get("numFullBaths"),
            "half": addr_info.get("numPartialBaths"),
            "total": addr_info.get("baths")
        },
        "yearBuilt": extracted_data["yearBuilt"] or addr_info.get("yearBuilt"),
        "dateSold": convert_timestamp_to_dd_mm_yyyy(addr_info.get('soldDate')) if addr_info.get("soldDate") else None,
        "googleMapsStreetView": safe_get(payload, ["mediaBrowserInfo", "streetView", "streetViewUrl"])
    })

    # Images and media
    if photos := safe_get(payload, ["mediaBrowserInfo", "photos"], []):
        extracted_data["images"] = [p["photoUrls"]["fullScreenPhotoUrl"] for p in photos if p.get("photoUrls", {}).get("fullScreenPhotoUrl")]
    
    if floor_plans := payload.get("tagsByPhotoId"):
        extracted_data["floorPlanImages"] = [v["photoUrl"] for v in floor_plans.values() if "Floor plans" in v.get("tags", [])]
    
    if videos := safe_get(payload, ["mediaBrowserInfo", "videos"], []):
        extracted_data["videoWalkthroughs"] = videos

    # Tax info
    extracted_data["taxHistory"] = safe_get(payload, ["publicRecordsInfo", "allTaxInfo"])

    extracted_data["stories"] = safe_get(payload, ["publicRecordsInfo", "latestListingInfo", "numStories"])

    # Amenities
    for super_group in safe_get(payload, ["amenitiesInfo", "superGroups"], []):
        for group in super_group.get("amenityGroups", []):
            for entry in group.get("amenityEntries", []):
                name, values = entry.get("amenityName"), entry.get("amenityValues", [])
                if not name and not values:
                    continue
                
                name_lower = name.lower() if name else ''
                if "interior" in name_lower or "feature" in name_lower:
                    extracted_data["interiorFeatures"].extend(values)
                elif "exterior" in name_lower:
                    extracted_data["exteriorFeatures"].extend(values)
                elif "heating" in name_lower and not extracted_data["heatingType"]:
                    extracted_data["heatingType"] = ", ".join(values)
                elif ("cooling" in name_lower or "ac" in name_lower) and not extracted_data["coolingType"]:
                    extracted_data["coolingType"] = ", ".join(values)
                elif "garage spaces" in name_lower and not extracted_data["garageSpaces"]:
                    try:
                        spaces = float(values[0])
                        extracted_data["garageSpaces"] = spaces
                        extracted_data["hasGarage"] = spaces > 0
                    except (ValueError, IndexError):
                        pass
                elif "lot" in name_lower and "size" in name_lower:
                    extracted_data["lotSize"] = values[0] if values else ''
                    if values and values[0]:
                        extracted_data["lotUnits"] = "sq ft" if "square feet" in values[0].lower() else "acres" if "acres" in values[0].lower() else None
                elif "parking" in name_lower and "type" in name_lower and not extracted_data["parkingType"]:
                    extracted_data["parkingType"] = ", ".join(values)
                elif "foundation" in name_lower:
                    extracted_data["foundationType"] = ", ".join(values)
                elif "construction" in name_lower and "material" in name_lower and not extracted_data["constructionMaterials"]:
                    extracted_data["constructionMaterials"] = ", ".join(values)
                elif "roof" in name_lower and "type" in name_lower:
                    extracted_data["roofType"] = ", ".join(values)
                elif "pets allowed" in name_lower and not extracted_data['petsAllowed']:
                    extracted_data["petsAllowed"] = True if values else None
                elif "restrictions" in name_lower or "hoa" in name_lower:
                    extracted_data["restrictions"].extend(values)
                elif "hoa includes" in name_lower:
                    extracted_data["hoaIncludes"].extend(values)
                elif "renovated" in name_lower:
                    extracted_data["lastRenovatedYear"] = values[0] if values else None
                elif "subdivision" in name_lower:
                    extracted_data['address']['subdivision'] = values[0] if values else None
                # Check in groupTitle
                elif group.get("referenceName") and "virtual" in group.get("referenceName").lower():
                    html = values[0] if values else None
                    match = re.search(r"href='([^']*)'", html)
                    if match:
                        extracted_data['virtualTourUrl'] = match.group(1)
                # Fill Floorings
                elif "flooring" in name_lower:
                    extracted_data['flooring'].extend(values)


    # Mortgage info
    if mortgage := safe_get(payload, ["publicRecordsInfo", "mortgageCalculatorInfo"]):
        extracted_data["mortgageInfo"] = {
            "monthlyPaymentEstimates": {
                k: mortgage.get(k) for k in [
                    "listingPrice", "downPaymentPercentage", 
                    "propertyTaxRate", "homeInsuranceRate", 
                    "mortgageInsuranceRate"
                ]
            },
            "interestRates": {
                "fixedRates": {
                    k: safe_get(mortgage, ["mortgageRateInfo", k]) for k in [
                        "tenYearFixed", "fifteenYearFixed", 
                        "twentyYearFixed", "thirtyYearFixed"
                    ]
                },
                "adjustableRates": {
                    k: safe_get(mortgage, ["mortgageRateInfo", k]) for k in [
                        "fiveOneArm", "sevenYearArm", "tenYearArm"
                    ]
                },
                "jumboRates": {
                    k: safe_get(mortgage, ["mortgageRateInfo", k]) for k in [
                        "tenYearFixedJumbo", "fifteenYearFixedJumbo",
                        "twentyYearFixedJumbo", "thirtyYearFixedJumbo"
                    ]
                }
            },
            "downPayment": {
                "percentage": mortgage.get("downPaymentPercentage"),
                "amount": (mortgage.get("listingPrice", 0) * (mortgage.get("downPaymentPercentage", 0) / 100 
                          if mortgage.get("listingPrice") and mortgage.get("downPaymentPercentage") 
                          else None))
            }
        }
        extracted_data['monthlyHoaFee'] = mortgage.get('monthlyHoaDues')
        
    # School info
    school_info = payload.get("schoolsAndDistrictsInfo", {})
    extracted_data["schoolDistrict"] = {
        "servingThisHomeSchools": school_info.get("servingThisHomeSchools"),
        "districtsServingThisHome": school_info.get("districtsServingThisHome")
    }

    # Transit Info
    if transits := safe_get(payload, ["transitData", "stops"]):
        extracted_data["transportation"] = []
        for stop in transits:
            extracted_data['transportation'].append({
                t: stop.get(t) for t in ["stopName", "agencies"]
            })

    # Deduplicate lists
    for field in ["interiorFeatures", "exteriorFeatures", "restrictions", "hoaIncludes", "sources"]:
        if extracted_data[field]:
            extracted_data[field] = list(set(extracted_data[field]))

    return extracted_data

def scrape_url(target_url: str):
    script_identifier = "_tLAB.wait"
    
    data = extract_data_from_url(target_url, script_identifier)
    
    if data:
        merged_response = {}

        for data_route in data['ReactServerAgent.cache']['dataCache'].keys():
            try:
                route_response = parse_walk_score_data(data['ReactServerAgent.cache']['dataCache'][data_route])
                try:
                    merged_response.update(route_response['payload'])
                except:
                    pass
            except Exception as e:
                continue
        
        mapped_data = extract_property_data(merged_response)

        # Assign zpId from URL
        mapped_data['zpId'] = target_url.split('/')[-1]
        
        return mapped_data
    else:
        print("Failed to extract data")
    
    return None

if __name__ == "__main__":
    target_url = "https://www.redfin.com/IL/Chicago/7304-S-Union-Ave-60621/home/13917057"

    output = scrape_url(target_url)

    print(scrape_url(output))

    # target_urls = [
    #     "https://www.redfin.com/IL/Chicago/11540-S-Racine-Ave-60643/home/13065504",
    #     "https://www.redfin.com/IL/Chicago/5360-N-Lowell-Ave-60630/unit-502/home/12796131",
    #     "https://www.redfin.com/IL/Chicago/1464-S-Michigan-Ave-60605/unit-810/home/39570556",
    #     "https://www.redfin.com/IL/Chicago/1000-W-Adams-St-60607/unit-523/home/12693733",
    #     "https://www.redfin.com/IL/Chicago/1400-E-55th-Pl-60637/unit-409S/home/13944752",
    #     "https://www.redfin.com/IL/Chicago/1014-N-Milwaukee-Ave-60642/unit-2/home/183843738",
    #     "https://www.redfin.com/IL/Chicago/2757-N-Kenmore-Ave-60614/home/195877755",
    #     "https://www.redfin.com/IL/Chicago/3342-S-Aberdeen-St-60608/home/190326005",
    #     "https://www.redfin.com/IL/Chicago/1704-N-Springfield-Ave-60647/home/13420238",
    #     "https://www.redfin.com/IL/Chicago/3524-N-Lawndale-Ave-60618/unit-1G/home/195113312",
    #     "https://www.redfin.com/IL/Chicago/11633-S-Parnell-Ave-60628/home/13062498",
    #     "https://www.redfin.com/IL/Chicago/5031-W-Byron-St-60641/home/13460937",
    #     "https://www.redfin.com/IL/Chicago/300-W-Grand-Ave-60654/unit-403/home/12787927",
    #     "https://www.redfin.com/IL/Chicago/7734-S-Saginaw-Ave-60649/home/13216869",
    #     "https://www.redfin.com/IL/Chicago/330-N-Jefferson-St-60661/unit-1002/home/12599519",
    #     "https://www.redfin.com/IL/Chicago/7303-N-Campbell-Ave-60645/unit-A/home/13601636",
    #     "https://www.redfin.com/IL/Chicago/1550-N-Lake-Shore-Dr-60610/unit-9F/home/14126666",
    #     "https://www.redfin.com/IL/Chicago/1511-W-Superior-St-60642/home/183788886",
    #     "https://www.redfin.com/IL/Chicago/8039-S-Ingleside-Ave-60619/home/13223813",
    #     "https://www.redfin.com/IL/Chicago/1058-W-105th-St-60643/home/13076165",
    #     "https://www.redfin.com/IL/Chicago/9323-S-Normal-Ave-60620/home/13106602",
    #     "https://www.redfin.com/IL/Chicago/7304-S-Union-Ave-60621/home/13917057",
    #     "https://www.redfin.com/IL/Chicago/6748-N-Greenview-Ave-60626/unit-2/home/12597517",
    #     "https://www.redfin.com/IL/Chicago/6147-N-Harding-Ave-60659/home/13518393",
    #     "https://www.redfin.com/IL/Chicago/718-N-Avers-Ave-60624/home/13262814",
    #     "https://www.redfin.com/IL/Chicago/505-N-Lake-Shore-Dr-60611/unit-5201/home/14096574",
    #     "https://www.redfin.com/IL/Chicago/7517-N-Oketo-Ave-60631/home/13651123",
    #     "https://www.redfin.com/IL/Chicago/1823-N-Lincoln-Park-W-60614/home/13344646",
    #     "https://www.redfin.com/IL/Chicago/7019-N-Ridge-Blvd-60645/unit-3B/home/13571303",
    #     "https://www.redfin.com/IL/Chicago/8743-S-Constance-Ave-60617/home/13117838",
    #     "https://www.redfin.com/IL/Chicago/401-N-Wabash-Ave-60611/unit-54E/home/18905779",
    #     "https://www.redfin.com/IL/Chicago/2540-W-Diversey-Ave-60647/unit-404/home/26805752",
    #     "https://www.redfin.com/IL/Chicago/7944-S-Talman-Ave-60652/home/13963581",
    #     "https://www.redfin.com/IL/Chicago/5820-S-Sangamon-St-60621/home/13940159",
    #     "https://www.redfin.com/IL/Chicago/220-S-Oakley-Blvd-60612/home/195438004",
    #     "https://www.redfin.com/IL/Chicago/222-S-Oakley-Blvd-60612/unit-2/home/195437886",
    #     "https://www.redfin.com/IL/Chicago/222-S-Oakley-Blvd-60612/unit-3/home/195437954",
    #     "https://www.redfin.com/IL/Oak-Lawn/11025-S-Kolmar-Ave-60453/home/13150650",
    #     "https://www.redfin.com/IL/Chicago/1201-S-Prairie-Ave-60605/unit-1505/home/13136545",
    #     "https://www.redfin.com/IL/Chicago/7440-S-Ingleside-Ave-60619/home/13921342",
    #     "https://www.redfin.com/IL/Chicago/9439-S-Racine-Ave-60620/home/194890407",
    #     "https://www.redfin.com/IL/Chicago/1345-S-Wabash-Ave-60605/unit-1008/home/167695181",
    #     "https://www.redfin.com/IL/Chicago/401-N-Wabash-Ave-60611/unit-42E/home/39565474",
    #     "https://www.redfin.com/IL/Chicago/2853-W-40th-St-60632/home/192434343",
    #     "https://www.redfin.com/IL/Chicago/500-W-Superior-St-60654/unit-805/home/195918980",
    #     "https://www.redfin.com/IL/Chicago/6436-N-Lehigh-Ave-60646/unit-2N/home/18919312",
    #     "https://www.redfin.com/IL/Chicago/3400-W-Lake-St-60624/home/13260230",
    #     "https://www.redfin.com/IL/Chicago/400-E-Ohio-St-60611/unit-2901/home/14097350",
    #     "https://www.redfin.com/IL/Chicago/3450-S-Halsted-St-60608/unit-308/home/26822052",
    #     "https://www.redfin.com/IL/Franklin-Park/9036-Walnut-Ave-60131/home/13533892",
    #     "https://www.redfin.com/IL/Chicago/201-E-Chestnut-St-60611/unit-3C/home/14116345",
    #     "https://www.redfin.com/IL/Chicago/340-E-Randolph-St-60601/unit-4703/home/26794935",
    #     "https://www.redfin.com/IL/Chicago/2177-N-Merrimac-Ave-60639/home/12562460",
    #     "https://www.redfin.com/IL/Chicago/4335-W-Fullerton-Ave-60639/home/13423363",
    #     "https://www.redfin.com/IL/Chicago/340-E-Randolph-St-60601/unit-1304/home/26814914",
    #     "https://www.redfin.com/IL/Chicago/5839-S-Newland-Ave-60638/home/13999565",
    #     "https://www.redfin.com/IL/Chicago/4241-W-Walton-St-60651/home/13282759",
    #     "https://www.redfin.com/IL/Chicago/10918-S-Ridgeway-Ave-60655/home/13153111",
    #     "https://www.redfin.com/IL/Chicago/6758-W-64th-Pl-60638/unit-13/home/13997124",
    #     "https://www.redfin.com/IL/River-Grove/3161-Paris-Ave-60171/unit-104/home/13536538",
    #     "https://www.redfin.com/IL/Chicago/7559-S-Michigan-Ave-60619/home/13919418",
    #     "https://www.redfin.com/IL/Chicago/1735-S-Desplaines-St-60616/home/183701545",
    #     "https://www.redfin.com/IL/Chicago/235-W-Van-Buren-St-60607/unit-4302/home/113098126",
    #     "https://www.redfin.com/IL/Chicago/7828-S-Escanaba-Ave-60649/home/13216262",
    #     "https://www.redfin.com/IL/Chicago/4728-S-Evans-Ave-60615/home/13952513",
    #     "https://www.redfin.com/IL/Chicago/5823-S-Francisco-Ave-60629/home/14015485",
    #     "https://www.redfin.com/IL/Chicago/5648-S-California-Ave-60629/home/14014633",
    #     "https://www.redfin.com/IL/Chicago/7854-S-South-Shore-Dr-60649/unit-306/home/13215324",
    #     "https://www.redfin.com/IL/Chicago/519-S-Maplewood-Ave-60612/unit-4S/home/12668946",
    #     "https://www.redfin.com/IL/Chicago/9329-S-Wentworth-Ave-60620/home/13106348",
    #     "https://www.redfin.com/IL/Chicago/2821-N-Orchard-St-60657/unit-5/home/195913305",
    #     "https://www.redfin.com/IL/Chicago/2821-N-Orchard-St-60657/unit-4/home/195913298",
    #     "https://www.redfin.com/IL/Chicago/2821-N-Orchard-St-60657/unit-3/home/195913295",
    #     "https://www.redfin.com/IL/Chicago/2821-N-Orchard-St-60657/unit-2/home/195913291",
    #     "https://www.redfin.com/IL/Chicago/1560-N-Sandburg-Ter-60610/unit-2506J/home/14116718",
    #     "https://www.redfin.com/IL/Chicago/5635-S-May-St-60621/home/13941584",
    #     "https://www.redfin.com/IL/Chicago/2821-N-Orchard-St-60657/unit-1/home/195913272",
    #     "https://www.redfin.com/IL/Chicago/555-W-Cornelia-Ave-60657/unit-1906/home/13375647",
    #     "https://www.redfin.com/IL/Chicago/910-S-Michigan-Ave-60605/unit-1805/home/12657963",
    #     "https://www.redfin.com/IL/Chicago/4419-S-Wallace-St-60609/home/195913017",
    #     "https://www.redfin.com/IL/Evergreen-Park/2946-W-102nd-St-60805/home/13161957",
    #     "https://www.redfin.com/IL/Chicago/7224-N-Claremont-Ave-60645/unit-F1/home/193657338",
    #     "https://www.redfin.com/IL/Chicago/9616-S-Claremont-Ave-60643/home/13099838",
    #     "https://www.redfin.com/IL/Chicago/7943-S-Vernon-Ave-60619/home/13224492",
    #     "https://www.redfin.com/IL/Chicago/7227-S-Paulina-St-60636/home/13910710",
    #     "https://www.redfin.com/IL/Chicago/1112-N-Monitor-Ave-60651/home/195912446",
    #     "https://www.redfin.com/IL/Chicago/6341-N-Lowell-Ave-60646/home/13514660",
    #     "https://www.redfin.com/IL/Chicago/1751-W-21st-Pl-60608/home/14086868",
    #     "https://www.redfin.com/IL/Chicago/854-E-82nd-St-60619/unit-G/home/12588584",
    #     "https://www.redfin.com/IL/Chicago/6301-N-Sheridan-Rd-60660/unit-14E/home/13413820",
    #     "https://www.redfin.com/IL/Chicago/6204-N-Claremont-Ave-60659/unit-3/home/12589827",
    #     "https://www.redfin.com/IL/Chicago/1636-W-Huron-St-60622/home/14104075",
    #     "https://www.redfin.com/IL/Chicago/6301-N-Sheridan-Rd-60660/unit-22N/home/13412389",
    #     "https://www.redfin.com/IL/Chicago/Undisclosed-address-60652/home/13966407",
    #     "https://www.redfin.com/IL/Chicago/1047-W-Monroe-St-60607/unit-2/home/21992676",
    #     "https://www.redfin.com/IL/Chicago/2316-W-Cortez-St-60622/unit-G/home/12638091",
    #     "https://www.redfin.com/IL/Chicago/501-W-60th-Pl-60621/unit-3/home/12643875",
    #     "https://www.redfin.com/IL/Chicago/6254-N-Richmond-St-60659/unit-1/home/18949033",
    #     "https://www.redfin.com/IL/Chicago/1070-W-15th-St-60608/unit-403/home/12588525",
    #     "https://www.redfin.com/IL/Chicago/431-E-87th-St-60619/home/13112287",
    #     "https://www.redfin.com/IL/Chicago/11739-S-Indiana-Ave-60628/home/39947422",
    # ]

    # output = []insp


    # for idx, target in enumerate(target_urls):
    #     print(f"[{idx}] Processing: {target}")
    #     url_data = scrape_url(target)
    #     url_data['url'] = target

    #     output.append(url_data)

    
    with open("redfin_data_sample.json", 'w') as f:
        json.dump(output, f)