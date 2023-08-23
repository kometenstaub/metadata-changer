#!/usr/bin/env python3
import os, frontmatter, yaml, re
from typing import TypedDict

try:
    from yaml import CSafeDumper as SafeDumper
except ImportError:
    from yaml import SafeDumper

from frontmatter import YAMLHandler


class Config(TypedDict):
    keys: list
    path: str
    exclude: str
    convert_inline: bool


global dict_keys

# Hacky stuff from https://stackoverflow.com/questions/47542343/how-to-print-a-value-with-double-quotes-and-spaces-in-yaml
def mk_double_quote(dumper, data):
    if data in dict_keys:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='')
    else:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')


SafeDumper.add_representer(str, mk_double_quote)


def get_config() -> Config:
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
                                convert_inline(post, keys)
                        if len(post.keys()) > 0:
                            with open(normalised_path, "w") as f:
                                global dict_keys
                                dict_keys = set(post.keys())
                                f.write(frontmatter.dumps(post))
        print("Done!")
    else:
        print("Set a vault path and/or add a key!")


def convert_inline(post: frontmatter.Post, keys: list):
    content = post.content
    lines = content.split("\n")
    indices = []
    for index, line in enumerate(lines):
        inline = line.find("::")
        if inline > 0:
            raw_key = line[:inline]
            raw_value = line[inline + 2:]
            excluded_chars = "[]{}*-_># " # may need fine-tuning
            new_key = raw_key.strip(excluded_chars)
            match = re.findall(r"(\[\[.+?]])", raw_value)
            if len(match) > 0 and new_key in keys:
                indices.append(index)
                current_value = post.get(new_key)
                new_values = []
                if current_value:
                    if isinstance(current_value, str):
                        new_values.append(current_value)
                    elif isinstance(current_value, list):
                        for value in current_value:
                            new_values.append(value)
                for el in match:
                    new_values.append(el)
                post.__setitem__(new_key, new_values)
                print("Fixed inline key: '" + new_key + "' with value(s): '" + ", ".join(match) + "'")
    if len(indices) > 0:
        new_indices = reversed(indices)
        for index in new_indices:
            lines.pop(index)
            post.content = "\n".join(lines)


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


if __name__ == "__main__":
    main()
