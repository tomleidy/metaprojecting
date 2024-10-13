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

storage = {}
files_list = []
directories_list = []
project_roots_paths = set()
project_roots_list = set()

# TODO: Implement ignore files

def get_hash(file_path) -> str:
    with open(file_path, "rb") as file:
        filehash = hashlib.file_digest(file, "sha256").hexdigest()
    return filehash


def get_file_metadata(file_path):
    # pylint: disable=W0641
    if os.path.islink(file_path):
        return None
    relative_path = os.path.relpath(os.path.abspath(file_path), CODING_DIR)
    timestamp = os.path.getmtime(file_path)
    sha256sum = get_hash(file_path)
    filename = os.path.basename(file_path)
    size = os.path.getsize(file_path)
    subdirectories = 0
    is_project = False # most likely, a lone file not a project
    git_status = subprocess.check_output(COMMAND_DETERMINE_GIT_STATUS + (file_path,)).decode("utf-8")
    file_dict = {key: value for key, value in locals().items() if key in FILE_METADATA}
    #print(file_dict)
    return file_dict


def get_git_root_of_directory(directory):
    if os.path.islink(directory):
        return None
    for x in Path(directory).parents:
        if x in project_roots_paths:
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


def iterate_through_directory(directory):
    start_time = time.time()
    for root, dirs, files in os.walk(directory,topdown=True):
        dirs[:] = [d for d in dirs if d not in DIRECTORIES_DO_NOT_RECURSE_INTO]
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            dir_git_root = get_git_root_of_directory(dir_path)
            if dir_git_root:
                project_roots_list.append(dir_git_root)
        for file in files:
            if file in DELETE_FILES:
                print(f"removing {file}")
                #os.remove(file)
            file_path = os.path.join(root, file)
            file_dict = get_file_metadata(file_path)
            if file_dict:
                files_list.append(file_dict)
    write_json("storage.json", files_list, directories_list, project_roots_list)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"get_git_root_of_directory execution time: {execution_time:.6f} seconds")

def iterate_through_projects(projects):
    for project in projects:
        status = get_git_status_of_directory(project)
        if status:
            print(f"\t{project}:\n{status}")

def get_storage_dict(files, dirs, project_roots_list) -> dict:
    storate_dict = {
                    "timestamp": time.time(),
                    "files_list": files,
                    "directories_list": dirs,
                    "project_roots_list": project_roots_list
                    }
    return storate_dict

storage_keys = ["files_list", "directories_list", "project_roots_list"]

def set_storage_variables_from_saved_dict(data):
    for key, value in data.items():
        if key in storage_keys:
            if isinstance([key], set):
                [key] = set(value)
            else:
                [key] = value
    for x in storage_keys:
        print([x])
    #return data

def write_json(filename, files, directories, projects):
    data = get_storage_dict(files, directories, projects)
    file_path = os.path.join(JSON_DIR, filename)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def read_json(filename):
    file_path = os.path.join(JSON_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8") as f:
            return json.load(f)
    return None


if __name__ == "__main__":
    read_json("storage.json")
    if len(project_roots_list) == 0:
        iterate_through_directory(CODING_DIR)
    else:
        print("loaded JSON successfully, skipping iterating through directories")
    iterate_through_projects(project_roots_list)