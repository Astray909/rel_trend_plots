
# Auto Plotting
**[Justin Huang](https://github.com/Astray909)**

Master Template script written in Python3

## Requirement:
1. Python 3 Environment
2. Windows NT based operating system

## Testing platform:
* Windows 10 20H2 with Anaconda

## Libaary Requirements for vanilla python
1. pandas
2. seaborn
3. matplotlib
4. numpy
5. traceback
6. tkinter

## Setup procedure:
### Recommended:
1. Launch main.py from command line
### Or alternatively: 
1. Open either anaconda prompt or anaconda powershell prompt
2. Run `python main.py` under anaconda prompt

## Features:
### Script workflow:
1. Reads filter file from shared drive and filters a local version of logger file
2. Stores filtered logger file on local harddrive
3. Reads processed test data from shared drive and stores them in a local dataframe
4. Sorts dataframe based on conditions
5. Generates box plots and stores in shared drive.

## Appendix:
1. To fetch latest build from GITHUB:
    ```
    git fetch --all; git reset --hard origin; git pull origin main
    ```
