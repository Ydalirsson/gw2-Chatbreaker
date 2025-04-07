import requests
import time
import json
import sys

def getCategories(catType, language="en", resume_from=None):
    """
    Fetch a category (e.g., "items", "skills", etc.) from the API.
    Parameters:
      - catType: category type string.
      - language: "en" (default) or "de". If "de", appends '?lang=de' to requests.
      - resume_from: an item ID to resume processing from.
    Any failed API calls are recorded in an error list and saved to errors_<catType>.json.
    """
    base_url = "https://api.guildwars2.com/v2/"
    list_url = base_url + catType
    if language == "de":
        list_url += "?lang=de"
        
    print(f"Fetching list of IDs for '{catType}' in language '{language}'...")
    res = requests.get(list_url)
    res.raise_for_status()
    list_of_ids = res.json()
    print(f"Total {catType} count: {len(list_of_ids)}")
    
    # Determine the start index if resume_from is provided.
    start_index = 0
    if resume_from is not None:
        try:
            start_index = list_of_ids.index(resume_from)
            print(f"Resuming from ID {resume_from} at index {start_index}.")
        except ValueError:
            print(f"ID {resume_from} not found in the list. Starting from the beginning.")
    
    items_data = []
    error_list = []
    
    for item_id in list_of_ids[start_index:]:
        item_url = f"{base_url}{catType}/{item_id}"
        if language == "de":
            item_url += "?lang=de"
            
        try:
            item_resp = requests.get(item_url)
            # If we hit rate limiting or a temporary error, wait and retry once.
            if item_resp.status_code in [429, 502]:
                print(f"Rate limit or temporary error (status {item_resp.status_code}) for ID {item_id}. Waiting 5 seconds and retrying...")
                time.sleep(5)
                item_resp = requests.get(item_url)
                
            item_resp.raise_for_status()
            item_json = item_resp.json()
            print(f"Status {item_resp.status_code} | {item_json}")
            item_entry = {
                "name": item_json.get("name"),
                "id": item_json.get("id"),
                "chat_link": item_json.get("chat_link")
            }
            items_data.append(item_entry)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {catType} with ID {item_id}: {e}")
            error_list.append({
                "id": item_id,
                "error": str(e),
                "url": item_url,
                "status_code": item_resp.status_code if item_resp is not None else "N/A"
            })
            continue

    # Write the successful data to file as valid JSON.
    output_filename = f"{catType}.json"
    with open(output_filename, "w") as f:
        json.dump(items_data, f, indent=2)
    print(f"Data successfully written to '{output_filename}'.")
    
    # Write errors to an error JSON file.
    error_filename = f"errors_{catType}.json"
    if error_list:
        with open(error_filename, "w") as err_f:
            json.dump(error_list, err_f, indent=2)
        print(f"Errors have been saved to '{error_filename}'.")
    else:
        print("No errors encountered while fetching data.")


def get_pois_for_continent(continent_id, error_list, language="en"):
    pois_data = []
    base_url = "https://api.guildwars2.com/v2"
    lang_suffix = "?lang=de" if language == "de" else ""
    
    try:
        regions_resp = requests.get(f"{base_url}/continents/{continent_id}/floors/1/regions{lang_suffix}")
        regions_resp.raise_for_status()
        region_ids = regions_resp.json()

        for region_id in region_ids:
            print(f"Continent {continent_id} – Region {region_id}")
            maps_resp = requests.get(f"{base_url}/continents/{continent_id}/floors/1/regions/{region_id}/maps{lang_suffix}")
            maps_resp.raise_for_status()
            map_ids = maps_resp.json()

            for map_id in map_ids:
                print(f"  → Map {map_id}")
                pois_resp = requests.get(f"{base_url}/continents/{continent_id}/floors/1/regions/{region_id}/maps/{map_id}/pois{lang_suffix}")
                pois_resp.raise_for_status()
                poi_ids = pois_resp.json()

                for poi_id in poi_ids:
                    try:
                        poi_url = f"{base_url}/continents/{continent_id}/floors/1/regions/{region_id}/maps/{map_id}/pois/{poi_id}{lang_suffix}"
                        poi_resp = requests.get(poi_url)

                        if poi_resp.status_code in [429, 502]:
                            print(f"    ✗ Error {poi_resp.status_code} for POI {poi_id} – saving error and continuing")
                            error_list.append({
                                "continent_id": continent_id,
                                "region_id": region_id,
                                "map_id": map_id,
                                "poi_id": poi_id,
                                "error_code": poi_resp.status_code
                            })
                            continue

                        poi_resp.raise_for_status()
                        poi_data = poi_resp.json()
                        if poi_data.get("name") and poi_data.get("id"):
                            pois_data.append({
                                "name": poi_data["name"],
                                "id": poi_data["id"],
                                "chat_link": poi_data.get("chat_link")
                            })
                            print(f"    ✓ {poi_data['id']} – {poi_data['name']}")
                    except Exception as e:
                        print(f"    ✗ Error loading POI {poi_id}: {e}")
                        error_list.append({
                            "continent_id": continent_id,
                            "region_id": region_id,
                            "map_id": map_id,
                            "poi_id": poi_id,
                            "error": str(e)
                        })
                        continue

    except Exception as e:
        print(f"✗ Error in continent {continent_id}: {e}")

    return pois_data


def getPois(language="en"):
    all_pois = []
    error_list = []
    for continent in [1, 2]:
        print(f"Starting continent {continent}...")
        pois = get_pois_for_continent(continent, error_list, language)
        all_pois.extend(pois)

    all_pois.sort(key=lambda x: x["id"])
    with open("pois.json", "w") as f:
        json.dump(all_pois, f, indent=2, ensure_ascii=False)
    print("\nAll POIs have been successfully written to 'pois.json'.")

    if error_list:
        with open("errors_pois.json", "w") as err_f:
            json.dump(error_list, err_f, indent=2)
        print("The POIs that encountered errors have been saved in 'errors_pois.json'.")
    else:
        print("No errors encountered while fetching POIs.")


def main():
    # Interactive selection menu
    print("Select the API call you want to perform:")
    print("1: Get Category (e.g., items, skills, skins, colors, traits, recipes)")
    print("2: Get POIs")
    choice = input("Enter choice (1 or 2): ").strip()

    # Set language: 'en' for English, 'de' for German.
    language = input("Select language ('en' for English, 'de' for German): ").strip().lower()
    if language not in ['en', 'de']:
        print("Invalid language choice. Defaulting to English.")
        language = "en"

    if choice == "1":
        catType = input("Enter the category type (e.g., items, skills, skins, colors, traits, recipes): ").strip()
        resume_str = input("Enter a resume ID (leave blank to start from the beginning): ").strip()
        resume_from = int(resume_str) if resume_str.isdigit() else None
        getCategories(catType, language, resume_from)
    elif choice == "2":
        getPois(language)
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)


if __name__ == '__main__':
    main()
