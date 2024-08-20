import shutil
import os

from gencontent import generate_page_recursive

dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def copy_static(source, destination):
    file_list = []

    # Recursion function to get file paths
    def copy_static_recur(current_source):
        source_directory = os.listdir(current_source)
        for item in source_directory:
            item_path = os.path.join(current_source, item)
            if os.path.isfile(item_path):
                file_list.append(item_path)
            else:
                copy_static_recur(item_path)

    # Getting source file paths
    copy_static_recur(source)
    source_file_list = file_list

    if os.path.exists(destination):
        file_list = []
        copy_static_recur(destination)

    destination_file_list = file_list.copy()
    if destination_file_list == source_file_list:
        print("No files deleted. Destination did not previously exist")
    else:
        shutil.rmtree(destination)
        print(destination)
        print(f"these are the files that were deleted:\n{destination_file_list}")

    # Creating destination list
    new_dest_list = source_file_list.copy()
    for i in range(len(new_dest_list)):
        new_dest_list[i] = new_dest_list[i].replace(source, destination)

    # Creating folders for destination and copying
    for dest in range(len(new_dest_list)):
        folders = new_dest_list[dest].split("/")
        path = ""
        for folder in folders[0:-1]:
            path = os.path.join(path, folder)
            if os.path.exists(folder):
                continue
            else:
                os.mkdir(path)
        shutil.copy(source_file_list[dest], new_dest_list[dest])

    return


def main():
    print("Copying static files to public directory...")
    copy_static("static", "public")

    print("Generating page...")
    generate_page_recursive(dir_path_content, template_path, dir_path_public)


main()
