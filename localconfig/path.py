"""
Paths, folders, and filenames are stored here

"""
import os

PROJECTS_DIR = os.path.expanduser("~/Coding/Projects/")
PROJECTS_DESCRIPTION_DIR = os.path.expanduser("~/Coding/Projects/Descriptions")

PROJECT_PATH = os.path.expanduser(PROJECTS_DIR)

DELETE_FILES = set({".DS_Store"})

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
