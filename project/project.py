"""
Module for Project class
"""
import os
from localconfig.path import PROJECTS_DESCRIPTION_DIR, DIRECTORIES_TO_IGNORE


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
