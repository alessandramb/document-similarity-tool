import os

def validate_paths(folder1, folder2):
    if not os.path.isdir(folder1):
        raise ValueError(f"Folder not found: {folder1}")
    if not os.path.isdir(folder2):
        raise ValueError(f"Folder not found: {folder2}")
    
    abs_folder1 = os.path.abspath(folder1)
    abs_folder2 = os.path.abspath(folder2)
    
    return abs_folder1, abs_folder2

def get_author_name_from_path(file_path, root_dir):
    abs_root = os.path.abspath(root_dir)
    abs_file = os.path.abspath(file_path)

    try:
        rel_path = os.path.relpath(abs_file, abs_root)
        parts = rel_path.split(os.sep)
        if parts and parts[0] != '..':
            folder_name = parts[0]
            if '_' in folder_name:
                author_name = folder_name.split('_')[0]
                if author_name:
                    return author_name
            return folder_name
    except ValueError:
        pass

    folder_name_from_file = os.path.basename(os.path.dirname(abs_file))
    if '_' in folder_name_from_file:
        author_name = folder_name_from_file.split('_')[0]
        if author_name:
            return author_name
    return folder_name_from_file
