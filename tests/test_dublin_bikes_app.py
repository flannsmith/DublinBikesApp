#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dublin_bikes_app` package."""


import unittest
from click.testing import CliRunner

from dublin_bikes_app import dublin_bikes_app
from dublin_bikes_app import cli


class TestDublin_bikes_app(unittest.TestCase):
    """Tests for `dublin_bikes_app` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'dublin_bikes_app.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
