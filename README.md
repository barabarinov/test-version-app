# test-varsion-app

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pytest](https://img.shields.io/badge/pytest-003E51?style=for-the-badge&logo=pytest&logoColor=white)

This project includes a set of test cases to ensure the correct functionality of a simple versioning API. The tests are written using pytest and cover various aspects of the API, including:

- Obtaining Status of Version
- Setting Initial Version
- Minor Version Update
- Major Version Update
- Removing Version
- Rollback to Previous Major Version or Specific Version


## Quick Start
Clone the repository:
```bash:
git clone https://github.com/barabarinov/test-version-app.git
```

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

Run the tests:
```bash
pytest
```

> [!IMPORTANT]
> - From diagram I can not understand is this system supports changing version on the rollback to particular one. If it is not in the future it might be supported and we can test it.
> 
