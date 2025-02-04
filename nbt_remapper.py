# This Python Program allows to easily rename resources inside a nbt file
# An example of it is the renaming of archeon:southstone to archeon:chiaspen
# This file need the "nbtlib" library to be installed (pip install nbtlib)

import nbtlib


def camel_case(string: str) -> str:
    return "".join([substring[0].upper() + substring[1:].lower() for substring in string.split("_")])


def remap(string: str, old: str, new: str) -> str:
    result = string.replace(old.lower(), new.lower()) # snake_case remapping
    result = result.replace(old.upper(), new.upper()) # UPPER_SNAKE_CASE remapping
    result = result.replace(camel_case(old), camel_case(new)) # CamelCase remapping
    return result


def process_array(array: nbtlib.tag.List, old: str, new: str) -> nbtlib.tag.List:
    result = []
    for i in range(len(array)):
        value = array[i]
        if isinstance(value, nbtlib.tag.String):
            value = nbtlib.tag.String(remap(value, old, new))
        elif isinstance(value, nbtlib.tag.List):
            value = process_array(value, old, new)
        elif isinstance(value, nbtlib.tag.Compound):
            process_compound(value, old, new)
        result.append(value)
    return nbtlib.tag.List(result)


def process_compound(compound: nbtlib.Compound, old: str, new: str):
    for key, value in filter(lambda x: isinstance(x[1], nbtlib.tag.String), compound.items()):
        value: nbtlib.tag.String
        compound[key] = nbtlib.tag.String(remap(value, old, new))
    for key, value in filter(lambda x: isinstance(x[1], nbtlib.tag.List), compound.items()):
        value: nbtlib.tag.List
        compound[key] = process_array(value, old, new)
    for key, value in filter(lambda x: isinstance(x[1], nbtlib.tag.Compound), compound.items()):
        value: nbtlib.tag.Compound
        process_compound(value, old, new)


if __name__ == '__main__':
    path = input("Please input path of the nbt to remap\n")
    current_name = input("Please input the current name (in snake case) to remap\n")
    remap_name = input("Please input the name (in snake case) you want to remap to\n")

    if input(f"Is it good?\nPath: {path}\nCurrent Name: {current_name}\nRemap Name: {remap_name}\nPress y to confirm" +
             " and any other to exit the process.\n").lower() != "y":
        exit()

    file = nbtlib.load(path)
    process_compound(file, current_name, remap_name)
    file.save()
