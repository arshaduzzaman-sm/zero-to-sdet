"""Start the app without Docker, or reset its data:

    cd practice-app
    python -m bookshelf           # start; then open http://127.0.0.1:8080
    python -m bookshelf reset     # put every database back to the seed data

With Docker:  docker compose exec app python -m bookshelf reset
"""

import logging
import os
import sys

import uvicorn

from .config import Settings
from .database import reset_data
from .guard import start_problem
from .main import create_app

USAGE = "Usage: python -m bookshelf [reset]"


def reset(settings: Settings) -> None:
    app = create_app(settings)
    reset_data(app)
    print("Done: every database is back to the seed data, and uploaded pictures are deleted.")


def main(args: list[str]) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(name)s  %(message)s")
    settings = Settings.from_env()
    if args == ["reset"]:
        reset(settings)
        return 0
    if args:
        print(USAGE, file=sys.stderr)
        return 2
    problem = start_problem(settings, dict(os.environ))
    if problem:
        print(problem, file=sys.stderr)
        return 1
    uvicorn.run(create_app(settings), host=settings.host, port=settings.port)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
