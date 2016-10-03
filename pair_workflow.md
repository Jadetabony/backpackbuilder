Jack:
$ git branch pair
$ git checkout pair
# do some work
$ git add file_worked_on.py
$ git commit -m "Took over the world"
$ git push origin pair:pair
Jill:
$ git remote add jack https://github.com/jack/exercise
$ git fetch jack
$ git checkout -b pair jack/pair
# do more work
$ git add file_worked_on.py
$ git add another_file.py
$ git commit -m "Took over Mars"
$ git push origin pair:pair
Jack:
$ git remote add jill https://github.com/jill/exercise
$ git pull jill pair:pair
