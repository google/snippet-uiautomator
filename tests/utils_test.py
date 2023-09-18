# Copyright 2015 Google Inc. All Rights Reserved.
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
"""Tests for snippet_uiautomator.utils."""

import datetime
import pathlib
from unittest import mock

import pytest
from snippet_uiautomator import utils


@pytest.mark.parametrize('timeout,expected', [
  (888, 888), (123.45, 123), (datetime.timedelta(seconds=3), 3000),
])
def test_covert_to_millisecond_succeeds(timeout, expected):
  millisecond = utils.covert_to_millisecond(timeout)

  assert millisecond == expected


@mock.patch.object(utils, 'mobly_utils')
def test_get_mobly_ad_log_path_succeeds(mock_mobly_utils):
  mock_mobly_utils.abs_path.return_value = str(pathlib.Path('mock', 'path'))
  ui_snippet_client = mock.MagicMock()
  ui_snippet_client._adb.serial = '1234'  # pylint: disable=protected-access

  log_path = utils.get_mobly_ad_log_path(ui_snippet_client)

  assert log_path == pathlib.Path('mock', 'path', 'AndroidDevice1234')


def test_get_uiautomator_apk_succeeds():
  expected_suffix = pathlib.Path(
    'snippet_uiautomator', 'android', 'app', 'uiautomator.apk')

  uiautomator_apk = utils.get_uiautomator_apk()

  assert uiautomator_apk.endswith(str(expected_suffix))
