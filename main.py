import os
import sys
import json
from datetime import datetime
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
        f.write(f"```\n{tree_structure}```\n\n")

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
            f.write(f"```\n{content}\n```\n\n")  # Ensure newline before closing triple backticks

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <project_directory>")
        sys.exit(1)

    project_directory = os.path.abspath(sys.argv[1].replace("\\", "/"))
    if not os.path.isdir(project_directory):
        print(f"Error: {project_directory} is not a valid directory.")
        sys.exit(1)

    config_file = "config.json"
    config = load_config(config_file)

    # Create the output directory if it doesn't exist
    output_directory = os.path.join(os.getcwd(), "data/output")
    os.makedirs(output_directory, exist_ok=True)

    # Generate the output file name
    timestamp = datetime.now().strftime("%y%m%d%H%M")
    project_name = os.path.basename(project_directory)
    output_md_file = os.path.join(output_directory, f"{timestamp}_{project_name}_summary.md")

    write_project_tree_summary(project_directory, output_md_file, config)
    write_file_contents(project_directory, output_md_file, config)

    print(f"Summary generated and saved to {output_md_file}")
