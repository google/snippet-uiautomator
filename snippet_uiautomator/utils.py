# Copyright 2023 Google Inc.
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

"""Common utils for Snippet UiAutomator."""

import datetime
import logging
import pathlib
import re
from typing import Union

from mobly import logger as mobly_logger
from mobly import utils as mobly_utils
from mobly.controllers import android_device
from mobly.controllers.android_device_lib import snippet_client_v2
from snippet_uiautomator import errors

REGEX_LOGCAT_TIMESTAMP = r'\d{2}-\d{2}\s{1,2}\d{2}:\d{2}:\d{2}.\d{3}'
REGEX_UIA_SERVICE_ALREADY_REGISTERED = (
    rf'({REGEX_LOGCAT_TIMESTAMP}){errors.REGEX_UIA_SERVICE_ALREADY_REGISTERED}'
)

TimeUnit = Union[float, int, datetime.timedelta]


def covert_to_millisecond(timeout: TimeUnit) -> int:
  """Converts a time unit object to an integer in milliseconds."""
  if isinstance(timeout, datetime.timedelta):
    return int(timeout.total_seconds() * 1_000)
  return int(timeout)


def get_latest_logcat_timestamp(ad: android_device.AndroidDevice) -> str:
  """Gets the latest timestamp from logcat."""
  logcat = ad.adb.logcat(['-d'])
  last_line = logcat.splitlines()[-1]
  return re.findall(REGEX_LOGCAT_TIMESTAMP.encode(), last_line)[-1].decode()


def get_mobly_ad_log_path(
    ui: snippet_client_v2.SnippetClientV2,
) -> pathlib.Path:
  """Gets the log path of Mobly AndroidDevice controller."""
  serial = ui._adb.serial  # pylint: disable=protected-access
  normalized_serial = mobly_logger.sanitize_filename(serial)
  log_path = pathlib.Path(
      mobly_utils.abs_path(getattr(logging, 'log_path', '/tmp/logs')),
      f'AndroidDevice{normalized_serial}',
  )
  mobly_utils.create_dir(log_path)
  return log_path


def get_uiautomator_apk() -> str:
  """Gets the absolute path of the UiAutomator apk."""
  return str(
      pathlib.Path(__file__).parent.joinpath(
          'android', 'app', 'uiautomator.apk'
      )
  )


def is_uiautomator_service_registered(
    ad: android_device.AndroidDevice, start_time: str
) -> bool:
  """Returns Ture if uiautomation service has registered, False otherwise.

  Args:
    ad: Mobly Android device controller.
    start_time: A timestamp that conforms to the REGEX_LOGCAT_TIMESTAMP format
      will only check the log after this time point.
  """
  logcat = ad.adb.logcat(['-d', '-s', 'AndroidRuntime:E'])
  runtime_errors = re.findall(
      REGEX_UIA_SERVICE_ALREADY_REGISTERED.encode(), logcat
  )
  if not runtime_errors:
    return False

  error_time = runtime_errors[-1].decode()
  return mobly_logger.logline_timestamp_comparator(error_time, start_time) > -1
