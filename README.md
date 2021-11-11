# Adamant

## Prerequisite

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Python v3.8.5](https://www.python.org/downloads/)
- [PIP](https://pip.pypa.io/en/stable/cli/pip_install/)


## Setup

### Clone

```
git clone git@github.com:akintaylor/adamant.git
```

### Environment

Create a virtual environment:
```
python3 -m venv venvironment
```

Activate the environment:
```
source venvironment/bin/activate
```

Upgrade the package installer for Python:
```
pip install --upgrade pip
```

Install the dependencies:
```
pip install -r requirements.txt
```

Deactivating the environment:
```
deactivate
```


## Run

By default `Adamant` is configured to run on OpenStack's Nova project

```
python3 run.py
```


## Output

### Logs

Logs showing a list of the 12 most active modules in the nova sub-directory by commit and churn.

### Directories

images - contains two bar-charts showing the number of for each module.
repos - contains repositories being pulled by Adamant.

```
  ├── adamant
  │   ├── .images/
  │   ├── .repos/
  │   ├── adamant
  │   │   ├── __init__.py
  │   ├── . . .
```

## **- How to run `Adamant` on other repositories**
NOTE; You can test this in the `run.py` file

Create an instance of `Adamant`
```
adamant = Adamant(owner='Python-World', repo='python-mini-projects')

adamant.most_active_modules_by_commits_in_directory_from_last_six_months(directory_name='projects')

adamant.most_active_modules_by_churn_in_directory_from_last_six_months(directory_name='projects')

```

