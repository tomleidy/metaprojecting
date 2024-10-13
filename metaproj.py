"""
Gather metadata and organize personal Coding folder
"""
import os
import hashlib
import subprocess
import json
from pathlib import Path
import time
# pylint: disable=W0101,C0116,C0115,W0613

CODING_DIR = os.path.expanduser("~/Coding")
CODING_DIR_PATH = Path(CODING_DIR)
COMMAND_DETERMINE_REPO_ROOT = ("git", "rev-parse", "--show-toplevel")
COMMAND_DETERMINE_GIT_STATUS = ("git", "status", "--porcelain")

PROJECT_INDICATOR_FILES = set({
    "requirements.txt", "Pipfile", "Pipfile.lock", "pyproject.toml", "setup.py",
    "package.json", "yarn.lock", "tsconfig.json", "webpack.config.js", "babel.config.js",
    ".babelrc", ".eslintrc", ".eslintignore", "node_modules", "venv", "CMakeLists.txt",
    "Makefile", ".git", "Dockerfile", ".env", "__pycache__", ".venv", "venv-mac",
    "venv-win", "README.md", "LICENSE.md"
})

DIRECTORIES_DO_NOT_RECURSE_INTO = set({
    "node_modules", "venv", "__pycache__", ".git", "build", "dist", "docs"
})
DELETE_FILES = set({".DS_Store"})
FILE_METADATA = ["timestamp", "sha256sum", "filename", "absolute_path",
                 "relative_path", "size", "is_project", "git_status"]
JSON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/json")
JSON_FILES_LIST = "files_list.json"
JSON_DIRECTORIES_LIST = "directories_list.json"
JSON_PROJECTS_LIST = "project_roots_list.json"

storage = {}
files_list = []
directories_list = []
project_roots_paths = set()
project_roots_list = []

def get_hash(file_path) -> str:
    with open(file_path, "rb") as file:
        filehash = hashlib.file_digest(file, "sha256").hexdigest()
    return filehash


def get_file_metadata(file_path):
    # pylint: disable=W0641
    if os.path.islink(file_path):
        return None
    relative_path = os.path.relpath(os.path.abspath(file_path), CODING_DIR)
    print(relative_path)
    timestamp = os.path.getmtime(file_path)
    sha256sum = get_hash(file_path)
    filename = os.path.basename(file_path)
    size = os.path.getsize(file_path)
    file_dict = {key: value for key, value in locals().items() if key in FILE_METADATA}

    return file_dict


def get_git_root_of_directory(directory):
    if os.path.islink(directory):
        return None
    for x in Path(directory).parents:
        if x in project_roots_paths:
            return str(x)
        if x == CODING_DIR_PATH:
            break
    command = COMMAND_DETERMINE_REPO_ROOT + (directory,)
    git_root = subprocess.run(command, cwd=directory, capture_output=True, check=False)
    if git_root.returncode == 128:
        root = ""
    else:
        stdout_list = git_root.stdout.decode("utf-8").split("\n")
        project_root = str(stdout_list[0])
        project_roots_paths.add(Path(project_root))
        root = project_root
    return root


def get_git_status_of_directory(directory):
    command = COMMAND_DETERMINE_GIT_STATUS + (directory,)
    git_status = subprocess.run(command, cwd=directory, capture_output=True, check=False)
    if git_status.returncode == 0 and git_status.stdout != b"":
        stdout = git_status.stdout.decode("utf-8")
        return stdout or ""
    return None


def has_git_repo(directory):
    if not os.path.isdir(os.path.join(directory, ".git")):
        return False
    need_directories = ["objects", "refs"]
    need_files = ["HEAD", "config"]
    for directory in need_directories:
        if not os.path.isdir(os.path.join(directory, ".git", directory)):
            return False
    for file in need_files:
        if not os.path.isfile(os.path.join(directory, ".git", file)):
            return False
    return True


def has_project_indicators(directory):
    for file in os.listdir(directory):
        if file in PROJECT_INDICATOR_FILES:
            return True
    return False


def iterate_helper_directories(root, dirs):
    for directory in dirs:
        dir_info = get_folder_metadata(directory)
        if dir_info:
            directories_list.append(dir_info)
        # dir_git_root = get_git_root_of_directory(dir_path)
        # if dir_git_root:
        #    project_roots_list.append(dir_git_root)
    return


def iterate_helper_files(root, files):
    for file in files:
        if file in DELETE_FILES:
            print(f"removing {file}")
            # os.remove(file)
        file_path = os.path.join(root, file)
        file_dict = get_file_metadata(file_path)
        if file_dict:
            files_list.append(file_dict)
    return


def save_json_files():
    write_json(JSON_FILES_LIST, files_list)
    write_json(JSON_DIRECTORIES_LIST, directories_list)
    write_json(JSON_PROJECTS_LIST, project_roots_list)


def iterate_through_directory(directory):
    start_time = time.time()
    for root, dirs, files in os.walk(directory, topdown=True):
        dirs[:] = [d for d in dirs if d not in DIRECTORIES_DO_NOT_RECURSE_INTO]
        iterate_helper_directories(root, dirs)
        iterate_helper_files(root, files)
    save_json_files()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"execution time: {execution_time:.6f} seconds")


def iterate_through_projects(projects):
    return None
    for project in projects:
        status = get_git_status_of_directory(project)
        if status:
            print(f"\t{project}:\n{status}")


def write_json(filename, data):
    file_path = os.path.join(JSON_DIR, filename)
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def read_json(filename):
    file_path = os.path.join(JSON_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8") as f:
            return json.load(f)
    return None


if __name__ == "__main__":
    directories_list = read_json("directories_list.json")
    if not directories_list:
        directories_list = []
    files_list = read_json("files_list.json")
    if not files_list:
        files_list = []
    project_roots_list = read_json("project_roots_list.json")
    if not project_roots_list:
        project_roots_list = []
    if not project_roots_list or len(project_roots_list) == 0:
        iterate_through_directory(CODING_DIR)
    else:
        print("loaded JSON successfully, skipping iterating through directories")
    iterate_through_projects(project_roots_list)
