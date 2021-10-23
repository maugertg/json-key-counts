import json
import operator

from collections import Counter


def read_json(file: str):
    """Decode JSON file from disk"""

    with open(file) as filter_template:
        return json.load(filter_template)


def parse_keys_from_source_extend(json_array: list) -> list:
    """Use for loop and extend to make a list of root keys within each object in a list"""
    keys = []
    for alarm in json_array:
        keys.extend(list(alarm.keys()))
    return keys


def parse_keys_from_source(json_array: list) -> list:
    """Use comprehension make a list of root keys within each object in a list"""
    return [key for obj in json_array for key in obj.keys()]


def count_keys(key_list: list) -> dict:
    """Count the number of times each key occurs in a list return a dictionary with the count for
    each key sorted from smallest to largest count and alphabetically"""
    return dict(sorted(Counter(key_list).items(), key=operator.itemgetter(1, 0)))


def group_keys_by_count(counted_keys):
    """Group keys that occur the same number of times together in a list"""
    keys_by_count = {}
    for key, value in counted_keys.items():
        keys_by_count.setdefault(value, []).append(key)
    return keys_by_count


def print_key_values(source: dict) -> None:
    """Print the keys and values on a new line"""
    for key, value in reversed(source.items()):
        print(key, value)


def key_not_in_object(source: list, key: str, identifier: str):
    """Identify objects in source that do not contain a specified key"""
    for obj in source:
        if key not in obj.keys():
            print(obj[identifier])


def count_always_keys(keys_by_count: dict) -> int:
    """Count number of keys that occur in every object"""
    return len(keys_by_count[max(keys_by_count)])


def create_new_source_with_always_keys(
    source_json: list, counted_keys: list, key_count: int = None
) -> list:
    """Parse source JSON and remove any keys that are not in every object"""
    key_count = key_count if key_count else len(source_json)
    new_list = []
    for obj in source_json:
        stripped_obj = {}
        for key, value in sorted(obj.items()):
            if counted_keys[key] == key_count:
                stripped_obj[key] = value
        new_list.append(stripped_obj)
    return new_list


def main():
    """Main script logic"""
    events = (
        read_json("JSON/events.json").get("_embedded", {}).get("eventResources", [])
    )
    keys = parse_keys_from_source(events)
    counted_keys = count_keys(keys)
    keys_by_count = group_keys_by_count(counted_keys)
    always_key_count = count_always_keys(keys_by_count)
    new_events = create_new_source_with_always_keys(events, counted_keys)
    print(keys_by_count)


if __name__ == "__main__":
    main()
