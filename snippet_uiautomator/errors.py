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

from typing import Optional

from mobly.controllers import android_device

ERROR_WHEN_APK_IS_NOT_INSTALLED = (
    '`skip_installing` is True but package {package_name} is not installed'
)
ERROR_WHEN_FILE_PATH_MISSING = (
    'Need to provide file path to configuration for installing snippet'
)
ERROR_WHEN_INSTANCE_MISSING = 'Missing UiDevice instance {instance}'
ERROR_WHEN_PACKAGE_NAME_MISSING = (
    'Need to provide package name to configuration for launching snippet'
)
ERROR_WHEN_SERVICE_ALREADY_REGISTERED = (
    'UiAutomation service has been registered by another app. Please stop the'
    ' app to release the service.'
)
ERROR_WHEN_SERVICE_NOT_RUNNING = 'Snippet UiAutomator service is not running'

REGEX_UIA_SERVICE_ALREADY_REGISTERED = r'.*UiAutomationService.*registered'
REGEX_TCP_PORT_NOT_FOUND = rb"adb: error: listener 'tcp:(\d+)' not found\n|$"


class BaseError(Exception):
  """Base error for Snippet UiAutomator."""

  def __init__(
      self, message: str, ad: Optional[android_device.AndroidDevice] = None
  ) -> None:
    self._ad = ad
    self._message = message

  def __str__(self) -> str:
    return self._message if self._ad is None else f'{self._ad} {self._message}'


class ApiError(BaseError):
  """Raised when an inexistent API is called or API is used incorrectly."""


class ConfigurationError(BaseError):
  """Raised when passed incorrect configuration to Snippet UiAutomator."""


class UiAutomatorError(BaseError):
  """Raised when fail to operate UiAutomator."""


class UiAutomationServiceAlreadyRegisteredError(BaseError):
  """Raised when UiAutomation service has already registered by other app."""


class UiObjectSearchError(BaseError):
  """Raised when an object does not match the search criteria."""
