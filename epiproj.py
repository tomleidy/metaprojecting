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
from localconfig.path import SKIP_CATEGORIES
from localconfig.path import PROJECT_PATH
from localconfig.path import DELETE_FILES
from project.project import Project


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
    for item in os.listdir(PROJECT_PATH):
        if item in SKIP_CATEGORIES:
            continue
        pathfile = os.path.join(PROJECT_PATH, item)
        if item in DELETE_FILES:
            delete_file(pathfile)
            continue
        if os.path.isdir(pathfile):
            categories.append(os.path.join(PROJECT_PATH, item))
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
