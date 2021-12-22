%echo off
git add --all
set /p id="what changed:"
git commit -m %id%
git push
git checkout master
git merge Itumeleng
git checkout Itumeleng
set FLASK_ENV=development