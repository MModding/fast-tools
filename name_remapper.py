# This Python Program allows to easily rename resources due to a name change
# An example of it is the renaming of archeon:southstone to archeon:chiaspen

import os


SUPPORTED_EXTENSIONS = ["txt", "md", "json", "java"]


def camel_case(string: str) -> str:
    return "".join([substring[0].upper() + substring[1:].lower() for substring in string.split("_")])


def remap(string: str, old: str, new: str) -> str:
    result = string.replace(old.lower(), new.lower()) # snake_case remapping
    result = result.replace(old.upper(), new.upper()) # UPPER_SNAKE_CASE remapping
    result = result.replace(camel_case(old), camel_case(new)) # CamelCase remapping
    return result


def process_directory(path: str, old: str, new: str):
    try:
        elements = os.scandir(path)
        for element in elements:
            if element.is_file():
                if element.name.split(".")[-1] in SUPPORTED_EXTENSIONS:
                    with open(element.path, "r", encoding = "locale") as file:
                        content = file.read()
                    with open(element.path, "w", encoding = "locale") as file:
                        file.write(remap(content, old, new))
            else:
                process_directory(element.path, old, new)
            os.rename(
                element.path,
                element.path[:len(element.path) - len(element.name)] + remap(element.name, old, new),
            )
    except OSError as err:
        print(err)


if __name__ == '__main__':
    root = input("Please input the root path where you want the process to start remapping\n")
    current_name = input("Please input the current name (in snake case) to remap\n")
    remap_name = input("Please input the name (in snake case) you want to remap to\n")

    if input(f"Is it good?\nRoot: {root}\nCurrent Name: {current_name}\nRemap Name: {remap_name}\nPress y to confirm" +
             " and any other to exit the process.\n").lower() != "y":
        exit()

    process_directory(root, current_name, remap_name)

    input("Done!\n")
