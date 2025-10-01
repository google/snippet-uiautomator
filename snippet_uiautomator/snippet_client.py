# Copyright 2025 Google Inc.
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

"""Snippet client for Snippet UiAutomator."""

from typing import Any, Sequence

from mobly.controllers import android_device
from mobly.controllers.android_device_lib import snippet_client_v2
from mobly.snippet import errors as snippet_errors


def _list_occupied_adb_ports(ad: android_device.AndroidDevice) -> Sequence[int]:
  """Returns a list of occupied host ports from ADB."""
  out = ad.adb.forward('--list')
  clean_lines = str(out, 'utf-8').strip().split('\n')
  used_ports = []
  for line in clean_lines:
    tokens = line.split(' tcp:')
    if len(tokens) != 3:
      continue
    used_ports.append(int(tokens[1]))
  return used_ports


class SnippetClient(snippet_client_v2.SnippetClientV2):
  """Client for interacting with Snippet UiAutomator on Android Device."""

  def __init__(
      self,
      user_args: Sequence[str],
      package: str,
      ad: android_device.AndroidDevice,
      config: Any = None,
  ):
    self.user_args = user_args
    super().__init__(package, ad, config)

  def _restart_snippet_connection(self) -> None:
    """Restarts the snippet connection."""
    if self.host_port in _list_occupied_adb_ports(self._device):
      self.close_connection()
    self._adb.shell(['pm', 'clear', *self.user_args, self.package])
    self.start_server()
    self.make_connection()

  def send_rpc_request(self, request: str) -> str:
    """Sends an RPC request to the server and receives a response."""
    try:
      return super().send_rpc_request(request)
    except (snippet_errors.ProtocolError, snippet_errors.Error) as e:
      if not isinstance(
          e, snippet_errors.ProtocolError
      ) and 'socket error' not in str(e):
        raise
      self._device.log.exception(
          'Lost connection to the snippet server. Reconnecting...'
      )
      self._restart_snippet_connection()
      return super().send_rpc_request(request)
