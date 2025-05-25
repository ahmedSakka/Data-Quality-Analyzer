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
    prefix = "#" * (indent + 2)
    for key, value in d.items():
        md += f"\n{prefix} {key.replace('_', ' ').title()}\n"
        if isinstance(value, dict):
            for sub_key, sub_val in value.items():
                md += f"- **{sub_key}**: {sub_val}\n"
        elif isinstance(value, list):
            if value:
                for item in value:
                    md += f"- {item}\n"
            else:
                md += "- No items found.\n"
        else:
            md += f"- {value}\n"
    return md

def timestamp():
    return dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")