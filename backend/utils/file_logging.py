def save_to_file(filename: str, content: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def append_to_log(filename: str, data: dict):
    import json
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")

def read_file(filename: str) -> str:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""
