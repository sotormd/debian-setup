#!/usr/bin/env python3

"""
setup a debian box
"""

import os
import json
import argparse
from setup import SetupAgent


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="setup a debian box")
    parser.add_argument("config")

    args = parser.parse_args()

    config_path = args.config

    assert os.path.isfile(config_path)

    with open(config_path, encoding="utf-8") as file:
        config = json.load(file)

    sa = SetupAgent(config)
    sa.setup()
