#!/usr/bin/python3
import os, frontmatter

keys = [] # key names
vaultPath = "" # "absolute path to the vault"

def main():
    for dirpath, dirnames, files in os.walk(vaultPath):
        # print(f"Found directory: {dirnames}, located here:{dirpath}")
        for file_name in files:
            if file_name.endswith(".md"):
                normalised_path = os.path.normpath(dirpath + "/" + file_name)
                # print(f"Found file: {normalised_path}")
                new_post = {}
                with open(normalised_path, "r") as f:
                    post = frontmatter.load(f)
                    change_keys(post, normalised_path)
    print("Done!")


def change_keys(post: frontmatter.Post, normPath: str):
    for key in keys:
        value = post.get(key)
        if value is not None:
            newValue = []
            if isinstance(value, list) and len(value) > 0:
                for el in value:
                    if el[0:2] != "[[":
                        newValue.append("[[" + el + "]]")
                        print("File: " + normPath)
                        print("Fixed value: '" + el + "' of key: '" + key + "'")
                    else:
                        newValue.append(el)
            elif isinstance(value, str):
                if value[0:2] != "[[":
                    newValue.append("[[" + value + "]]")
                    print("File: " + normPath)
                    print("Fixed value " + el + " of key " + key)
                else:
                    newValue.append(el)
            post.__setitem__(key, newValue)
            with open(normPath, "w") as f:
                f.write(frontmatter.dumps(post))


if __name__ == "__main__":
    main()