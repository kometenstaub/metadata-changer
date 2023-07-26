# Metadata updater

## Introduction

This Python script is made for Breadcrumbs users.  
It does two things after you select on which `keys` it shall act:

1. It converts all the values (which need to be either a `string` or an `array`) and formats them as wikilinks.
2. If you set `convert_inline` to `true` in the config file, it will move the `[[wikilinks]]` to the frontmatter, turning them into a `list`. **Attention: This will remove anything that is not a wikilink from that value. 

**Disclaimer: I have tested this on my own vault and written it for my own use case, but have not done extensive testing. *Make sure to have backups, use version control and test it on a test vault first*.**

**Syncing tools (like Obsidian Sync) are *not* backups!**

## Shortcomings

1. It will turn nested lists of the form ``- [[link name]]`` into `- - - link name`
2. It will use single quotes instead of double quotes. You may try [this fix](https://github.com/kometenstaub/metadata-changer/pull/1), which I have not tested however.
3. The script will fail on invalid YAML which is why it is possible to exclude a path in the config file. (I personally needed this for my templates.) However, the script will show you on which file it failed.

## Usage

1. Download or clone this repository.
2. Create a YAML config file `config.yml` (see example below)
3. `pip3 install -r requirements.txt`
4. Set the desired config values.
5. Run the following in the directory where you saved/cloned this repo: 
   - Windows: `python3 main.py`
   - Linux/macOS: `./main.py` 

### Example config:


```yml
keys: ["parent"] # the YAML keys of which the values shall be transformed
vault_path: "/Users/username/vault_path/" # absolute path to your vault
exclude: "Templates" # optional, leave string empty if nothing is to be excluded, but the key needs to exist
convert_inline: false # whether to convert key:: value
```

Easy creation on Linux/macOS

```shell
cat <<< '''keys: ["parent"] # the YAML keys of which the values shall be transformed
vault_path: "/Users/username/vault_path/" # absolute path to your vault
exclude: "Templates" # optional, leave string empty if nothing is to be excluded, but the key needs to exist
convert_inline: false # whether to convert key:: value
''' > config.yml
```
