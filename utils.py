import json


def save_result(result: dict, filename='result'):
    with open(filename+'.json', 'w') as f:
        json.dump(result, f, indent=4)
