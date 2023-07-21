#!/usr/bin/python3
import os, frontmatter, yaml, re
from typing import TypedDict


class Movie(TypedDict):
    keys: list
    path: str
    exclude: str
    convert_inline: bool


def get_config() -> Movie:
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f.read())
        return {
            "keys": config["keys"],
            "path": config["vault_path"],
            "exclude": config["exclude"],
            "convert_inline": config["convert_inline"]
        }


def main():
    config = get_config()
    keys = config["keys"]
    vault_path = config["path"]
    exclude = config["exclude"]
    convert = config["convert_inline"]
    if len(vault_path) > 0 and len(keys) > 0:
        for dirpath, dirnames, files in os.walk(vault_path):
            # print(f"Found directory: {dirnames}, located here:{dirpath}")
            for file_name in files:
                if file_name.endswith(".md"):
                    if (len(exclude) == 0) or (len(exclude) > 0 and exclude not in dirpath):
                        normalised_path = os.path.normpath(dirpath + "/" + file_name)
                        print(normalised_path)
                        with open(normalised_path, "r") as f:
                            post = frontmatter.load(f)
                            change_keys(post, normalised_path, keys)
                            if convert:
                                convert_inline(post)
        print("Done!")
    else:
        print("Set a vault path and/or add a key!")


def convert_inline(post: frontmatter.Post):
    content = post.content
    lines = content.split("\n")
    for index, line in enumerate(lines):
        match = re.search(r"(.*?)::\s*? (\[\[.+?]])", line)
        print(match)
        if match:
            lines.pop(index)
            key = match.group(1)
            current_value = post.get(key)
            new_values = []
            if current_value:
                if isinstance(current_value, str):
                    new_values.append(current_value)
                elif isinstance(current_value, list):
                    for value in current_value:
                        new_values.append(value)
            #post.__setitem__(key,)

def change_keys(post: frontmatter.Post, norm_path: str, keys: list):
    for key in keys:
        value = post.get(key)
        if value is not None:
            new_value = []
            if isinstance(value, list) and len(value) > 0:
                for el in value:
                    if el is not None and not isinstance(el, list) and el[0:2] != "[[":
                        new_value.append("[[" + el + "]]")
                        print("File: " + norm_path)
                        print("Fixed value: '" + el + "' of key: '" + key + "'")
                    else:
                        new_value.append(el)
            elif isinstance(value, str):
                if value[0:2] != "[[":
                    new_value.append("[[" + value + "]]")
                    print("File: " + norm_path)
                    print("Fixed value: '" + value + "' of key: '" + key + "'")
                else:
                    new_value.append(value)
            post.__setitem__(key, new_value)
    if len(post.keys()) > 0:
        with open(norm_path, "w") as f:
            f.write(frontmatter.dumps(post))


if __name__ == "__main__":
    main()
