"""
Paths, folders, and filenames are stored here

"""
import os
CODING_DIR = os.path.expanduser("~/Coding/")
PROJECTS_DIR = os.path.join(CODING_DIR, "Projects/")
PROJECTS_DESCRIPTION_DIR = os.path.join(PROJECTS_DIR, "Descriptions/")

PROJECT_PATH = os.path.expanduser(PROJECTS_DIR)

DELETE_FILES = set({".DS_Store", "._.DS_Store", "Thumbs.db"})

DIRECTORIES_TO_IGNORE = set({
    ".git",
    "node_modules",
    ".vscode",
    "venv",
    ".venv",
    "venv-mac",
    "venv-win",
    "__pycache__",
    ".pytest_cache",
    "pytest_cache",
    "build",
    "dist",
    "docs",
    ".idea",
    "env",
    ".tox",
    "migrations",
    "target",
    ".coverage",
    ".gradle",
    "coverage",
    ".history",
    ".sass-cache",
    "out",
    "temp",
    "tmp"
})


FILE_METADATA = ["timestamp", "sha256sum", "filename", "absolute_path",
                 "relative_path", "size"]
JSON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/json")
JSON_DIRECTORIES_LIST = "directories_list.json"
JSON_PROJECTS_LIST = "project_roots_list.json"

SKIP_CATEGORIES = set({"Scraps", "Descriptions", "Summaries"})
