# coding: utf-8
"""AK."""
import logging

from plumbum import cli, local
from plumbum.cmd import (
    gunzip, pg_isready, createdb, psql,
    dropdb, pg_restore, pg_dump, git, wget, python)
from plumbum.commands.modifiers import FG, TF, BG, RETCODE
from datetime import datetime
import os
import ConfigParser

from plumbum.commands.base import BaseCommand

from .ak_sub import AkSub, Ak

@Ak.subcommand("run")
class AkRun(AkSub):
    """Start odoo."""

    def _parse_args(self, argv):
        self.argv = argv
        argv = []
        return super(AkRun, self)._parse_args(argv)

    def main(self):
        return self._exec('odoo', self.argv)


@Ak.subcommand("console")
class AkConsole(AkSub):
    """Start a python console."""

    def main(self):
        return self._exec('bin/python_openerp')


@Ak.subcommand("upgrade")
class AkUpgrade(AkSub):
    """Upgrade odoo."""

    db = cli.SwitchAttr(
        ["d"], help="Force Database")

    def _get_log_params(self):
        config = self.parent.read_erp_config_file()
        data_dir = config.get('options', 'data_dir')
        upgrade_dir_full_path = os.path.join(data_dir, UPGRADE_LOG_DIR)
        if not os.path.exists(upgrade_dir_full_path):
            os.makedirs(upgrade_dir_full_path)
        version = open('VERSION.txt', 'r').read().strip()
        upgrade_file_path = os.path.join(
            upgrade_dir_full_path, '%s.log' % version)
        return ['--log-level', 'debug', '--log-file', upgrade_file_path]

    def main(self, *args):
        params = []
        if ENV != 'dev':
            params += self._get_log_params()
        if self.db:
            params += ['-d', self.db]
        return self._exec('bin/upgrade_openerp', params)

