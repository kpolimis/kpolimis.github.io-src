---
Title: make a Pelican blog
Date: 2016-3-24 17:07
Author: Kivan Polimis
Category: How-to
---

# How to setup Pelican to build a blog with Travis-CI
The goal of this post is to use Pelican, a static-blogging Python package, and Travis-CI to automatically deploy a Github-hosted blog. Your blog's url will be "username.github.io". You will need <a href = "https://github.com" target="_blank">Github</a> and <a href = "https://travis-ci.org/" target="_blanks">Travis-CI </a>accounts.
<br>
I chose to use Pelican instead of other Python alternatives after reading this <a href = "https://jakevdp.github.io/blog/2013/05/07/migrating-from-octopress-to-pelican/" target ="_blank">Jake Vanderplas post</a>. These instructions are written for Linux-based operating systems (my computer uses Linux Mint) and some workarounds may be necessary if you have another operating system to install software.
<br>

# Outline #
1. Create Github blog source repository
<br>
2. Install Pelican
<br>
3. Connect Github and Travis-CI
<br>
4. Create Github blog repository
<br>
5. Make first blog post
<br>
6. Deploy Travis-CI 
<br>

# Create Github blog source repository #
We will use two separate git repositories on Github for the source and the
built website, let's first only create the repository for the source

Login to Github and create the <username>.github.io-src repository. Initialize this repo with a README.md so you can clone immediately. The '.io-src' repository is the source repo for our Pelican blog. After you create this repository, add it as origin in your Pelican folder repository 

# Install Pelican #
~~~bash
pip install pelican
~~~ 

additional packages to install
~~~bash
pip install Markdown beautifulsoup4 typogrify Pillow webassets
~~~ 

change directory to .io-src folder

run pelican-quickstart to set up the pelican blogging platform. The screenshot below shows how to answer the quickstart questions to allow your blog to be hosted on Github.
~~~bash 
pelican-quickstart  
~~~ 
![pelican-quickstart](images/pelican-quickstart.png)  
add your github.io-src repository as the origin for your blog's folder
~~~bash 
git remote add origin <username.github.io-src>  
git init .  
git remote -v  
~~~ 

add requirements.txt for pelican blog build on Travis
~~~bash 
(echo pelican; echo Markdown; echo fabric) >> requirements.txt  
~~~

add a .travis.yml file for Travis build
nano .travis.yml
~~~bash 
branches:
  only:
  - master
language: python
python:
- 2.7
install:
- pip install -r requirements.txt --use-mirrors
script:
- make html
notifications:
  email:
    on_success: always
    on_failure: always
after_success: bash deploy.sh
after_script:
  - git config credential.helper "store --file=.git/credentials"
  - echo "https://${GH_TOKEN}:@github.com" > .git/credentials
~~~

# Connect Github and Travis-CI #
In order to create the encrypted token, you can login to the Github web interface
to get an <a href = "https://help.github.com/articles/creating-an-access-token-for-command-line-use" target ="_blank">Authentication Token</a>, and then install the travis command line tool with:  

Select your avatar in the top right of the screen  
Select settings  
Select Personal access tokens  
Select generate new token near upper right of the screen  
copy the token to a text editor  

Select your avatar in the top right of the screen again  
Select integrations  
Select Travis CI  
Add to github account and authorize application  

in the travis-ci.org webinterface
select your account name in the top right  
refresh and flick the repository switch on for your .io-src repository  

on Ubuntu you need ruby dev to install travis
~~~bash
sudo apt-get install ruby1.9.1-dev
sudo gem install travis
~~~

inside repository:
~~~bash
travis encrypt GH_TOKEN=LONGTOKENFROMGITHUB --add env.global
~~~
Will be prompted with "detected repository as <username>.<username>.github.io-src,
is this correct?"  

type yes
<br>

Then add the deploy.sh script and update the global variable with yours:
~~~bash
nano deploy.sh
#!/usr/bin/env bash
BRANCH=master
TARGET_REPO=<username/username.github.io.git>
PELICAN_OUTPUT_FOLDER=output

echo -e "Testing travis-encrypt"
echo -e "$VARNAME"

if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
    echo -e "Starting to deploy to Github Pages\n"
    if [ "$TRAVIS" == "true" ]; then
        git config --global user.email "<user_email>"
        git config --global user.name "<username>"
    fi
    #using token clone gh-pages branch
    git clone --quiet --branch=$BRANCH https://${GH_TOKEN}@github.com/
    $TARGET_REPO built_website > /dev/null
    #go into directory and copy data we're interested in to that directory
    cd built_website
    rsync -rv --exclude=.git  ../$PELICAN_OUTPUT_FOLDER/* .
    #add, commit and push files
    git add -f .
    git commit -m "Travis build $TRAVIS_BUILD_NUMBER pushed to Github Pages"
    git push -fq origin $BRANCH > /dev/null
    echo -e "Deploy completed\n"
fi
~~~

~~~bash
git pull origin master  
git status  
git add .  
git commit -m "initial commit"  
git push origin master
~~~

# Create blog repository #
Then we can create the repository that will host the actual blog:
create the <username>.github.io repository for the website (initialize with README.md for immediate cloning)

# Make a post #
you cannot run deploy.sh without an initial post

~~~bash
cd content/
touch first-post.md
~~~

use pelican command generate static pages from files in content folder
~~~bash
cd ..
pelican content
~~~

you can preview your site locally before pushing and building on Travis  
Other installation materials I've consulted suggest running the folliwng commands in a new terminal.  
~~~bash
cd output
python -m pelican.server
~~~

your site is running locally at port 8000
[http://localhost:8000/](http://localhost:8000)

commit your first post to <username>.github.io-src
~~~bash
git status
git add .
git commit -m "added first post"
git push origin master
~~~

run deploy.sh file to build your blog with Travis
~~~bash
chmod +x deploy.sh
sh deploy.sh
~~~
running sh deploy.sh creates built_website folder  
I receive an access denied/authentication error the first time deploy.sh executes  

add your <username>.github.io repository as the origin in built_website folder  
~~~bash
git remote add http https://github.com/<username>/<username>.github.io.git
git remote remove origin
git remote rename http origin
git remote -v
~~~

Github defaults to Jekyll, a Ruby package, to format static .html sites. Because our blog is formatted with Pelican, we need to add a .nojekyll file to ignore Jekyll defaults  
~~~bash
touch .nojekyll
git add .nojekyll
~~~

Commit the .nojekyll file to your .io repository
~~~bash
git commit -m "added .nojekyll file for formatting"
git push origin master
~~~

Commit the .nojekyll file and built_website folder to your <username>.github.io-src repository
<br>
~~~bash
cd ..
git status
git pull origin master
git add built_website
git commit -m "adding .nojekyll file and built_website folder"
git push origin master
~~~
now run deploy.sh to build your website on Travis
~~~bash
sh deploy.sh
~~~

Your webshite is available at "username.github.io"
<br>
<br>
Workflow for posts  
 - Write post as .md and place in content folder  
 - Run `pelican content`  
 - Add and commit new posts to .io-src repository  
 - use deploy.sh to automatically push .io-src repository and build <username>.github.io website  
<br>

# References #
1. <a href ="http://docs.getpelican.com/en/3.6.3/index.html" target="_blank">Pelican docmentation</a>
2. notions and notes setup pelican <a href = "http://www.notionsandnotes.org/tech/web-development/pelican-static-blog-setup.html" target="_blank">blog post</a>
3. <a href="http://zonca.github.io/2013/09/automatically-build-pelican-and-publish-to-github-pages.html" target="_blank">Automatically build pelican</a>with Travis CI
