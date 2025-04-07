import requests
import json
import time
import multiprocessing

def fetch_item_data(item_ids, cat_type, result_list, error_list, process_id):
    base_url = "https://api.guildwars2.com/v2/"
    retry_delay = 5  # Delay in seconds before retrying failed requests

    item_data = []
    error_data = []
    for item_id in item_ids:
        try:
            response = requests.get(base_url + cat_type + "/" + str(item_id))
            if response.status_code == 429 or response.status_code == 502:
                print(f"Too many requests. Waiting for {retry_delay} seconds before retrying.")
                time.sleep(retry_delay)
                response = requests.get(base_url + cat_type + "/" + str(item_id))  # Retry the request
 
            response.raise_for_status()
            item_json = response.json()

            item_data.append({
                "name": item_json.get("name"),
                "id": item_json.get("id"),
                "chat_link": item_json.get("chat_link")
            })

            # Print result of each API call along with process ID
            print(f"Process {process_id} processed item {item_id}")

        except requests.exceptions.RequestException as e:
            error_data.append({
                "id": item_id,
                "error_code": response.status_code,
                "process_id": process_id
            })
            print(f"Failed to fetch item {item_id}: {e}")

    result_list.extend(item_data)
    error_list.extend(error_data)

def getCategories(cat_type):
    base_url = "https://api.guildwars2.com/v2/"
    output_file = f"{cat_type}.json"
    error_output_file = f"errors_{cat_type}.txt"

    try:
        response = requests.get(base_url + cat_type)
        response.raise_for_status()
        item_ids = response.json()

        # Divide item ids into roughly equal parts for each process
        chunk_size = len(item_ids) // multiprocessing.cpu_count()
        item_id_chunks = [item_ids[i:i+chunk_size] for i in range(0, len(item_ids), chunk_size)]

        # Use multiprocessing to fetch data in parallel
        processes = []
        result_list = multiprocessing.Manager().list()
        error_list = multiprocessing.Manager().list()

        for i, chunk in enumerate(item_id_chunks):
            process = multiprocessing.Process(target=fetch_item_data, args=(chunk, cat_type, result_list, error_list, i))
            processes.append(process)
            process.start()
            print(f"Process {i} started")

        for process in processes:
            process.join()

        # Convert Manager list to regular list
        combined_results = list(result_list)
        combined_errors = list(error_list)

        # Sort combined_results by item ID
        combined_results.sort(key=lambda x: x["id"])

        # Write data to JSON file
        with open(output_file, "w") as f:
            json.dump(combined_results, f, indent=2)
        print(f"Data written to {output_file}")

        # Write errors to JSON-formatted text file
        with open(error_output_file, "w") as err_f:
            json.dump(list(combined_errors), err_f, indent=2)
        print(f"Errors written to {error_output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {cat_type}: {e}")

def main():
    getCategories("items")
    #getCategories("skills")
    #getCategories("skins")
    #getCategories("colors")
    #getCategories("traits")
    #getCategories("recipes")
    #getPois()

if __name__ == '__main__':
    main()
