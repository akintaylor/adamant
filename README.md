# Adamant

## **- Prerequisite**
To have Python (v3.8.5) installed in your computer:
```
https://www.python.org/downloads/
```

## **- Clone project**
```
git clone git@github.com:akintaylor/adamant.git
```

## **- Environment setup**
Create a virtual environment:
```
python3 -m venv venvironment
```

Activate the environment:
```
source venvironment/bin/activate
```

NOTE; For deactivating the environment:
```
deactivate
```

Upgrade the package installer for Python:
```
pip install --upgrade pip
```

Install the dev dependencies:
```
pip install -r requirements.txt
```

## **- Run**
By default `Adamant` is configured to run on OpenStack's Nova project
```
python run.py
```

The following outputs are created:
- Logs showing a list of the 12 most active modules in the nova subdirectory by commit and churn.
- creates `.images` folder - contains two barcharts showing the number of for each module.
- creates `.repos` folder - contains repositories being pulled by Adamant.
