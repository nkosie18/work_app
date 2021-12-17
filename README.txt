There are a few things that you need to do after doing changes to the application.
# the first is to uipdate the git repository using the git commands:
git status
git add --all
git commit -m "message of the changes to to be commited, give details of the changes done since the last commit"

because the application is now on heroku, the git push command will not work. instead, we need to run the:
git push heroku master. 


# To create a new branch on the git project you use the command. this will create a new branch on your local repository.
git checkout -b <name of the new branch to be created>

# To push your new branch to the remote repository you will need to run the command.
git push --set-upstream <name of repository> <name of branch>

#heroku apps have repository of heroku, so the command at the top will read:
git push --set-upstream heroku <name of breach>

# now you can make changes to your application on your local repository, add the changes to git, do a git commit and push the commit to the remote repository branch using:
git add --all
git commit -m "message of changes done"
git push heroku <name of branch>

# Remember, this will not make changes to the master branch and because the heroku application is built on the master branch, this will not trigger a new build of the application.
#If you wish to make the changes on the branch take effect on the application, you have to merg the branch with the master branch and to do this tou have to run the command.
git checkout master   #This will switch you to the master branch.
git merge <name of branch>  # This will merge your branch with master and if you run:
git push heroku master   # This will now make changes that were initially one on the branch to the master branch and trigger an new application build. now your application will have all the changes you have made on both the branch and the mater.
 