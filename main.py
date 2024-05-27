import os

def generate_tree_structure(root_dir, padding=''):
    structure = ""
    items = sorted(os.listdir(root_dir))
    for i, item in enumerate(items):
        path = os.path.join(root_dir, item)
        if os.path.isdir(path):
            structure += f"{padding}├── {item}/\n"
            structure += generate_tree_structure(path, padding + "│   ")
        else:
            structure += f"{padding}├── {item}\n"
    return structure

def read_js_files(root_dir):
    js_files = {}
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.js'):
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    js_files[file_path] = f.read()
    return js_files

def create_md_file(root_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("## Project Structure\n")
        tree_structure = generate_tree_structure(root_dir)
        f.write(f"```\n{tree_structure}```\n\n")
        
        js_files = read_js_files(root_dir)
        for file_path, content in js_files.items():
            relative_path = os.path.relpath(file_path, root_dir)
            f.write(f"## {relative_path}\n")
            f.write(f"```\n{content}```\n\n")

if __name__ == "__main__":
    project_directory = os.getcwd()  # Use current working directory
    output_md_file = "project_structure.md"
    create_md_file(project_directory, output_md_file)
