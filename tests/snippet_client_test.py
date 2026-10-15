# Copyright 2026 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for snippet_uiautomator.snippet_client."""

from unittest import mock

from mobly.controllers.android_device_lib import adb
from snippet_uiautomator import snippet_client


def _make_client():
  client = snippet_client.SnippetClient.__new__(snippet_client.SnippetClient)
  client.user_args = ['--user', '0']
  client.package = 'com.google.android.mobly.snippet.uiautomator'
  client.host_port = 12345
  client._device = mock.Mock()
  client._adb = mock.Mock()
  client.close_connection = mock.Mock()
  client.start_server = mock.Mock()
  client.make_connection = mock.Mock()
  return client


@mock.patch.object(snippet_client, '_list_occupied_adb_ports', return_value=[])
def test_restart_snippet_connection_clears_package(_):
  client = _make_client()

  client._restart_snippet_connection()

  client._adb.shell.assert_called_once_with(
      ['pm', 'clear', '--user', '0', client.package]
  )
  client.start_server.assert_called_once_with()
  client.make_connection.assert_called_once_with()


@mock.patch.object(snippet_client, '_list_occupied_adb_ports', return_value=[])
def test_restart_snippet_connection_tolerates_pm_clear_failure(_):
  client = _make_client()
  client._adb.shell.side_effect = adb.AdbError(
      cmd=['pm', 'clear'], stdout=b'', stderr=b'Failed\n', ret_code=1
  )

  client._restart_snippet_connection()

  client._device.log.warning.assert_called_once()
  client.start_server.assert_called_once_with()
  client.make_connection.assert_called_once_with()
