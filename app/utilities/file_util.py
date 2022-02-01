import yaml
import json

def load_yaml(filepath, mode='r', encoding='utf-8'):
    with open(filepath, mode, encoding=encoding) as f:
        data = yaml.full_load(f)
        return data

def save_yaml(data, filepath, mode='w', encoding='utf-8'):
    with open(filepath, mode, encoding=encoding) as f:
        yaml.dump(data, f)

def load_json(filepath, mode='r', encoding='utf-8'):
    with open(filepath, mode, encoding=encoding) as f:
        data = json.load(f)
        return data

def save_json(data, filepath, mode='w', encoding='utf-8'):
    with open(filepath, mode, encoding=encoding) as f:
        json.dump(data, f, indent=4)
        return data