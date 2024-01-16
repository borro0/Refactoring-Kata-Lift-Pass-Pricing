# Python version of Lift Pass Pricing Kata

As with the other language versions, this exercise requires a database. There is a description in the [top level README](../README.md) of how to set up MySQL. ~~If you don't have that, this version should fall back on sqlite3, and create a local database file 'lift_pass.db' in the directory where you run the application. Unfortunately the code doesn't actually work properly with sqlite3, so you'll have to adjust the SQL statements in prices.py.~~

For this python version you will also need to install the dependencies. 

You could choose to install the dependencies in a venv (not required) like this:

    python -m venv .venv

Check the [Python documentation](https://docs.python.org/3/library/venv.html) for how to activate this environment on your platform.
For windows using powershell I had to do the following:
- Open a powershell with admin rights: Set-ExecutionPolicy -ExecutionPolicy Unrestricted
- Open terminal in vscode: .\.venv\Scripts\Activate.ps1
- Ctrl+shift+P -> Select Interpreter -> select the newly created venv: .\venv\Scripts\python.exe

Then install the requirements:

    cd python 
    python -m pip install -r requirements.txt

You can start the application like this:

    python -m lift_pass_pricing

Note there is no webpage on the default url - try this url as an example to check it's running: http://127.0.0.1:3005/prices?type=1jour

You can run the tests with pytest:

    pytest

You can run the tests from within vscode. To get line coverage in the source code, install the following extension: 
    ryanluker.vscode-coverage-gutters
