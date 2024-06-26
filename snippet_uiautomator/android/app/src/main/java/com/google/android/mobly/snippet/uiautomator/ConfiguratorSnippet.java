/*
 * Copyright 2023 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.google.android.mobly.snippet.uiautomator;

import androidx.test.uiautomator.Configurator;
import com.google.android.mobly.snippet.Snippet;
import com.google.android.mobly.snippet.rpc.Rpc;
import com.google.android.mobly.snippet.uiautomator.Info.ConfiguratorInfo;
import org.json.JSONException;

/**
 * Configurator snippet class.
 *
 * <p><a
 * href="https://developer.android.com/reference/androidx/test/uiautomator/Configurator">Configurator</a>
 */
public class ConfiguratorSnippet implements Snippet {
  private final Configurator configurator = Configurator.getInstance();
  private final ConfiguratorInfo defaultConfiguratorInfo = getConfigurator();

  @Rpc(description = "Gets all properties of Configurator.")
  public ConfiguratorInfo getConfigurator() {
    return ConfiguratorInfo.create(
        /* toolType= */ configurator.getToolType(),
        /* uiAutomationFlags= */ configurator.getUiAutomationFlags(),
        /* waitForIdleTimeout= */ configurator.getWaitForIdleTimeout());
  }

  @Rpc(description = "Gets the current tool type to use for motion events.")
  public int getToolType() {
    return configurator.getToolType();
  }

  @Rpc(
      description =
          "Gets the current flags that are used to obtain a android.app.UiAutomation instance.")
  public int getUiAutomationFlags() {
    return configurator.getUiAutomationFlags();
  }

  @Rpc(
      description =
          "Gets the current timeout in milliseconds used for waiting for the user interface to go"
              + " into an idle state.")
  public long getWaitForIdleTimeout() {
    return configurator.getWaitForIdleTimeout();
  }

  @Rpc(description = "Sets up Configurator.")
  public void setConfigurator(ConfiguratorInfo config) throws JSONException {
    if (config.toolType() != null) {
      configurator.setToolType(config.toolType());
    }
    if (config.uiAutomationFlags() != null) {
      configurator.setUiAutomationFlags(config.uiAutomationFlags());
    }
    if (config.waitForIdleTimeout() != null) {
      configurator.setWaitForIdleTimeout(config.waitForIdleTimeout());
    }
  }

  @Rpc(description = "Sets the current tool type to use for motion events.")
  public void setToolType(int toolType) {
    configurator.setToolType(toolType);
  }

  @Rpc(description = "Sets the flags to use when obtaining a android.app.UiAutomation instance.")
  public void setUiAutomationFlags(int flags) {
    configurator.setUiAutomationFlags(flags);
  }

  @Rpc(
      description =
          "Sets the timeout for waiting for the user interface to go into an idle state before"
              + " starting a uiautomator action.")
  public void setWaitForIdleTimeout(long timeoutInMillis) {
    configurator.setWaitForIdleTimeout(timeoutInMillis);
  }

  @Override
  public void shutdown() throws JSONException {
    setConfigurator(defaultConfiguratorInfo);
  }
}
