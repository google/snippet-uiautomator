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


@pytest.mark.parametrize(
    'timeout,expected',
    [
        (888, 888),
        (123.45, 123),
        (datetime.timedelta(seconds=3), 3000),
    ],
)
def test_covert_to_millisecond_succeeds(timeout, expected):
  millisecond = utils.covert_to_millisecond(timeout)

  assert millisecond == expected


def test_get_latest_logcat_timestamp_fails():
  mock_ad = mock.Mock()
  mock_ad.adb.logcat.return_value = b''

  timestamp = utils.get_latest_logcat_timestamp(mock_ad)

  assert timestamp == ''


def test_get_latest_logcat_timestamp_succeeds():
  mock_ad = mock.Mock()
  mock_ad.adb.logcat.return_value = (
      b'09-19 04:02:11.326 30775 30775 I logbuffer_pcie0: [2224165] L0(0x11)'
  )

  timestamp = utils.get_latest_logcat_timestamp(mock_ad)

  assert timestamp == '09-19 04:02:11.326'


def test_get_uiautomator_apk_succeeds():
  expected_suffix = pathlib.Path(
      'snippet_uiautomator', 'android', 'app', 'uiautomator.apk'
  )

  uiautomator_apk = utils.get_uiautomator_apk()

  assert uiautomator_apk.endswith(str(expected_suffix))


def test_is_uiautomator_service_registered_when_not_registered():
  start_time = '09-19 04:02:11.326'
  mock_ad = mock.Mock()
  mock_ad.adb.logcat.return_value = (
      b'09-19 04:02:11.326 30775 30775 I logbuffer_pcie0: [2224165] L0(0x11)'
  )

  is_registered = utils.is_uiautomator_service_registered(mock_ad, start_time)

  assert not is_registered


def test_is_uiautomator_service_registered_when_registered():
  start_time = '09-20 17:17:19.549'
  mock_ad = mock.Mock()
  mock_ad.adb.logcat.return_value = (
      b'09-20 17:17:19.550 20159 20159 E AndroidRuntime: Caused by:'
      b' java.lang.IllegalStateException: UiAutomationService'
      b' android.accessibilityservice.IAccessibilityServiceClient$Stub$Proxy@fabaa34already'
      b' registered!\n'
  )

  is_registered = utils.is_uiautomator_service_registered(mock_ad, start_time)

  assert is_registered


def test_is_uiautomator_service_registered_when_found_old_registered_error():
  start_time = '09-20 17:17:19.551'
  mock_ad = mock.Mock()
  mock_ad.adb.logcat.return_value = (
      b'09-20 17:17:19.550 20159 20159 E AndroidRuntime: Caused by:'
      b' java.lang.IllegalStateException: UiAutomationService'
      b' android.accessibilityservice.IAccessibilityServiceClient$Stub$Proxy@fabaa34already'
      b' registered!\n'
  )

  is_registered = utils.is_uiautomator_service_registered(mock_ad, start_time)

  assert not is_registered


def test_is_uiautomator_service_registered_when_fail_to_get_logcat():
  start_time = ''
  mock_ad = mock.Mock()
  mock_ad.adb.logcat.return_value = b''

  is_registered = utils.is_uiautomator_service_registered(mock_ad, start_time)

  assert not is_registered
