import json

def sort_json_by_id(input_file, output_file):
    # Load JSON data from the input file
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Sort the list of objects by "id"
    sorted_data = sorted(data, key=lambda x: x['id'])
    
    # Write the sorted data to the output file
    with open(output_file, 'w') as f:
        json.dump(sorted_data, f, indent=2)
    
    print(f"Sorted data has been saved in '{output_file}'.")

if __name__ == '__main__':
    # Paths to the input and output files
    input_json = "items_en.json"   # Adjust the path to the input JSON file here
    output_json = "items_en_sorted.json" # Adjust the desired path for the sorted output here
    
    sort_json_by_id(input_json, output_json)
