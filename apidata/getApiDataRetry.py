import requests
import json
import time
import multiprocessing

def fetch_item_data(item_ids, cat_type, result_list, error_list, process_id):
    base_url = "https://api.guildwars2.com/v2/"
    retry_delay = 5  # Wartezeit in Sekunden bei Fehlern

    item_data = []
    error_data = []
    for item_id in item_ids:
        try:
            response = requests.get(base_url + cat_type + "/" + str(item_id))
            if response.status_code in (429, 502):
                print(f"Prozess {process_id}: Too many requests. Warte {retry_delay} Sekunden und versuche es erneut.")
                time.sleep(retry_delay)
                response = requests.get(base_url + cat_type + "/" + str(item_id))  # Erneuter Versuch
 
            response.raise_for_status()
            item_json = response.json()

            item_data.append({
                "name": item_json.get("name"),
                "id": item_json.get("id"),
                "chat_link": item_json.get("chat_link")
            })

            print(f"Prozess {process_id} hat Item {item_id} verarbeitet")

        except requests.exceptions.RequestException as e:
            error_data.append({
                "id": item_id,
                "error_code": response.status_code if response is not None else "N/A",
                "process_id": process_id
            })
            print(f"Prozess {process_id}: Fehler beim Abruf von Item {item_id}: {e}")

    result_list.extend(item_data)
    error_list.extend(error_data)


def getCategories(cat_type, resume_from=None):
    base_url = "https://api.guildwars2.com/v2/"
    output_file = f"{cat_type}.json"
    error_output_file = f"errors_{cat_type}.txt"

    try:
        response = requests.get(base_url + cat_type)
        response.raise_for_status()
        item_ids = response.json()

        # Wenn resume_from gesetzt ist, filtere die IDs
        if resume_from is not None:
            item_ids = [item_id for item_id in item_ids if item_id >= resume_from]
            print(f"Verarbeite nur Items ab ID {resume_from} ({len(item_ids)} Items)")

        # Aufteilen der item_ids in gleich große Chunks
        cpu_count = multiprocessing.cpu_count()
        chunk_size = max(1, len(item_ids) // cpu_count)
        item_id_chunks = [item_ids[i:i + chunk_size] for i in range(0, len(item_ids), chunk_size)]

        processes = []
        result_list = multiprocessing.Manager().list()
        error_list = multiprocessing.Manager().list()

        for i, chunk in enumerate(item_id_chunks):
            process = multiprocessing.Process(target=fetch_item_data, args=(chunk, cat_type, result_list, error_list, i))
            processes.append(process)
            process.start()
            print(f"Prozess {i} gestartet")

        for process in processes:
            process.join()

        combined_results = list(result_list)
        combined_errors = list(error_list)
        combined_results.sort(key=lambda x: x["id"])

        # Schreibe Ergebnisse in JSON-Datei
        with open(output_file, "w") as f:
            json.dump(combined_results, f, indent=2)
        print(f"Data written to {output_file}")

        # Schreibe Fehler in Fehlerdatei
        with open(error_output_file, "w") as err_f:
            json.dump(combined_errors, err_f, indent=2)
        print(f"Errors written to {error_output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen von {cat_type}: {e}")


def fetch_single_item(item_id, cat_type, retry_delay=5):
    """
    Versucht, ein einzelnes Item so lange abzurufen, bis der Request erfolgreich war.
    """
    base_url = "https://api.guildwars2.com/v2/"
    while True:
        try:
            response = requests.get(base_url + cat_type + "/" + str(item_id))
            if response.status_code in (429, 502):
                print(f"Item {item_id}: Too many requests (Status {response.status_code}). Warte {retry_delay} Sekunden...")
                time.sleep(retry_delay)
                continue
            response.raise_for_status()
            item_json = response.json()
            # Überprüfen, ob das Objekt sinnvoll ist (hier: es muss einen Namen und eine ID haben)
            if item_json.get("name") and item_json.get("id"):
                return {
                    "name": item_json.get("name"),
                    "id": item_json.get("id"),
                    "chat_link": item_json.get("chat_link")
                }
            else:
                print(f"Item {item_id}: Unvollständige Daten. Erneuter Versuch...")
                time.sleep(retry_delay)
        except requests.exceptions.RequestException as e:
            print(f"Item {item_id}: Exception {e}. Warte {retry_delay} Sekunden und versuche es erneut...")
            time.sleep(retry_delay)


def retry_failed_items(cat_type, error_file="errors_items.txt", output_file="items_retry_success.json"):
    """
    Liest die Fehlerdatei, versucht jeden fehlerhaften API-Request erneut abzurufen und speichert die erfolgreichen Ergebnisse.
    """
    try:
        with open(error_file, "r") as f:
            error_items = json.load(f)
    except Exception as e:
        print(f"Fehler beim Laden der Fehlerdatei: {e}")
        return

    successful_results = []

    for error_obj in error_items:
        item_id = error_obj.get("id")
        print(f"Versuche, Item {item_id} erneut abzurufen...")
        result = fetch_single_item(item_id, cat_type)
        if result:
            successful_results.append(result)
            print(f"Item {item_id} erfolgreich abgerufen.")
        else:
            print(f"Item {item_id} konnte nach mehrfachen Versuchen nicht abgerufen werden.")

    # Schreibe die erfolgreich abgerufenen Items in eine neue JSON-Datei
    try:
        with open(output_file, "w") as f:
            json.dump(successful_results, f, indent=2)
        print(f"Erfolgreiche Wiederholungen in {output_file} gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern der Ergebnisse: {e}")


def main():
    # Ursprüngliche Datenabfrage (ggf. Resume-Funktion nutzen)
    catType = "items"
    #resume_id = None  # Beispiel: setze hier eine Resume-ID, wenn nötig
    #getCategories(catType, resume_from=resume_id)

    # Ausführung der Retry-Funktion für fehlerhafte IDs
    retry_failed_items(catType, error_file="errors_" + catType + ".txt", output_file= catType + "_retry_success.json")


if __name__ == '__main__':
    main()
