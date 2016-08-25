# Consensus
A customized Twitter to deal with social dilemmas. Work initiated at CERN laboratory (Geneva, Switzerland).

INSTRUCTIONS:
-> The /venv directory is for a Python 3 virtual environment (the file requirements.txt exists already in order to create this environment)

-> The API has several python files, the central one is 'app.py', the others are imported
To run app.py:
> source venv/bin/activate
> python app.py
API will then be active at localhost, port 5000

-> The database is neo4j, I have version 2.1  (old, to be updated)
Inside the /bin directory of the package, do
> ./neo4j start
Database will be active

