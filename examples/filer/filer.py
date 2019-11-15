from os import walk, rename
from os.path import sep


def print_directory(path, file_extension):
    print("\nThe following are the files in your path with the desired extension: ")
    list_of_files = []
    for root, directories, file_names in walk(path):
        for file_name in sorted(file_names):
            if file_extension in file_name:
                list_of_files.append(root + sep + file_name)
                print(root + sep + file_name)


def select_option():
    print("\nChoose one of the following options:")
    print("1. Rename with text + numbers")
    print("2. Rename a TV show")
    print("3. Add a string to the names")
    selection = input("")
    return selection


def rename_text_and_numbers(path, file_extension):
    print("You chose to rename the files with text and numbers")
    text = input("Input text: ")
    first_number = int(input("Input starting number (default 1)") or 1)
    step = int(input("Input step (default 1): ") or 1)

    for root, directories, file_names in walk(path):
        for file_name in sorted(file_names):
            if file_extension in file_name:
                rename(root + sep + file_name, root + sep + text +
                       str(first_number).zfill(4) + file_extension)
                first_number += step


def rename_tv_show(path, file_extension):
    print("You chose to rename a TV show")
    show_name = input("Name of TV show: ")
    season = input("Season: ")
    starting_chapter = int(input("Starting chapter (default 1): ") or 1)

    for root, directories, file_names in walk(path):
        for file_name in sorted(file_names):
            if file_extension in file_name:
                rename(root + sep + file_name,
                       root + sep + show_name + "_"
                       + season.zfill(2) + "x"
                       + str(starting_chapter).zfill(2)
                       + file_extension)
                starting_chapter += 1


def add_string_to_file_name(path, file_extension):
    print("You chose to add a string to a file_name: ")
    text = input("What would you like to add? ")

    for root, directories, file_names in walk(path):
        for file_name in sorted(file_names):
            if file_extension in file_name:
                rename(root + sep + file_name,
                       root + sep + file_name[:-len(file_extension)]
                       + text + file_extension)


def rename_files(selection, path, file_extension):
    if selection == "1":
        rename_text_and_numbers(path, file_extension)
    elif selection == "2":
        rename_tv_show(path, file_extension)
    elif selection == "3":
        add_string_to_file_name(path, file_extension)
    else:
        print("Sorry your selection was invalid, run the program again.")


def main():
    print("Welcome to file renamer!")
    path = input(
        "Insert the path of the folder with the files you want to rename: ")
    file_extension = input(
        "Insert the file extension of the files you want to rename: ")
    if "." not in file_extension:
        file_extension = "." + file_extension

    # print all the current files on the directory
    print_directory(path, file_extension)

    selection = select_option()
    rename_files(selection, path, file_extension)

    # print updated directory
    print_directory(path, file_extension)
    print("Done!")


if __name__ == "__main__":
    main()
