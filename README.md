# bwrapper
A wrapper to make the Bitwarden CLI work with `git':
- by automatically fetching credentials from your vault for repos still using password auth.
- by automatically fetching the password unlocking your RSA key for ssh repos.

(This project is not associated in any way with [Bitwarden](https://bitwarden.com/).)

## Requirements:
- Bitwarden CLI
- Python>=3.5
- setsid

## Password-based authentication
### Installation for password auth
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

### Usage
If it is the first time you use the Bitwarden CLI, you have to login using `bw login`, see [the official documentation](https://bitwarden.com/help/article/cli/).

At the beginning of your session, unlock your vault with,
```
bw unlock
```
and set the `BW_SESSION` environment variable as recommanded by the output of this command.

Now, when crdentials are needed to interact with a remote repository, `git` will query your crdentials from your vault using the remote URL as a search term. If no credentials are found (or an error occurs), `git` will ask for your credentials normally.

## SSH authentication
### Installation for password auth
Assume that the password for ssh identity is named 'RSA' in your vault. If you prefer an other name, please modify `bw_helper.sh'.

To use this helper, set 
```
[core]
    sshCommand = SSH_ASKPASS="/absolute/path/bw_helper.sh" DISPLAY=1 setsid ssh
```
in your local or global  `git config`, where `/absolute/path/git-credential-bwrapper.py` is the absolute path to the bash script. You can specify a particular ssh identity here if needed.

Finally, make the script executable by running,
```
chmod +x /absolute/path/bw_helper.sh
```

### Usage
If it is the first time you use the Bitwarden CLI, you have to login using `bw login`, see [the official documentation](https://bitwarden.com/help/article/cli/).

At the beginning of your session, unlock your vault with,
```
bw unlock
```
and set the `BW_SESSION` environment variable as recommanded by the output of this command.

Now, when a ssh key is needed to interact with a remote repository and it is not in the current identities,`git` will query the password for the key from your vault.

## Note
For a more practical way to unlock your vault, you can add the following alias to your `~/.bashrc`
```
alias bwunlock="source <(bw unlock | grep \"\$ export BW_SESSION=\" | cut -c 2-)"
```
