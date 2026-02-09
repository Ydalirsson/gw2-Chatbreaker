import argparse
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


def fetch_single_item(item_id, cat_type, max_retries=5, retry_delay=5):
    """
    Versucht ein einzelnes Item mehrfach abzurufen.
    Bei unvollständigen Daten wird ebenfalls erneut versucht.
    Nach max_retries wird abgebrochen und None zurückgegeben.
    """
    base_url = "https://api.guildwars2.com/v2/"
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(base_url + cat_type + "/" + str(item_id))
            if response.status_code in (429, 502):
                last_error = f"HTTP {response.status_code}"
                print(f"Item {item_id}: Too many requests (Status {response.status_code}). Versuch {attempt}/{max_retries}. Warte {retry_delay} Sekunden...")
                time.sleep(retry_delay)
                continue
            response.raise_for_status()
            item_json = response.json()
            if item_json.get("name") and item_json.get("id"):
                return {
                    "name": item_json.get("name"),
                    "id": item_json.get("id"),
                    "chat_link": item_json.get("chat_link")
                }, None
            last_error = "Unvollständige Daten"
            print(f"Item {item_id}: Unvollständige Daten. Versuch {attempt}/{max_retries}.")
            time.sleep(retry_delay)
        except requests.exceptions.RequestException as e:
            last_error = f"RequestException: {e}"
            print(f"Item {item_id}: Exception {e}. Versuch {attempt}/{max_retries}. Warte {retry_delay} Sekunden...")
            time.sleep(retry_delay)

    return None, last_error


def _load_item_ids(input_file):
    try:
        with open(input_file, "r") as f:
            data = json.load(f)
    except Exception as e:
        raise ValueError(f"Fehler beim Laden der Input-Datei: {e}")

    if isinstance(data, list):
        if not data:
            return []
        if isinstance(data[0], dict):
            return [item.get("id") for item in data if item.get("id") is not None]
        return [item_id for item_id in data if item_id is not None]

    if isinstance(data, dict):
        if "ids" in data and isinstance(data["ids"], list):
            return [item_id for item_id in data["ids"] if item_id is not None]

    raise ValueError("Ungültiges JSON-Format. Erwartet: Liste von IDs, Liste von Objekten mit 'id' oder {'ids': [...]}") 


def retry_failed_items(cat_type, input_file, output_file, error_output_file, max_retries=5, retry_delay=5):
    """
    Liest eine JSON-Inputdatei (IDs oder Objekte mit id), versucht jedes Item erneut
    abzurufen und speichert die erfolgreichen Ergebnisse. Items mit unvollständigen
    Daten werden max_retries Mal versucht und danach übersprungen.
    """
    try:
        item_ids = _load_item_ids(input_file)
    except ValueError as e:
        print(str(e))
        return

    successful_results = []

    error_list = []

    for item_id in item_ids:
        print(f"Versuche, Item {item_id} abzurufen...")
        result, error_reason = fetch_single_item(item_id, cat_type, max_retries=max_retries, retry_delay=retry_delay)
        if result:
            successful_results.append(result)
            print(f"Item {item_id} erfolgreich abgerufen.")
        else:
            print(f"Item {item_id} konnte nach {max_retries} Versuchen nicht abgerufen werden. Überspringe.")
            error_list.append({
                "id": item_id,
                "error": error_reason or "Unbekannter Fehler",
                "attempts": max_retries
            })

    # Schreibe die erfolgreich abgerufenen Items in eine neue JSON-Datei
    try:
        with open(output_file, "w") as f:
            json.dump(successful_results, f, indent=2)
        print(f"Erfolgreiche Wiederholungen in {output_file} gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern der Ergebnisse: {e}")

    if error_list:
        try:
            with open(error_output_file, "w") as err_f:
                json.dump(error_list, err_f, indent=2)
            print(f"Fehlerliste in {error_output_file} gespeichert.")
        except Exception as e:
            print(f"Fehler beim Speichern der Fehlerliste: {e}")


def main():
    parser = argparse.ArgumentParser(description="Retry API-Calls mit JSON-Input (IDs oder Objekte mit id).")
    parser.add_argument("input_file", help="JSON-Datei mit IDs oder Objekten mit 'id'")
    parser.add_argument("--cat", default="items", help="Kategorie (z.B. items, skills)")
    parser.add_argument("--output", default=None, help="Output-Datei für erfolgreiche Items")
    parser.add_argument("--errors", default=None, help="Output-Datei für fehlgeschlagene Items")
    parser.add_argument("--max-retries", type=int, default=5, help="Maximale Versuche pro Item")
    parser.add_argument("--retry-delay", type=int, default=5, help="Wartezeit in Sekunden zwischen Versuchen")
    args = parser.parse_args()

    output_file = args.output or f"{args.cat}_retry_success.json"
    error_output_file = args.errors or f"errors_{args.cat}_retry.json"

    retry_failed_items(
        args.cat,
        input_file=args.input_file,
        output_file=output_file,
        error_output_file=error_output_file,
        max_retries=args.max_retries,
        retry_delay=args.retry_delay,
    )


if __name__ == '__main__':
    main()
