# PyLeague Soccer Simulation
PyLeague is a software simulation of a soccer championship developed using Python. The goal of PyLeague is to provide the simulation of the course of one season in a realistical league (such as Lega A).
![pyleague](https://user-images.githubusercontent.com/48762613/146046505-f49740ef-9ed6-44d7-8691-43c5d8ddcafa.png)
![Screenshot from 2021-12-14 18-11-19](https://user-images.githubusercontent.com/48762613/146046625-3e570241-98cc-4802-b589-2c17d1e56fcf.png)

## Features
* League setup with csv configuration.
* Possibility of changing the parameters of each team (_strength value_, _attack power_, _defense power_).
* Realistic outcome and score generation.
* Scores and outcomes slightly influenced by the form of the teams.
* Updated standings screen.
* (In development) Realistic outgoing of the games played in a single matchday.

## Future developments
PyLeague can be seen as a basis for creating cool projects which need the generation of realistical random soccer results.
<br>Also, it can be improved and enhanced with many other features.
<br>The next developments of PyLeague will be:
* Enhancement and improvement of the available features.
* Improvement of code documentation.
* Development of the screen for the simulation of the games minute by minute.
* Tests creation.
* Many other possibilities!

## Installing PyLeague
To install and run PyLeague just clone the project and create a specific Python environment for running/modifying PyLeague.
<br>The requirements are contained in the <code>requirements.txt</code> file.<br>
PyLeague will start after running <code>main.py</code>.

## Contributing
If you want to help me adding new features and improving PyLeague, you're welcome!<br> Just fork the project, commit your changes and create a PR.
<br>If you want you can create a new issue for the project and ask me anything related to it here on Github!
<br>When starting working to an issue, create a branch called: 
``` 
issue/{number of the issue}-{title of the issue (lowercase), separe spaces with `-`}
```
<br>I'm open to new improvements and suggestions.
<br>Class/function/method documentation is written like (this)[https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html].

### Testing
To start the automated tests run:
```
.../pyleague_soccer_simulation$ pytest
```
### Formatting
To format the code run:
```
.../pyleague_soccer_simulation$ black .
```

### Type-checking
To execute type-checking run:
```
.../pyleague_soccer_simulation$ mypy pyleague
```
<br>
Thank you and happy coding with PyLeague!
