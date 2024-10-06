import os

def GetFilesInDirectory(directory):
    paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            paths.append(file_path)
    # print(paths)
    return paths