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

"""Python wrapper for Android UI Automator."""

from __future__ import annotations

import dataclasses
import re
from typing import Optional

from mobly import utils as mobly_utils
from mobly.controllers import android_device
from mobly.controllers.android_device_lib import adb
from mobly.controllers.android_device_lib.services import base_service
from mobly.snippet import errors as snippet_errors
from snippet_uiautomator import configurator as uiconfig
from snippet_uiautomator import errors
from snippet_uiautomator import uidevice
from snippet_uiautomator import uiobject2
from snippet_uiautomator import uiwatcher
from snippet_uiautomator import utils

UIAUTOMATOR_PACKAGE_NAME = 'com.google.android.mobly.snippet.uiautomator'

ANDROID_SERVICE_NAME = 'uiautomator'
HIDDEN_SERVICE_NAME = '_ui'
PUBLIC_SERVICE_NAME = 'ui'

Configurator = uiconfig.Configurator
Flag = uiconfig.Flag
Timeout = uiconfig.Timeout
ToolType = uiconfig.ToolType
UiDevice = uidevice.UiDevice
UiObject2 = uiobject2.UiObject2
UiWatcher = uiwatcher.UiWatcher


@dataclasses.dataclass
class Snippet:
  """The information of the Mobly Snippet app.

  Attributes:
    file_path: The absolute apk path of the snippet.
    package_name: The package name of the snippet.
    ui_public_service_name: The attribute name to which to attach the Python
      wrapper of Snippet UiAutomator.
    ui_hidden_service_name: The actual attribute name to which to attach the
      snippet client of Snippet UiAutomator. This can be None if
      Snippet.custom_service_name is set.
    custom_service_name: The attribute name that has already attached to the
      existing snippet client. This can be None if the Snippet UiAutomator is
      not wrapped into other snippet apps.
  """

  file_path: str = dataclasses.field(default_factory=utils.get_uiautomator_apk)
  package_name: str = UIAUTOMATOR_PACKAGE_NAME
  ui_public_service_name: str = PUBLIC_SERVICE_NAME
  ui_hidden_service_name: Optional[str] = None
  custom_service_name: Optional[str] = None


@dataclasses.dataclass
class UiAutomatorConfigs:
  """A configuration object for configuring the UiAutomatorService.

  Attributes:
    snippet: The information of the Mobly Snippet app.
    configurator: The Configurator to configure UiAutomator.
    skip_installing: Set to True if the APK has already been installed.
    raise_error: By default, a boolean value indicates whether an object
      appears/disappears as expected in UiObject2#exists and UiObject2#wait
      APIs. Set to True to raise an error instead of returning a False value.
  """

  snippet: Snippet
  configurator: Configurator
  skip_installing: bool
  raise_error: bool


