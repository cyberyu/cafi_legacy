fancy_echo() {
  printf "\n%b\n" "$1"
}

install_if_needed() {
  local package="$1"

  if [ $(dpkg-query -W -f='${Status}' "$package" 2>/dev/null | grep -c "ok installed") -eq 0 ];
  then
    sudo aptitude install -y "$package";
  fi
}

append_to_zshrc() {
  local text="$1" zshrc
  local skip_new_line="$2"

  if [[ -w "$HOME/.zshrc.local" ]]; then
    zshrc="$HOME/.zshrc.local"
  else
    zshrc="$HOME/.zshrc"
  fi

  if ! grep -Fqs "$text" "$zshrc"; then
    if (( skip_new_line )); then
      printf "%s\n" "$text" >> "$zshrc"
    else
      printf "\n%s\n" "$text" >> "$zshrc"
    fi
  fi
}

#!/usr/bin/env bash

trap 'ret=$?; test $ret -ne 0 && printf "failed\n\n" >&2; exit $ret' EXIT
set -e

if [[ ! -d "$HOME/.bin/" ]]; then
  mkdir "$HOME/.bin"
fi

if [ ! -f "$HOME/.zshrc" ]; then
  touch "$HOME/.zshrc"
fi

append_to_zshrc 'export PATH="$HOME/.bin:$PATH"'

if ! grep -qiE 'wheezy|jessie|precise|trusty' /etc/os-release; then
  fancy_echo "Sorry! we don't currently support that distro."
  exit 1
fi

fancy_echo "Updating system packages ..."
  if command -v aptitude >/dev/null; then
    fancy_echo "Using aptitude ..."
  else
    fancy_echo "Installing aptitude ..."
    sudo apt-get install -y aptitude
  fi

fancy_echo "Installing git, for source control management ..."
  install_if_needed git

sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/10gen.list
sudo apt-get update
sudo apt-get install -y mongodb-10gen

fancy_echo "Installing nvm, nodejs, npm, bower, grunt, gulp and angularjs"
sudo apt-get install -y nodejs-legacy
sudo apt-get install -y npm
sudo npm install npm -g
sudo npm install -g express bower grunt-cli gulp


fancy_echo "Installing ruby build dependencies ..."
  sudo aptitude build-dep -y ruby-full

fancy_echo "Installing libraries for common gem dependencies ..."
  sudo aptitude install -y libxslt1-dev libcurl4-openssl-dev libksba8 libksba-dev libqtwebkit-dev libreadline-dev

fancy_echo "Installing sqlite3, for prototyping database-backed rails apps"
  install_if_needed libsqlite3-dev
  install_if_needed sqlite3

fancy_echo "Installing Postgres, a good open source relational database ..."
  install_if_needed postgresql
  install_if_needed postgresql-server-dev-all

fancy_echo "Installing Redis, a good key-value database ..."
  install_if_needed redis-server

fancy_echo "Installing ctags, to index files for vim tab completion of methods, classes, variables ..."
  install_if_needed exuberant-ctags

fancy_echo "Installing vim ..."
  install_if_needed vim-gtk

fancy_echo "Installing tmux, to save project state and switch between projects ..."
  install_if_needed tmux

fancy_echo "Installing ImageMagick, to crop and resize images ..."
  install_if_needed imagemagick

fancy_echo "Installing watch, to execute a program periodically and show the output ..."
  install_if_needed watch

fancy_echo "Installing curl ..."
  install_if_needed curl

fancy_echo "Installing zsh ..."
  install_if_needed zsh


#fancy_echo "Changing your shell to zsh ..."
# chsh -s $(which zsh)

silver_searcher_from_source() {
  git clone git://github.com/ggreer/the_silver_searcher.git /tmp/the_silver_searcher
  sudo aptitude install -y automake pkg-config libpcre3-dev zlib1g-dev liblzma-dev
  sh /tmp/the_silver_searcher/build.sh
  cd /tmp/the_silver_searcher
  sh build.sh
  sudo make install
  cd
  rm -rf /tmp/the_silver_searcher
}

if ! command -v ag >/dev/null; then
  fancy_echo "Installing The Silver Searcher (better than ack or grep) to search the contents of files ..."

  if aptitude show silversearcher-ag &>/dev/null; then
    install_if_needed silversearcher-ag
  else
    silver_searcher_from_source
  fi
fi

fancy_echo "Installing Ruby 2.2"
sudo apt-add-repository -y ppa:brightbox/ruby-ng
sudo apt-get update
sudo apt-get install -y ruby2.2

fancy_echo "Updating to latest Rubygems version ..."
sudo gem update --system

fancy_echo "Installing Bundler to install project-specific Ruby gems ..."
sudo gem install bundler --no-document --pre

fancy_echo "Configuring Bundler for faster, parallel gem installation ..."
  number_of_cores=$(nproc)
  bundle config --global jobs $((number_of_cores - 1))

fancy_echo "Installing Parity, shell commands for development, staging, and production parity ..."
sudo gem install parity --no-document

fancy_echo "Installing Heroku CLI client ..."
  curl -s https://toolbelt.heroku.com/install-ubuntu.sh | sh

fancy_echo "Installing the heroku-config plugin to pull config variables locally to be used as ENV variables ..."
  heroku plugins:install git://github.com/ddollar/heroku-config.git

fancy_echo "Installing GitHub CLI client ..."
  version="$(curl https://github.com/jingweno/gh/releases/latest -s | cut -d'v' -f2 | cut -d'"' -f1)"

  if uname -m | grep -Fq 'x86_64'; then
    arch='amd64'
  else
    arch='i386'
  fi

  cd /tmp
  url="https://github.com/jingweno/gh/releases/download/v${version}/gh_${version}_${arch}.deb"
  curl "$url" -sLo gh.deb
  sudo dpkg -i gh.deb
  cd -

fancy_echo "Installing rcm, to manage your dotfiles ..."
  wget -O /tmp/rcm_1.2.3-1_all.deb https://thoughtbot.github.io/rcm/debs/rcm_1.2.3-1_all.deb
  sudo dpkg -i /tmp/rcm_1.2.3-1_all.deb
  rm -f /tmp/rcm_1.2.3-1_all.deb

fancy_echo "Installing pip, to manage python packages ..."
  sudo aptitude install -y python-pip python-dev build-essential
  sudo -H pip install --upgrade paramiko PyYAML Jinja2 httplib2 
  sudo -H pip install --upgrade pip 

fancy_echo "Installing ansible virtualenv and django ..."
  sudo -H pip install --upgrade ansible
  sudo -H pip install --upgrade virtualenv django

fancy_echo "Installing SciPy, Scientific Python stack ..."
  sudo aptitude install -y python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
