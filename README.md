# bwrapper
A wrapper to use the Bitwarden CLI as a git credential helper

(This project is not associated in any way with [Bitwarden](https://bitwarden.com/).)

## Requirements:
- Bitwarden CLI
- Python>=3.5

## Installation
To use this helper for the current repository,
```
git config --local credential.helper '/absolute/path/git-credential-bwrapper.py'
```
where `/absolute/path/git-credential-bwrapper.py` is the absolute path to this script.

To enable this heper globally, replace `local` by `global`.

If you are curious, you can enable debugging output by replacing `'/absolute/path/git-credential-bwrapper.py'` by `'/absolute/path/git-credential-bwrapper.py --debug'.`

Finally, make the script executable by running,
```
chmod +x /absolute/path/git-credential-bwrapper.py
```

## Usage
If it is the first time you use the Bitwarden CLI, you have to login using `bw login`, see [the official documentation](https://bitwarden.com/help/article/cli/).

At the beginning of your session, unlock your vault with,
```
bw unlock
```
and set the `BW_SESSION` environment variable as recommanded by the output of this command.

Now, when crdentials are needed to interact with a remote repository, `git` will query your crdentials from your vault using the remote URL as a search term. If no credentials are found (or an error occurs), `git` will ask for your credentials normally.

## Note
For a more practical way to unlock your vault, you can add the following alias to your `~/.bashrc`
```
alias bwunlock="source <(bw unlock | grep \"\$ export BW_SESSION=\" | cut -c 2-)"
```
