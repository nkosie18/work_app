There are a few things that you need to do after doing changes to the application.
# the first is to uipdate the git repository using the git commands:
git status
git add --all
git commit -m "message of the changes to to be commited, give details of the changes done since the last commit"

because the application is now on heroku, the git push command will not work. instead, we need to run the:
git push heroku master  