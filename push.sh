#!/bin/sh

setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
  echo -n > .gitignore
  printf '# Ignore everything\n*\n# But not these files...\n!.gitignore\n# And include directories\n!reports/**/*' >> .gitignore
}

commit_website_files() {
  git status
  git add reports
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
  git remote remove origin-pages
  git remote add origin-pages https://0f1a98b5230491c575404356efa6286c29f9077c@github.com/Haegi/WebSock.git > /dev/null 2>&1
  git push --quiet --set-upstream origin-pages gh-pages 
}

setup_git
commit_website_files
upload_files