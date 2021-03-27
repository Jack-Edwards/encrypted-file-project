import os

def size_of_directory_recursive(path: str) -> int:
    size = 0
    for path, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
    return size

def bytes_remaining_in_cloud_storage(storage_path: str, bytes_allocated: int) -> int:
    bytes_in_storage = size_of_directory_recursive(storage_path)
    return bytes_allocated - bytes_in_storage

def bytes_to_nice_string(byte_count: int) -> str:
    labels = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    label_index = 0
    while (byte_count > 1024):
        byte_count /= 1024
        label_index += 1

    return f'{round(byte_count, 2)} {labels[label_index]}'
