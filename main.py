import os
import fnmatch

def generate_tree_structure(root_dir, padding='', exclude_skipping_tree=None, max_files=4, top_files=3):
    if exclude_skipping_tree is None:
        exclude_skipping_tree = []

    structure = ""
    items = sorted(os.listdir(root_dir))
    extension_count = {}
    file_list = {}

    for item in items:
        path = os.path.join(root_dir, item)
        ext = os.path.splitext(item)[1]
        if ext not in exclude_skipping_tree:
            extension_count[ext] = extension_count.get(ext, 0) + 1
            if ext not in file_list:
                file_list[ext] = []
            file_list[ext].append(item)

    skip_folder = any(count > max_files for count in extension_count.values())

    for i, item in enumerate(items):
        path = os.path.join(root_dir, item)
        if os.path.isdir(path):
            structure += f"{padding}├── {item}/\n"
            structure += generate_tree_structure(path, padding + "│   ", exclude_skipping_tree, max_files, top_files)
        elif not skip_folder or os.path.splitext(item)[1] in exclude_skipping_tree:
            structure += f"{padding}├── {item}\n"

    if skip_folder:
        for ext, count in extension_count.items():
            if count > max_files:
                structure += "".join(f"{padding}├── {name}\n" for name in file_list[ext][:top_files])
                remaining_files = count - top_files
                structure += f"{padding}├── (... with {remaining_files} more {ext} files found)\n"
                break

    return structure

def read_file_content(root_dir, patterns, ignore_paths):
    file_contents = {}
    ignore_paths = [os.path.abspath(ignore_path) for ignore_path in ignore_paths]  # Convert to absolute paths

    for subdir, _, files in os.walk(root_dir):
        abs_subdir = os.path.abspath(subdir)
        if any(os.path.commonpath([abs_subdir, ignore_path]) == ignore_path for ignore_path in ignore_paths):
            continue
        for file in files:
            for pattern in patterns:
                if fnmatch.fnmatch(file, pattern):
                    file_path = os.path.join(subdir, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_contents[file_path] = f.read()
    return file_contents

def tree_structure_summary(root_dir, output_file, exclude_skipping_tree=None, max_files=4, top_files=3):
    if exclude_skipping_tree is None:
        exclude_skipping_tree = []

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("## Project Structure\n")
        tree_structure = generate_tree_structure(root_dir, exclude_skipping_tree=exclude_skipping_tree, max_files=max_files, top_files=top_files)
        f.write(f"```\n{tree_structure}```\n\n")

def file_inspection(root_dir, output_file, list_inspection_needed, ignore_paths):
    file_contents = read_file_content(root_dir, list_inspection_needed, ignore_paths)
    with open(output_file, 'a', encoding='utf-8') as f:  # Open in append mode
        for file_path, content in file_contents.items():
            relative_path = os.path.relpath(file_path, root_dir)
            f.write(f"## {relative_path}\n")
            f.write(f"```\n{content}```\n\n")

if __name__ == "__main__":
    project_directory = os.getcwd()  # Use current working directory
    output_md_file = "project_structure.md"
    exclude_skipping_tree = ['.js']  # Add extensions to exclude from skipping here
    list_inspection_needed = ["*.js", "lib/manifest.json"]
    ignore_paths = ["data/"]  # Add paths to ignore here

    tree_structure_summary(project_directory, output_md_file, exclude_skipping_tree=exclude_skipping_tree)
    file_inspection(project_directory, output_md_file, list_inspection_needed, ignore_paths)
