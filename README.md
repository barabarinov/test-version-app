# test-version-app

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pytest](https://img.shields.io/badge/pytest-003E51?style=for-the-badge&logo=pytest&logoColor=white)

This project includes a set of test cases to ensure the correct functionality of a simple versioning API. The tests are written using pytest and cover various aspects of the API, including:

- Getting status
- Setting initial status version
- Upgrade to major status version
- Update minor status version
- Rollback to previous major status version (or to specific version)
- Deleting status version

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
SERVICE_HOST=<your-host> pytest
```

> [!IMPORTANT]
> - From diagram I couln't understand is this system supports changing version on the rollback to particular one or just to previous major version. In the tests I'm testing also changing to particular version (just in case).
> 
