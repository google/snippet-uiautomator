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

import android.app.Instrumentation;
import android.app.UiAutomation;
import android.os.Bundle;
import androidx.test.platform.app.InstrumentationRegistry;
import androidx.test.uiautomator.Configurator;
import androidx.test.uiautomator.UiDevice;

/** Initialize UiAutomator when starting Mobly Snippet service. */
public class UiAutomator {
  private static final Instrumentation instrumentation =
      InstrumentationRegistry.getInstrumentation();
  private static final UiAutomation uiAutomation;
  private static final UiDevice uiDevice;

  static {
    applyFlagsFromArguments();
    uiAutomation = initializeUiAutomation();
    uiDevice = UiDevice.getInstance(instrumentation);
  }

  public static UiAutomation getUiAutomation() {
    return uiAutomation;
  }

  public static UiDevice getUiDevice() {
    return uiDevice;
  }

  private static UiAutomation initializeUiAutomation() {
    Bundle arguments = InstrumentationRegistry.getArguments();
    if (arguments.containsKey("uiAutomationFlags")) {
      try {
        int flags = Integer.parseInt(arguments.getString("uiAutomationFlags"));
        return instrumentation.getUiAutomation(flags);
      } catch (NumberFormatException e) {
        // Ignore invalid flags
      }
    }
    return instrumentation.getUiAutomation();
  }

  private static void applyFlagsFromArguments() {
    Bundle arguments = InstrumentationRegistry.getArguments();
    if (arguments.containsKey("uiAutomationFlags")) {
      try {
        int flags = Integer.parseInt(arguments.getString("uiAutomationFlags"));
        Configurator.getInstance().setUiAutomationFlags(flags);
      } catch (NumberFormatException e) {
        // Ignore invalid flags
      }
    }
    if (arguments.containsKey("toolType")) {
      try {
        int toolType = Integer.parseInt(arguments.getString("toolType"));
        Configurator.getInstance().setToolType(toolType);
      } catch (NumberFormatException e) {
      }
    }
    if (arguments.containsKey("waitForIdleTimeout")) {
      try {
        long timeout = Long.parseLong(arguments.getString("waitForIdleTimeout"));
        Configurator.getInstance().setWaitForIdleTimeout(timeout);
      } catch (NumberFormatException e) {
      }
    }
  }

  private UiAutomator() {}
}
