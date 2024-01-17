#  data_server

Current Python version is 3.11.4

Make sure you are creating a virtualenv with 3.11.4!

Using pyenv
```zsh
pyenv install -v 3.11.4

pyenv virtualenv 3.11.4
```

## Local Development
To work on your local machine, I recommend to install direnv to seemlessly activate and deactive out of virutalenv for each microservice.

```zsh
brew install direnv
```

Add to your shell configuration file
```zsh
vim ~/.zshrc

eval "$(direnv hook pyenv)"

# Go to your directory
layout pyenv 3.11.4

direnv allow

# You may need to restart your terminal or simply:
source ~/.zshrc # or ~/.zashrc etc
```
