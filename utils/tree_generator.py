import os

def generate_project_tree(root_dir, padding='', exclude_extensions=None, max_files=4, top_files=3, is_compact=False):
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
            tree_structure += f"{padding}├─ {item}/\n" if is_compact else f"{padding}├── {item}/\n"
            tree_structure += generate_project_tree(path, padding + ("│" if is_compact else "│   "), exclude_extensions, max_files, top_files, is_compact)
        elif not skip_folder or os.path.splitext(item)[1] in exclude_extensions:
            tree_structure += f"{padding}├ {item}\n" if is_compact else f"{padding}├── {item}\n"

    if skip_folder:
        for ext, count in extension_count.items():
            if count > max_files:
                tree_structure += "".join(f"{padding}├ {name}\n" if is_compact else f"{padding}├── {name}\n" for name in files_by_extension[ext][:top_files])
                remaining_files = count - top_files
                tree_structure += f"{padding}├ (... with {remaining_files} more {ext} files found)\n" if is_compact else f"{padding}├── (... with {remaining_files} more {ext} files found)\n"
                break

    return tree_structure