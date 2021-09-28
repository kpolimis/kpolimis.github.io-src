#!/usr/bin/env bash
BRANCH=master
TARGET_REPO=kpolimis/kpolimis.github.io
PELICAN_OUTPUT_FOLDER=output

echo -e "Testing travis-encrypt"
echo -e "$VARNAME"
echo -e "${GH_TOKEN}"

if ["$TRAVIS_PULL_REQUEST" =="false" ]; then
    echo -e "Starting to deploy to Github Pages\n"
    if ["$TRAVIS" =="true" ]; then
        git config user.email "travis@travis-ci.org"
        git config user.name "Travis"
    fi
    #using token clone gh-pages branch
#    git clone --depth 1 --quiet --branch=$BRANCH https://${GH_TOKEN}@github.com/$TARGET_REPO built_website > /dev/null
    git clone --depth 1 --quiet --branch=master https://github.com/kpolimis/$TARGET_REPO built_website > /dev/null
    #go into directory and copy data we're interested in to that directory
    cd built_website
    rsync -rv --exclude=.git  ../$PELICAN_OUTPUT_FOLDER/* .
    #add, commit and push files
    git add -f -A
    git commit -m "Travis build $TRAVIS_BUILD_NUMBER pushed to Github Pages"
    git push -fq origin $BRANCH > /dev/null
    echo -e "Deploy completed\n"
fi
