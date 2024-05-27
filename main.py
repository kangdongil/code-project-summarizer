import os
import fnmatch

def generate_project_tree(root_dir, padding='', exclude_extensions=None, max_files=4, top_files=3):
    if exclude_extensions is None:
        exclude_extensions = []

    tree_structure = ""
    items = sorted(os.listdir(root_dir))
    extension_count = {}
    files_by_extension = {}

    for item in items:
        path = os.path.join(root_dir, item)
        ext = os.path.splitext(item)[1]
        if ext not in exclude_extensions:
            extension_count[ext] = extension_count.get(ext, 0) + 1
            if ext not in files_by_extension:
                files_by_extension[ext] = []
            files_by_extension[ext].append(item)

    skip_folder = any(count > max_files for count in extension_count.values())

    for item in items:
        path = os.path.join(root_dir, item)
        if os.path.isdir(path):
            tree_structure += f"{padding}├── {item}/\n"
            tree_structure += generate_project_tree(path, padding + "│   ", exclude_extensions, max_files, top_files)
        elif not skip_folder or os.path.splitext(item)[1] in exclude_extensions:
            tree_structure += f"{padding}├── {item}\n"

    if skip_folder:
        for ext, count in extension_count.items():
            if count > max_files:
                tree_structure += "".join(f"{padding}├── {name}\n" for name in files_by_extension[ext][:top_files])
                remaining_files = count - top_files
                tree_structure += f"{padding}├── (... with {remaining_files} more {ext} files found)\n"
                break

    return tree_structure

def get_file_contents(root_dir, patterns, ignore_dirs):
    file_contents = {}
    ignore_dirs = [os.path.abspath(ignore_dir) for ignore_dir in ignore_dirs]  # Convert to absolute paths

    for subdir, _, files in os.walk(root_dir):
        abs_subdir = os.path.abspath(subdir)
        if any(os.path.commonpath([abs_subdir, ignore_dir]) == ignore_dir for ignore_dir in ignore_dirs):
            continue
        for file in files:
            for pattern in patterns:
                if fnmatch.fnmatch(file, pattern):
                    file_path = os.path.join(subdir, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_contents[file_path] = f.read()
    return file_contents

def write_project_tree_summary(root_dir, output_file, exclude_extensions=None, max_files=4, top_files=3):
    if exclude_extensions is None:
        exclude_extensions = []

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("## Project Structure\n")
        tree_structure = generate_project_tree(root_dir, exclude_extensions=exclude_extensions, max_files=max_files, top_files=top_files)
        f.write(f"```\n{tree_structure}```\n\n")

def write_file_contents(root_dir, output_file, patterns, ignore_dirs):
    file_contents = get_file_contents(root_dir, patterns, ignore_dirs)
    with open(output_file, 'a', encoding='utf-8') as f:  # Open in append mode
        for file_path, content in file_contents.items():
            relative_path = os.path.relpath(file_path, root_dir)
            f.write(f"## {relative_path}\n")
            f.write(f"```\n{content}\n```\n\n")  # Ensure newline before closing triple backticks

if __name__ == "__main__":
    current_directory = os.getcwd()  # Use current working directory
    output_md_file = "project_structure.md"
    exclude_extensions = ['.js']  # Add extensions to exclude from skipping here
    inspection_patterns = ["*.js", "lib/manifest.json"]
    ignore_directories = ["data/"]  # Add directories to ignore here

    write_project_tree_summary(current_directory, output_md_file, exclude_extensions=exclude_extensions)
    write_file_contents(current_directory, output_md_file, inspection_patterns, ignore_directories)
