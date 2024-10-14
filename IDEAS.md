# MetaProjecting
## Purpose
Managing code is a pain. This will hopefully bridge the gap, somewhat. The idea is gather metadata about projects in the users Coding directory.

## MVP
- [ ] Checks the git status of each project folder
- [ ] Suggest making commits (pick one per day)
- [ ] Check if each repo has a remote
- [ ] If project has git, figures out if owner of ~/Coding/ is part of git history for it, sets a boolean in the dictionary for this project (owner_is_dev)
- [ ] If the project needs a README.md (or it’s >0 bytes) (not in Git tree)
- [ ] If the project needs a LICENSE.* file (if owner_is_dev) (not in Git tree)
- [ ] For folders with venv folder, it will check if there's a requirements.txt
	- [ ] If not, make one
- [ ] If the folder could be a project, pick one per day and 

# Goals
## Configuration & Identity
- [ ] Loads information from ~/Coding/.mpidentity
- [ ] Load usernames/email addresses/names belong to the person who owns ~/Coding/
- [ ] loads files/folders to ignore from ~/Coding/.mpignore like git does .gitignore)

## Reading
### Restoring
- [x] Loads previous data from JSON files
- [ ] Scans list for deviations in modification times and size, update metadata if different

### Scanning directory tree
#### Folders
- [x] List of dictionaries for folders
- [x] Folder dictionaries indicate whether it has a git repo
- [x] Folder dictionaries indicate whether it might be a project (without a repo)
- [x] Folder dictionaries indicate whether it is unlikely to be a project
- [x] Folder dictionaries record modification timestamp of folder
- [ ] A list of dir names for educational / challenge sites (to not check for repos)
#### Files
- [x] Metadata collected: relative path, modification timestamp, sha256sum, filename, size
- [ ] Figure out how to determine if file should to go scraps folder
#### Projects
- [x] List of folders containing repos

##### Aging
- [ ] latest_timestamp: timestamp of recently modified file in  project (exclusions apply)
- [ ] An configurable age limit for when a project should be considered part of
- [ ] Archived: >3 months old
- [ ] Inactive: >1 week, <3 months
- [ ] Active: <= 1 week
## Performance
- [ ] Differentiate between slow and fast metadata functions (e.g., size and mtime are way faster than sha256sum)
## Writing
- [x] Stores JSON files of metadata for files, folders, and projects
- [ ] Option to output it as XLS with files, folders, and projects on different sheets
- [ ] Or three different CSV files
- [ ] If the project isn’t maintained by the user and it’s not in the Git or External folder, offer to move it there
- [ ] If the project is in the active range, and it’s not in the active folder, offer to move it there, then offer to symlink it into ~/Coding/
- [ ] If the project is older than the archive date and it’s not in the archive folder, offer to move it there
- [ ] If the symlinked projects are in the archive range, offer to remove the symlinks
- [ ] Offer to move scraps to the scrap folder
- [ ] If it’s technically inactive but gets moved to Archived, then let it stay in Archived.
- [ ] Inactive is the in between like, updated this week and not touched in 3 months.
- [ ] I’d also like a way to have it move a project out of Archive via the command-line symlinking to it in the root coding directory.
- [ ] Challenges should be offered up in a similar way.

- [x] Python script
- [x] Iterates through folders in ~/Coding/ tree.
- [x] Store the resulting information in a list
- [x] Relative path from ~/Coding
- [x] To determine if a folder is a project, uses cues like files/folders named .git, .gitignore, node_modules, venv*, pycache (or whatever the equivalent is), package.json, package-lock.json, requirements.txt
- [x] Does not recurse into node_modules, pycache, etc., type folders