class UiAutomatorService(base_service.BaseService):
  """A service for operating Snippet UiAutomator."""

  def __init__(
      self,
      ad: android_device.AndroidDevice,
      configs: UiAutomatorConfigs,
  ) -> None:
    super().__init__(ad, configs)
    self._service = (
        configs.snippet.custom_service_name
        or configs.snippet.ui_hidden_service_name
        or HIDDEN_SERVICE_NAME
    )

  @property
  def _is_apk_installed(self) -> bool:
    """Checks if the snippet apk is already installed."""
    all_packages = self._device.adb.shell(['pm', 'list', 'package'])
    return bool(
        mobly_utils.grep(
            f'^package:{self._configs.snippet.package_name}$', all_packages
        )
    )

  def _install_apk(self) -> None:
    """Installs the snippet apk to the Android devices."""
    if self._configs.skip_installing:
      if not self._is_apk_installed:
        raise errors.ConfigurationError(
            errors.ERROR_WHEN_APK_IS_NOT_INSTALLED.format(
                package_name=self._configs.snippet.package_name
            )
        )
    else:
      if self._is_apk_installed:
        # In case the existing application is signed with a different key.
        self._device.adb.uninstall(self._configs.snippet.package_name)
      self._device.adb.install(['-g', self._configs.snippet.file_path])

  def _load_snippet(self) -> None:
    """Starts the snippet apk with the given package name and connects."""
    snippet_manager = self._device.services.snippets
    if snippet_manager.get_snippet_client(self._service) is not None:
      self._device.log.info(
          'Snippet client %s has already been loaded', self._service
      )
      return

    if self._configs.snippet.package_name is None:
      raise errors.ConfigurationError(errors.ERROR_WHEN_PACKAGE_NAME_MISSING)

    start_time = utils.get_latest_logcat_timestamp(self._device)
    try:
      self._device.load_snippet(
          self._service, self._configs.snippet.package_name
      )
    except snippet_errors.ServerStartProtocolError as e:
      if utils.is_uiautomator_service_registered(self._device, start_time):
        raise errors.UiAutomationServiceAlreadyRegisteredError(
            self._device.serial, errors.ERROR_WHEN_SERVICE_ALREADY_REGISTERED
        ) from e
      raise

  def _initial_uidevice(self) -> None:
    """Initializes the UiDevice object."""
    snippet_client = getattr(self._device, self._service)
    snippet_client.setConfigurator(self._configs.configurator.to_dict())
    setattr(
        self._device,
        self._configs.snippet.ui_public_service_name,
        UiDevice(ui=snippet_client, raise_error=self._configs.raise_error),
    )

  @property
  def ui_device(self) -> UiDevice:
    """Gets the UiDevice object."""
    if not self.is_alive:
      raise errors.ConfigurationError(errors.ERROR_WHEN_SERVICE_NOT_RUNNING)
    service = getattr(
        self._device, self._configs.snippet.ui_public_service_name, None
    )
    if service is None:
      raise errors.ConfigurationError(
          errors.ERROR_WHEN_INSTANCE_MISSING.format(
              instance=self._configs.snippet.ui_public_service_name,
              serial=self._device.serial,
          )
      )
    return service

  @property
  def is_alive(self) -> bool:
    return (
        hasattr(self._device, self._configs.snippet.ui_public_service_name)
        and hasattr(self._device.services, 'snippets')
        and self._device.services.snippets.get_snippet_client(self._service)
        is not None
    )

  def start(self) -> None:
    if self.is_alive:
      self._device.log.debug('uiautomator service has already started')
    else:
      self._install_apk()
      self._load_snippet()
      self._initial_uidevice()
      self._configs.skip_installing = True

  def stop(self) -> None:
    if not self.is_alive:
      self._device.log.debug('uiautomator service has already stopped')
      return

    if not self._is_apk_installed:
      self._device.log.debug(
          'package %s was uninstalled before stopping the service',
          self._configs.snippet.package_name,
      )
      return

    try:
      self._device.unload_snippet(self._service)
    except adb.AdbError as e:
      if re.fullmatch(errors.REGEX_TCP_PORT_NOT_FOUND, e.stderr) is None:
        raise
      self._device.log.exception(
          'listener TCP port has already lost connection before unloading the'
          ' snippet client'
      )

    if hasattr(self._device, self._configs.snippet.ui_public_service_name):
      delattr(self._device, self._configs.snippet.ui_public_service_name)
    else:
      self._device.log.debug(
          'class UiDevice %s was deleted before stopping the service',
          self._configs.snippet.ui_public_service_name,
      )

  def pause(self):
    if self.is_alive:
      client = self._device.services.snippets.get_snippet_client(self._service)
      client.close_connection()
      self._device.log.debug('uiautomator service is paused')
    else:
      self._device.log.debug('uiautomator service has already paused')

  def resume(self):
    if self.is_alive:
      self._device.log.debug('uiautomator service has already resumed')
    else:
      client = self._device.services.snippets.get_snippet_client(self._service)
      client.restore_server_connection()
      self._device.log.debug('uiautomator service is resumed')


def load_uiautomator_service(
    ad: android_device.AndroidDevice,
    snippet: Optional[Snippet] = None,
    configurator: Optional[Configurator] = None,
    skip_installing: bool = False,
    raise_error: bool = False,
) -> None:
  """Loads Snippet UiAutomator as a Mobly AndroidDevice service."""
  if ad.services.has_service_by_name(ANDROID_SERVICE_NAME):
    ad.services.unregister(ANDROID_SERVICE_NAME)

  ad.services.register(
      ANDROID_SERVICE_NAME,
      service_class=UiAutomatorService,
      configs=UiAutomatorConfigs(
          snippet=snippet or Snippet(),
          configurator=configurator or Configurator(),
          skip_installing=skip_installing,
          raise_error=raise_error,
      ),
  )


def unload_uiautomator_service(ad: android_device.AndroidDevice) -> None:
  """Stops Snippet UiAutomator service."""
  if ad.services.has_service_by_name(ANDROID_SERVICE_NAME):
    ad.services.unregister(ANDROID_SERVICE_NAME)
