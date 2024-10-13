import os
import hashlib
import subprocess
import json
from pathlib import Path

CODING_DIR = os.path.expanduser("~/Coding")
CODING_DIR_PATH = Path(CODING_DIR)
COMMAND_DETERMINE_REPO_ROOT = ("git", "rev-parse", "--show-toplevel")
COMMAND_DETERMINE_GIT_STATUS = ("git", "status", "--porcelain")

PROJECT_INDICATOR_FILES = set({"requirements.txt", "Pipfile", "Pipfile.lock", "pyproject.toml", "setup.py", "package.json", "yarn.lock", "tsconfig.json", "webpack.config.js", "babel.config.js", ".babelrc", ".eslintrc", ".eslintignore", "node_modules", "venv", "CMakeLists.txt", "Makefile", ".git", "Dockerfile", ".env", "__pycache__", ".venv", "venv-mac", "venv-win"})

DIRECTORIES_DO_NOT_RECURSE_INTO = set({"node_modules", "venv", "__pycache__", ".git", "build", "dist", "docs" })
DELETE_FILES = set({".DS_Store"})
FILE_METADATA = ["timestamp","sha256sum","filename","absolute_path","relative_path","size","is_project", "git_status", "subdirectories"]
JSON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/json")

storage = {}
files_list = []
directories_list = []
project_roots = set()
# TODO: Implement ignore files
# TODO: def get_symlink_metadata

def get_hash(file_path) -> str:
    with open(file_path, "rb") as file:
        hash = hashlib.file_digest(file, "sha256").hexdigest()
    return hash



def get_file_metadata(file_path):
    if os.path.islink(file_path):
        return None
    # get relative path from CODING_DIR
    relative_path = os.path.relpath(os.path.abspath(file_path), CODING_DIR)
    # get timestamp
    timestamp = os.path.getmtime(file_path)
    # hash file
    sha256sum = get_hash(file_path)
    # get filename
    filename = os.path.basename(file_path)
    size = os.path.getsize(file_path)
    subdirectories = 0
    is_project = False # most likely, a lone file not a project
    git_status = subprocess.check_output(COMMAND_DETERMINE_GIT_STATUS + (file_path,)).decode("utf-8")
    file_dict = {key: value for key, value in locals().items() if key in FILE_FOLDER_METADATA}
    #print(file_dict)
    return file_dict


def get_git_root_of_directory(directory):
    if os.path.islink(directory):
        return None
    for x in Path(directory).parents:
        if x in project_roots:
            return x
        if x == CODING_DIR_PATH:
            break
    command = COMMAND_DETERMINE_REPO_ROOT + (directory,)
    git_root = subprocess.run(command, cwd=directory, capture_output=True)
    if git_root.returncode == 128:
        root = ""
    else:
        stdout_list = git_root.stdout.decode("utf-8").split("\n")
        project_root = stdout_list[0]
        project_roots.add(Path(project_root))
        root = project_root
    return root


def get_git_status_of_directory(directory):
    command = COMMAND_DETERMINE_GIT_STATUS + (directory,)
    git_status = subprocess.run(command, cwd=directory, capture_output=True)
    if git_status.returncode == 0 and git_status.stdout != b"":
        stdout = git_status.stdout.decode("utf-8")
        return stdout or ""
    return None


def iterate_through_directory(directory):
    segment_count = []
    for root, dirs, files in os.walk(directory,topdown=True):
        dirs[:] = [d for d in dirs if d not in DIRECTORIES_DO_NOT_RECURSE_INTO]
        for file in files:
            if file in DELETE_FILES:
                print(f"removing {file}")
                #os.remove(file)
            file_path = os.path.join(root, file)
            file_dict = get_file_metadata(file_path)
            if file_dict:
                files_and_directories.append(file_dict)

        #for dir in dirs:
            #dir_path = os.path.join(root, dir)
            #dir_dict = get_file_metadata(dir_path)
            #files_and_directories.append(dir_dict)
    print(json.dumps(files_and_directories, indent=4))
    #print(max(segment_count))



if __name__ == "__main__":
    iterate_through_directory(CODING_DIR)