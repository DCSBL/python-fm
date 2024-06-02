# FM: `python-fm`

Asyncio package to communicate with Flitsmeister
This package is aimed to get basic information about your Flitsmeister account.


# Usage
Instantiate the FM class and access the data.

## Installation
```bash
python3 -m pip install python-fm
```

## Example
```python
import asyncio
from flitsmeister import FM
from flitsmeister.models import Auth

async def main():
    
    async with FM() as api:
        auth = await api.login(USERNAME, PASSWORD)
        
    # - Persist auth in a file or database
    # - Create a new auth object from the persisted data
    
    auth = Auth(session_token=SESSION_TOKEN, access_token=ACCESS_TOKEN)
    async with FM(auth=auth) as api:
        print(await api.user())
        print(await api.statistics())

if __name__ == "__main__":
    asyncio.run(main())
```

# Development and contribution
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Requirements
- Python 3.9 or higher
- [Poetry](https://python-poetry.org/docs/#installing-with-pipx)

## Installation and setup
```bash
poetry install
poetry shell
pre-commit install
```

You can now start developing. The pre-commit hooks will run automatically when you commit your changes. Please note that a failed pre-commit hook will prevent you from committing your changes. This is to make sure that the code is formatted correctly and that the tests pass.
