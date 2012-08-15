This is the Cottage Labs website. It requires python 2.7, so you should specify 
that in your virtualenv if necessary:

virtualenv -p python2.7 cl --no-site-packages

cd cl
mkdir src
cd src

Then you should clone this repo. It includes submodules, so after cloning you should:

cd cl

git submodule update --init

(if it fails, just go into cl/static/vendor and yank out facetview and jtedit, 
then clone them directly instead)

http://github.com/okfn/facetview

http://github.com/CottageLabs/jtedit

This repo is also used to track sysadmin issues. see the issue tracker for things tagged "admin"


