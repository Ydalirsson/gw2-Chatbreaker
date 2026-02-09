import json


def merge_and_sort_by_id(primary_file, retry_file, output_file):
    # Load JSON data from both input files
    with open(primary_file, "r") as f:
        primary_data = json.load(f)
    with open(retry_file, "r") as f:
        retry_data = json.load(f)

    # Merge by id; retry entries overwrite primary entries if same id exists
    merged_by_id = {}
    for item in primary_data:
        item_id = item.get("id")
        if item_id is not None:
            merged_by_id[item_id] = item
    for item in retry_data:
        item_id = item.get("id")
        if item_id is not None:
            merged_by_id[item_id] = item

    # Sort the merged list of objects by "id"
    sorted_data = sorted(merged_by_id.values(), key=lambda x: x["id"])

    # Write the sorted data to the output file
    with open(output_file, "w") as f:
        json.dump(sorted_data, f, indent=2)

    print(f"Merged and sorted data saved in '{output_file}'.")


if __name__ == "__main__":
    primary_json = "items.json"
    retry_json = "items_retry_success.json"
    output_json = "items_merged_sorted.json"

    merge_and_sort_by_id(primary_json, retry_json, output_json)
