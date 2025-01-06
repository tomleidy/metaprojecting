Abandoning IDEAS.md, that was for a different vision. I've learned so much since then.

# pylint: disable=W0105
# rude of pylint to tell me my plotting below is "pointless."
"""
Let's think through this.

We want the title bar to contain the app name and the root directory (with the ~ if inside the home directory; I personally don't like to share my username with screenshots, for example). Or we could make that an option.

LOST IN THE WEEDS THERE.

We can omit the timestamp, I suppose. We can put the machine name in the top right.

STILL LOST IN THE WEEDS.

How do I want to navigate?


On load: progress bar for scanning all projects

Command line option: skip pre-scanning
- (do full scan when open when opening project)

Configuration & project information: save in PROJECT_ROOT

Status bar: available key commands from navscreen
if project selected:
- *: favorite project
- M: moves project
        in active:
            if active timeframe, confirm before moving to inactive
            to inactive if >1 week since last mtime
            to archive if >1 month since last mtime
            offer to remove symlink [also toggle to not confirm]
        in inactive/archive: move to active
- H: hide/unhide (move to hidden section)
- S: summarize project architecture
- Enter: open project (under cursor only, in case of multi-select)
- L: on active project, [offer to] symlink projects to ~/Coding
- R: rename project (and DESCRIPTION and offer to update remote origin)
- X/A/N: select (as part of multi-select), all, none (in category)
    - preserve selection even if
- C: open IDE to project (e.g., code)

if category selected:
- Enter: expand/close category

- C: config
- editor choice (vim, nano, code, cursor, etc.)
- category folders to skip
- files to delete (e.g., .DS_Store, ._.DS_Store, etc.)
- files to not scan for mtime (e.g., *.pyc) [could it be good to use .gitignore for this?]
- folders to not scan for mtime (e.g., node_modules)
- time boundaries for active / inactive / archive
- offer symlinking or ignore symlinking in ~/Coding
- [don't] ask for confirmation before adding/removing symlinks in ~/Coding



~/Coding/Projects/
[+] Active
[+] Inactive
[+] Archive

[-] Favorites:
    Active/project1
    Inactive/project4

[-] Latest:
    Active/project1
    Active/project2

[+] Hidden:

---
Expanded category

~/Coding/Projects/
[-] Active
      |--- project1 [last modified: time_since_latest_mtime]
      |--- project2
      `--- project3
[+] Inactive
[+] Archive

I need to figure out what opening a project looks like.
Project View:

# project_name:
[ ] Git repo: "Yes" or "No. Initialize?"
     |--- branch status: (eventually will figure out how to do this)
     `--- branch2 status: ... (also, the [ ] to the left of git repo will display a - or + depending on if there is a repo)
## Project Documentation
[ ] README: extension or "missing"
[ ] LICENSE: extension or "missing
[ ] CHANGELOG: extension or missing
[ ] .gitignore exists or missing
## Personal Record Keeping
[ ] DESCRIPTION-project_name: present or missing

Pressing enter on the documents will:
if extant, bring up a scrollable display of the document
if non-extant, prompt to create
-- for license, eventually have a bunch of copies of licenses somewhere to select/copy
-- have template .gitignores floating around

Pressing E on the documents will open an editor to the document.

OH. I had a weird instance where I changed the project name on Github, and the directory name locally, THEN created a project with the old name for a full stack version of the same thing. Then months later (last night), I discovered that I didn’t change the remote origin. So git was VERY angry with me.
So maybe keep track of remote origin in the git status. And if it matches and then eventually diverges from the project name… Offer to update it.



"""

