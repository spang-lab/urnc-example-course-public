#!/usr/bin/env python3
import glob
import os
import re
import shutil
import subprocess
import sys
from os.path import join, normpath, exists

root_dir = normpath(join(__file__, "..", ".."))
script_dir = join(root_dir, "scripts")
website_dir = join(root_dir, "website")

def main():
    install_dependencies()
    convert_lecture_notebooks_to_html()
    copy_html_files_to_folder_website()
    patch_img_paths_in_website()
    print_user_info()

def install_dependencies():
    print_header("CHECKING DEPENDENCIES")
    if not shutil.which("jupyter-book"):
        print('Command `jupyter-book` not available.')
        print('Trying installation via `pip install jupyter-book`.')
        subprocess.check_call(["pip", "install", "jupyter-book"])

def convert_lecture_notebooks_to_html():
    print_header("BUILDING WERBSITE IN FOLDER `LECTURES/_BUILD/HTML`")
    subprocess.check_call(["jupyter-book", "build", "lectures"])

def copy_html_files_to_folder_website():
    print_header("COPYING `./LECTURES/_BUILD/HTML/*` TO `./WEBSITE/`")
    os.makedirs(website_dir, exist_ok=True)
    shutil.copytree("lectures/_build/html", website_dir, dirs_exist_ok=True)
    if exists("images"):
        shutil.copytree("images", join(website_dir, "images"), dirs_exist_ok=True)
    # Create .nojekyll file to tell github pages this is a static website
    open(join(website_dir, ".nojekyll"), "w").close()

def patch_img_paths_in_website():
    print_header("CONVERTING LOCAL PATHS IN WEBSITE TO UNC PATHS")
    os.chdir(website_dir)
    html_files = glob.glob("**/[0-9][0-9]*.html", recursive=True)
    unc_repl = r"https://fids.git-pages.uni-regensburg.de/urnc-example-course/images/\1"
    for html_file in html_files:
        print(html_file)
        contents = open(html_file, "r").read()
        contents = re.sub(r'".*?/images/(.*?)"', unc_repl, contents)
        open(html_file, "w").write(contents)

def print_user_info():
    print_header("STATIC WEBPAGE GENERATED IN FOLDER")
    print(website_dir)
    print_header("TO VIEW, OPEN THE FOLLOWING LINK IN YOUR BROWSER")
    print(join(website_dir, "index.html").replace("/mnt/c/", "C:/"))

def print_header(*args, **kwargs):
    text = " ".join(str(arg) for arg in args)
    length = len(text) + 8
    print(f"\n{'#' * length}\n### {text} ###\n{'#' * length}\n")

if __name__ == "__main__":
    main()