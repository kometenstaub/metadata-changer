**Disclaimer: This has not been properly tested, make sure to have backups, use version control and test it on a test vault first.**

1. Create a YAML config file `config.yml` (see example below)
2. `pip3 install -r requirements.txt`
3. Set the values for the keys and the vault path.
4. `./main.py`

Example config:


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
