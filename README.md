# Skripsi

## Virtual Env
This program requires virtual env on both login website and the api you need to install virtual env on your computer by entering this on your prompt
> ```pip install virtualenv```

Then you will need to create the environment on each of the program folder

> ```virtualenv -p python3 env```

You'll first need to activate your virtual environment first! If you open your folder inside the login website folder or the api folder the visual studio code will automatically activate it. If you're on the root folder then you will need activate them manually.
Open 2 terminal, set each directory into each app then enter

> ```& ./env/scripts/activate```

to activate the environment.
Once that done now you can install the dependencies by using

> ```pip install -r requirements.txt```

on each of the app environtment. Now you should be set! run them using

> ```python app.py```
