# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmpv8 import Gmp

from .. import MockConnection


class GmpCreateTagTestCase(unittest.TestCase):
    def setUp(self):
        self.connection = MockConnection()
        self.gmp = Gmp(self.connection)

    def test_create_tag_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_tag(
                name=None, resource_ids=['foo'], resource_type='task'
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_tag(
                name='', resource_ids=['foo'], resource_type='task'
            )

    def test_create_tag_missing_resource_filter_and_ids(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_tag(
                name='foo',
                resource_type='task',
                resource_filter=None,
                resource_ids=None
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_tag(
                name='foo',
                resource_type='task',
                resource_filter=None,
                resource_ids=[]
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_tag(
                name='foo',
                resource_type='task'
            )

    def test_create_tag_missing_resource_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_tag(
                name='foo',
                resource_type=None,
                resource_filter=None,
                resource_ids=['foo']
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_tag(
                name='foo',
                resource_type=None,
                resource_filter="name=foo",
                resource_ids=None
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_tag(
                name='foo',
                resource_type='',
                resource_ids=['foo']
            )

    def test_create_tag_with_resource_filter(self):
        self.gmp.create_tag(
            name='foo', resource_filter='name=foo', resource_type='task'
        )

        self.connection.send.has_been_called_with(
            '<create_tag>'
            '<name>foo</name>'
            '<resources filter="name=foo">'
            '<type>task</type>'
            '</resources>'
            '</create_tag>'
        )

    def test_create_tag_with_resource_ids(self):
        self.gmp.create_tag(
            name='foo', resource_ids=['foo'], resource_type='task'
        )

        self.connection.send.has_been_called_with(
            '<create_tag>'
            '<name>foo</name>'
            '<resources>'
            '<resource id="foo"/>'
            '<type>task</type>'
            '</resources>'
            '</create_tag>'
        )

        self.gmp.create_tag(
            name='foo', resource_ids=['foo', 'bar'], resource_type='task'
        )

        self.connection.send.has_been_called_with(
            '<create_tag>'
            '<name>foo</name>'
            '<resources>'
            '<resource id="foo"/>'
            '<resource id="bar"/>'
            '<type>task</type>'
            '</resources>'
            '</create_tag>'
        )

    def test_create_tag_with_comment(self):
        self.gmp.create_tag(
            name='foo',
            resource_ids=['foo'],
            resource_type='task',
            comment='bar'
        )

        self.connection.send.has_been_called_with(
            '<create_tag>'
            '<name>foo</name>'
            '<resources>'
            '<resource id="foo"/>'
            '<type>task</type>'
            '</resources>'
            '<comment>bar</comment>'
            '</create_tag>'
        )

    def test_create_tag_with_value(self):
        self.gmp.create_tag(
            name='foo', resource_ids=['foo'], resource_type='task', value='bar'
        )

        self.connection.send.has_been_called_with(
            '<create_tag>'
            '<name>foo</name>'
            '<resources>'
            '<resource id="foo"/>'
            '<type>task</type>'
            '</resources>'
            '<value>bar</value>'
            '</create_tag>'
        )

    def test_create_tag_with_active(self):
        self.gmp.create_tag(
            name='foo', resource_ids=['foo'], resource_type='task', active=True
        )

        self.connection.send.has_been_called_with(
            '<create_tag>'
            '<name>foo</name>'
            '<resources>'
            '<resource id="foo"/>'
            '<type>task</type>'
            '</resources>'
            '<active>1</active>'
            '</create_tag>'
        )

        self.gmp.create_tag(
            name='foo', resource_ids=['foo'], resource_type='task', active=False
        )

        self.connection.send.has_been_called_with(
            '<create_tag>'
            '<name>foo</name>'
            '<resources>'
            '<resource id="foo"/>'
            '<type>task</type>'
            '</resources>'
            '<active>0</active>'
            '</create_tag>'
        )


if __name__ == '__main__':
    unittest.main()
