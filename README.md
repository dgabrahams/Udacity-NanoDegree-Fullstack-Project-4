# Udacity Fullstack Nano Degree - Project 4

### Overview
---

The instructions in this readme will get a copy of the project up and running on a local machine for development and testing purposes.

### Prerequisites
---

It is assumed that an active connection to the internet will be available at all times. To run this program Python is required, plus access to Terminal (MAC Linux) or Command Prompt (Windows). Also required is that a web browser be installed.

### MAC AND WINDOWS

To determine whether you have Python installed, open the Terminal application, type the following, and press Return:
```
python -V
```

This command will report the version of Node:
```
Python 2.7.15
```

If your machine does not recognise the node command, then you might need to install it.
```
https://wiki.python.org/moin/BeginnersGuide/Download
```

To determine whether you have GIT installed, open the Terminal application, type the following, and press Return:
```
git --version
```

This command will report the version:
```
git version 2.15.1 (Apple Git-101)
```

If your machine does not recognise the command, then you might need to install it.
```
https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
```

### INSTALL AND RUN
---

To install the application, assuming that the required prerequisite software is installed, use GIT to clone the repository using a terminal console.

Clone: https://github.com/dgabrahams/Udacity-NanoDegree-Fullstack-Project-4.git

To clone run:
```
git clone https://github.com/dgabrahams/Udacity-NanoDegree-Fullstack-Project-4.git
```

It should build into your current working folder, and produce an output similar to that found below:
```
Cloning into 'Udacity-NanoDegree-Fullstack-Project-4'...
remote: Enumerating objects: 2202, done.
remote: Counting objects: 100% (2202/2202), done.
remote: Compressing objects: 100% (1797/1797), done.
remote: Total 2202 (delta 377), reused 2197 (delta 372), pack-reused 0
Receiving objects: 100% (2202/2202), 7.40 MiB | 1.18 MiB/s, done.
Resolving deltas: 100% (377/377), done.
Checking out files: 100% (2128/2128), done.
```

Navigate into the newly created 'Udacity-NanoDegree-Fullstack-Project-4' folder:
```
cd Udacity-NanoDegree-Fullstack-Project-4
```

Navigate into the newly the workspace folder:
```
cd sqlalchemy-workspace
```

Activate the Python Virtual environment:
```
source bin/activate
```

Navigate back one level:
```
cd ..
```

Create the database:
```
python category_database_setup.py
```

Populate the database:
```
python category_populate.py
```

Start the webservice:
```
python categoryapp_webserver.py
```

Open browser and navigate to;
```
http://localhost:8000/
```

### License
---

This project is licensed under the MIT License.

### Acknowledgments
---
