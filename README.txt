There are a few things that you need to do after doing changes to the application.
# the first is to update the git repository using the git commands: 
git status      #This gives you the status of your git repository
git add --all     #This adds all the changes you made in your local repository and gets them readt to commit
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



##########################################################
Flask stuff
##########################################################

# To set environment variables on the bash terminal, use the export trigger like:
export FLASK_APP=app.py   # app.py is a file on the root directory.
export FLASK_ENV=development  # This will allow you to run the server in development mode and the debug mode on, It is very helpful when making changes to the application and wanting to see the changes without having to restart the server.

# To start the server we use command:
flask run

#To kill the server you use CRT + C 

# all HTML files live in templates, all javascripts files live in static, including images and CSS stuff.



#08/08/2022

I need to work on the page that is going to display the data from energy checks views.
From there I need to complete the photon_energy TRS-398 model and move on to the electrons model

<!--<div class="w3-row">
            <p>
              Determin K<sub>pol</sub>. <br />
              <i>Reversing the elevtrometer polarity as defined in TRS-398</i>
            </p>
          </div>
          <div class="w3-row">
            <div class="w3-col m6 l6">{{form.m31_reading.label}}</div>
            <div class="w3-col m6 l6">{{form.m31_reading(size=24)}}</div>
          </div>
          <div class="w3-row">
            {% for error in form.m31_reading.errors %}
            <span style="color: red">{{error}}</span>
            {%endfor%}
          </div>

          <div class="w3-row">
            <div class="w3-col m6 l6">{{form.m32_reading.label}}</div>
            <div class="w3-col m6 l6">{{form.m32_reading(size=24)}}</div>
          </div>
          <div class="w3-row">
            {% for error in form.m32_reading.errors %}
            <span style="color: red">{{error}}</span>
            {%endfor%}
          </div> -->
