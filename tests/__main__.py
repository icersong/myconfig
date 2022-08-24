#!/usr/bin/env python
import os
import unittest

case_path = os.path.dirname(__file__)
report_path = os.path.dirname(__file__) + "/unittest_case/unittest_log"


def all_case():
    discover = unittest.defaultTestLoader.discover(
        case_path, pattern="test*.py", top_level_dir=None
    )
    return discover


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(all_case())
