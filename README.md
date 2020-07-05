# bwrapper
A wrapper to use the Bitwarden CLI as a git credential helper

## Requirements:
- Bitwarden CLI
- Python>=3.5

## Installation
To use this helper for the current repository,
```
git config --local credential.helper '/absolute/path/git-credential-bwrapper.py'
```
To enable this heper globally, replace `local` by `global`.

## Usage
Login or unlock your vault using the Bitwarden CLI and set the `BW_SESSION` environment variable as recommanded by the Bitwarden CLI.
Then, `git` will query your usernames and passwords from your vault using the remote URL as a search term. If no credentials are found (or an error occur), `git` will ask for your credentials normally.
