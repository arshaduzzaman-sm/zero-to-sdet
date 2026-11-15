"""Start the app without Docker:

    cd practice-app
    python -m bookshelf

Then open http://127.0.0.1:8080/docs
"""

import logging

import uvicorn

from .config import Settings
from .main import create_app


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(name)s  %(message)s")
    settings = Settings.from_env()
    uvicorn.run(create_app(settings), host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
