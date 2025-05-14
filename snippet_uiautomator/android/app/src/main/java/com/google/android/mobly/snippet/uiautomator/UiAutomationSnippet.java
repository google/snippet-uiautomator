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

import android.app.UiAutomation;
import android.os.Build;

import com.google.android.mobly.snippet.Snippet;
import com.google.android.mobly.snippet.rpc.Rpc;
import com.google.android.mobly.snippet.rpc.RpcMinSdk;

/**
 * UiAutomation snippet class.
 *
 * <p><a
 * href="https://developer.android.com/reference/android/app/UiAutomation">UiAutomation</a>
 */
public class UiAutomationSnippet implements Snippet {
  private static final UiAutomation uiAutomation = UiAutomator.getUiAutomation();

  @Rpc(description = "Clears the accessibility cache.")
  public boolean clearCache() {
    return Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE && uiAutomation.clearCache();
  }

  @RpcMinSdk(Build.VERSION_CODES.Q)
  @Rpc(description = "Adopt Shell Permission Identity")
  public void adoptShellPermissionIdentity() {
    uiAutomation.adoptShellPermissionIdentity();
  }

  @RpcMinSdk(Build.VERSION_CODES.Q)
  @Rpc(description = "Drop Shell Permission Identity")
  public void dropShellPermissionIdentity() {
    uiAutomation.dropShellPermissionIdentity();
  }

  @Override
  public void shutdown() {
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
      dropShellPermissionIdentity();
    }
  }
}
