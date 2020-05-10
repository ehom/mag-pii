import json

def save_as_json(obj, filepath):
    def date_comparator(item):
        return item['updatedAt']

    # TODO: locate folder for data/scan_history/
    with open(filepath, 'w') as file_handle:
        obj.sort(key=date_comparator, reverse=True)
        json.dump(obj, file_handle, indent=4)


def save_as_json_hash_table(obj, filename):
    # TODO: locate for data/scan_history/
    with open(filename, 'w') as file_handle:
        hash_table = {
            item['name']: item for item in obj
        }
        json.dump(hash_table, file_handle, indent=4)
