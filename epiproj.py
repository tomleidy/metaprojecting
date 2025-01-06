"""
Text based utility for managing projects in a personal coding directory.

It will, as a byproduct, also delete .DS_Store files.

For example:
~/Coding/Projects/
            |--- Active/
            |      `--- favorite-project
            |--- Inactive/
            `--- Archive/


"""

import os


PROJECTS_DIR = os.path.expanduser("~/Coding/Projects/")
PROJECTS_DESCRIPTION_DIR = os.path.expanduser("~/Coding/Projects/Descriptions")
base_path = os.path.expanduser(PROJECTS_DIR)
DELETE_FILES = set({".DS_Store"})


class Project:
    def __init__(self, path: str):
        if not os.path.exists(path):
            return None
        if not os.path.isdir(path):
            return None
        self.path = path
        self.name = self.path.split("/")[-1]
        self.readme = self._does_document_exist_project_root("README")
        self.license = self._does_document_exist_project_root("LICENSE")
        self.changelog = self._does_document_exist_project_root("CHANGELOG")
        self.dotgitignore = self._does_document_exist_project_root(".gitignore")
        self.dotgit = self._does_directory_exist_in_project_root(".git")
        self.description = self._does_project_description_exist()
        self.latest_mtime = self._get_latest_mtime()
        # print(self)

    def __str__(self):
        prepared_string = f"# Project: {self.name}\n"
        prepared_string += f"## Path: {self.path}\n"
        prepared_string += f"## Git Repo: {self.dotgit}\n"
        prepared_string += f"## Project Description Exists: {self.description}\n"
        prepared_string += f"## Latest mtime: {self.latest_mtime}\n"
        # prepared_string += "## Documentation \n"
        # prepared_string += f"- README: {self.readme}\n"
        # prepared_string += f"- LICENSE: {self.license}\n"
        # prepared_string += f"- CHANGELOG: {self.changelog}\n"
        # prepared_string += f"- .gitignore: {self.dotgitignore}\n"
        # prepared_string += "\n"
        return prepared_string

    def _does_project_description_exist(self):
        desc_file_name = "DESCRIPTION-" + self.name
        path_file_name = os.path.join(PROJECTS_DESCRIPTION_DIR, desc_file_name)
        if not os.path.exists(path_file_name):
            return False
        if os.path.isfile(path_file_name):
            return True
        return True

    def _get_latest_mtime(self):
        latest_mtime = 0
        for root, files, dirs in os.walk(self.path, topdown=True):
            for x in dirs:
                if x in DIRECTORIES_TO_IGNORE:
                    dirs.remove(x)
            for x in files:
                x_path = os.path.join(root, x)
                latest_mtime = max(os.path.getmtime(x_path), latest_mtime)
        return latest_mtime

    def _does_directory_exist_in_project_root(self, directory_name):
        path_and_directory = os.path.join(self.path, directory_name)
        if not os.path.exists(path_and_directory):
            return False
        if os.path.isdir(path_and_directory):
            return True
        return False

    def _does_document_exist_project_root(self, document: str):
        base_filename = ""
        if document.endswith(".txt") or document.endswith(".md"):
            base_filename = document.split(".")[0]
        for ext in [".md", ".txt"]:
            path_and_base_filename = os.path.join(self.path, base_filename, ext)
            if not os.path.exists(path_and_base_filename):
                continue
            if os.path.isfile(path_and_base_filename):
                return path_and_base_filename
        return ""


DIRECTORIES_TO_IGNORE = set({
    "node_modules", "venv", "__pycache__", ".git", "build", "dist", "docs",
    "venv-mac", "venv-win", ".venv", ".pytest_cache", "pytest_cache",
    ".idea", ".vscode", "env", ".tox", "migrations", "target", ".coverage",
    ".gradle", "coverage", ".history", ".sass-cache", "out", "temp", "tmp"
})


FILE_METADATA = ["timestamp", "sha256sum", "filename", "absolute_path",
                 "relative_path", "size"]
JSON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/json")
JSON_DIRECTORIES_LIST = "directories_list.json"
JSON_PROJECTS_LIST = "project_roots_list.json"

SKIP_CATEGORIES = set({"Scraps", "Descriptions", "Summaries"})

projects = []


def delete_file(pathfile: str) -> None:
    if not os.path.exists(pathfile):
        return
    if not os.path.isfile(pathfile):
        return
    print(f"::: Removing {pathfile}")
    os.remove(pathfile)
    return


def get_project_category_paths() -> list:
    """Get list of category directories in projects directory"""
    categories = []
    for item in os.listdir(base_path):
        if item in SKIP_CATEGORIES:
            continue
        pathfile = os.path.join(base_path, item)
        if item in DELETE_FILES:
            delete_file(pathfile)
            continue
        if os.path.isdir(pathfile):
            categories.append(os.path.join(base_path, item))
    return categories


def get_project_class_list() -> list:
    category_paths = get_project_category_paths()
    for category in category_paths:
        project_list = []
        for item in os.listdir(category):
            pathfolder = os.path.join(category, item)
            if os.path.isdir(pathfolder):
                project_list.append(Project(pathfolder))
    return project_list


if __name__ == "__main__":
    for project in get_project_class_list():
        print(project)
