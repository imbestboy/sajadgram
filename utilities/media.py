def hash_media_name(name) -> str:
    hash_dict = {
        0: "<",
        1: "p",
        2: "J",
        3: "]",
        4: "Z",
        5: "l",
        6: "I",
        7: "q",
        8: "_",
        9: "-",
    }
    hashed_name = ""
    for letter in name:
        hashed_name += hash_dict[int(letter)] if letter.isnumeric() else letter

    return hashed_name.replace(" ", "s")
