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

"""Common errors for Snippet UiAutomator."""

ERROR_WHEN_APK_IS_NOT_INSTALLED = (
    '`skip_installing` is True but package {package_name} is not installed'
)
ERROR_WHEN_FILE_PATH_MISSING = (
    'Need to provide file path to configuration for installing snippet'
)
ERROR_WHEN_INSTANCE_MISSING = (
    'Missing UiDevice instance {instance} from AndroidDevice {serial}'
)
ERROR_WHEN_PACKAGE_NAME_MISSING = (
    'Need to provide package name to configuration for launching snippet'
)
ERROR_WHEN_SERVICE_NOT_RUNNING = 'Snippet UiAutomator service is not running'

REGEX_TCP_PORT_NOT_FOUND = rb"adb: error: listener 'tcp:(\d+)' not found\n|$"


class BaseError(Exception):
  """Base error for Snippet UiAutomator."""

  def __init__(self, serial: str, message: str) -> None:
    self._serial = serial
    self._message = message

  def __str__(self) -> str:
    return f'[AndroidDevice|{self._serial}] {self._message}'


class ApiError(Exception):
  """Raised when an inexistent API is called or API is used incorrectly."""


class ConfigurationError(Exception):
  """Raised when passed incorrect configuration to Snippet UiAutomator."""


class UiAutomatorError(Exception):
  """Raised when fail to operate UiAutomator."""


class UiObjectSearchError(BaseError):
  """Raised when an object does not match the search criteria."""

