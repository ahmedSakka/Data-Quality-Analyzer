import os
import json
import datetime as dt

def save_json(report: dict, output_dir: str = "reports") -> str:
    os.makedirs(output_dir, exist_ok= True)
    file_path = os.path.join(output_dir, f"report_{timestamp()}.json")
    with open(file_path, "w") as f:
        json.dump(report, f, indent=4)
    return file_path

def save_markdown(report: dict, output_dir: str = "reports") -> str:
    os.makedirs(output_dir, exist_ok= True)
    file_path = os.path.join(output_dir, f"report_{timestamp()}.md")
    with open(file_path, "w") as f:
        f.write(dict_to_markdown(report))
    return file_path

def dict_to_markdown(d: dict, indent: int = 0) -> str:
    md = ""
    for key, value in d.items():
        prefix = "#" * (indent + 2)
        md += f"\n{prefix} {key.capitalize().replace('_', ' ')}\n"
        if isinstance(value, dict):
            md += dict_to_markdown(value, indent + 1)
        else:
            md += f"- {value}\n"
    return md

def timestamp():
    return dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")