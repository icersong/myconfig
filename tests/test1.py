#!/usr/bin/env python
import os
import site
import unittest

from path import Path


class TestConfig(unittest.TestCase):
    def setUp(self):
        from myconfig import cfg_init

        self.devroot = Path(__file__).parent.parent
        self.datapath = self.devroot / "conf"
        self.pjname = "test_myconfig"
        self.userpath = Path(site.USER_BASE)
        self.pjpath = self.userpath / "share" / self.pjname
        self.pjpath.rmtree_p()
        self.datapath.copytree(self.pjpath / "conf")
        os.environ[f"{self.pjname.upper()}_MODE"] = "develop"
        cfg_init(self.pjname)

    def tearDown(self):
        for f in getattr(self, "logfiles", []):
            f.remove_p()
        self.pjpath.rmtree_p()

    def test_cfg(self):
        from myconfig import ConfigLoader

        cfg = ConfigLoader().get("config.yaml", mode=None)
        self.assertEqual(cfg["app"]["name"], "myconfig")
        cfg = ConfigLoader().get("config.yaml")
        self.assertEqual(cfg["app"]["name"], "myconfig-develop")

    def test_log(self):
        import logging

        from myconfig import log_init
        from myconfig import ConfigLoader

        log_init(mode=None)
        logging.error("test")
        cfg = ConfigLoader().get("logging.yaml", mode=None)
        log = Path(cfg["handlers"]["rolling"]["filename"])
        self.logfiles = [log]
        self.assertEqual(log.stat().st_size, 53)


if __name__ == "__main__":
    unittest.main()
