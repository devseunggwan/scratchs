# 파이썬 설치 시 의존성을 가진 라이브러리 설치
# https://devlog.jwgo.kr/2019/06/05/must-installed-lib-when-installing-python-using-pyenv/
sudo apt-get update
sudo apt-get install build-essential libffi-dev libbz2-dev zlib1g-dev libreadline-dev libsqlite3-dev
curl https://pyenv.run | bash

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Restart your shell for the changes to take effect.
# Load pyenv-virtualenv automatically by adding
# the following to ~/.bashrc:

echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

# activate bash
source ~/.bashrc