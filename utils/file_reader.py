import os
import fnmatch

def minify_code_content(content):
    lines = content.split('\n')
    minified_lines = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            minified_lines.append(stripped_line)
    return ' '.join(minified_lines)

def get_file_contents(root_dir, patterns, ignore_dirs, is_compact=False):
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
                        content = f.read()
                        if is_compact:
                            content = minify_code_content(content)
                        file_contents[file_path] = content
    return file_contents
