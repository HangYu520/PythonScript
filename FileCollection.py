"""
Return a list of files of a given folder
"""
import os
from Logger import Logger

def get_Allfiles(folder_path, logger = None):
    file_list = []
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            file_list.append(os.path.join(folder_path, filename))
    if logger:
        logger.info(f"read {len(file_list)} files from {folder_path}")
    return file_list

if __name__ == "__main__":
    logger = Logger()
    logger.launch()
    folder_path = "../src"
    file_list = get_Allfiles(folder_path, logger)