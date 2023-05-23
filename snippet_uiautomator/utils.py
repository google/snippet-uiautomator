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
from typing import Union

from mobly import logger as mobly_logger
from mobly import utils as mobly_utils
from mobly.controllers.android_device_lib import snippet_client_v2

TimeUnit = Union[float, int, datetime.timedelta]


def covert_to_millisecond(timeout: TimeUnit) -> int:
  """Converts a time unit object to an integer in milliseconds."""
  if isinstance(timeout, datetime.timedelta):
    return int(timeout.total_seconds() * 1_000)
  return int(timeout)


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

