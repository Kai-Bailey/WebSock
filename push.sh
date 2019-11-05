#!/bin/sh

setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
  git remote remove origin
  git init
}

commit_website_files() {
  git status
  git add .
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
  git checkout -b gh-pages
  git remote add origin-pages https://${GH_TOKEN}@github.com/Haegi/WebSock.git > /dev/null 2>&1
  git push --quiet --set-upstream origin-pages gh-pages --force
}

setup_git
commit_website_files
upload_files