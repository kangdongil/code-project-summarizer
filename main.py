import os
import json
from utils.tree_generator import generate_project_tree
from utils.file_reader import get_file_contents

def load_config(config_file):
    default_config = {
        "exclude_extensions": ['.js'],
        "inspection_patterns": ["*.js", "lib/manifest.json"],
        "ignore_directories": ["data/"],
        "is_compact": False,
        "max_files": 4,
        "top_files": 3
    }

    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            user_config = json.load(f)
            default_config.update(user_config)
    
    return default_config

def write_project_tree_summary(root_dir, output_file, config):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("## Project Structure\n")
        tree_structure = generate_project_tree(
            root_dir, 
            exclude_extensions=config["exclude_extensions"], 
            max_files=config["max_files"], 
            top_files=config["top_files"], 
            is_compact=config["is_compact"]
        )
        f.write(f"```\n{tree_structure}```\n")

def write_file_contents(root_dir, output_file, config):
    file_contents = get_file_contents(
        root_dir, 
        config["inspection_patterns"], 
        config["ignore_directories"], 
        config["is_compact"]
    )
    with open(output_file, 'a', encoding='utf-8') as f:  # Open in append mode
        for file_path, content in file_contents.items():
            relative_path = os.path.relpath(file_path, root_dir)
            f.write(f"## {relative_path}\n")
            f.write(f"```\n{content}\n```\n")  # Ensure newline before closing triple backticks

if __name__ == "__main__":
    current_directory = os.getcwd()  # Use current working directory
    config_file = os.path.join(current_directory, "config.json")
    output_md_file = "result.md"

    config = load_config(config_file)

    write_project_tree_summary(current_directory, output_md_file, config)
    write_file_contents(current_directory, output_md_file, config)
