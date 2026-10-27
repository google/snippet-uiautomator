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

import android.accessibilityservice.AccessibilityServiceInfo;
import android.app.UiAutomation;
import android.graphics.Rect;
import android.os.Build;
import android.view.accessibility.AccessibilityWindowInfo;
import com.google.android.mobly.snippet.Snippet;
import com.google.android.mobly.snippet.rpc.Rpc;
import com.google.android.mobly.snippet.rpc.RpcMinSdk;
import java.util.List;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * UiAutomation snippet class.
 *
 * <p><a href="https://developer.android.com/reference/android/app/UiAutomation">UiAutomation</a>
 */
public class UiAutomationSnippet implements Snippet {
  private static UiAutomation uiAutomation = UiAutomator.getUiAutomation();

  @Rpc(description = "Clears the accessibility cache.")
  public boolean clearCache() {
    return Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE
        && uiAutomation.clearCache();
  }

  @Rpc(description = "Lists the accessibility windows currently on screen.")
  public JSONArray listWindows() throws JSONException {
    AccessibilityServiceInfo info = uiAutomation.getServiceInfo();
    if (info != null
        && (info.flags & AccessibilityServiceInfo.FLAG_RETRIEVE_INTERACTIVE_WINDOWS) == 0) {
      info.flags |= AccessibilityServiceInfo.FLAG_RETRIEVE_INTERACTIVE_WINDOWS;
      uiAutomation.setServiceInfo(info);
    }
    JSONArray result = new JSONArray();
    List<AccessibilityWindowInfo> windows = uiAutomation.getWindows();
    if (windows == null) {
      return result;
    }
    for (AccessibilityWindowInfo window : windows) {
      if (window == null) {
        continue;
      }
      Rect bounds = new Rect();
      window.getBoundsInScreen(bounds);
      CharSequence title = window.getTitle();
      JSONObject entry = new JSONObject();
      entry.put("id", window.getId());
      entry.put("type", window.getType());
      entry.put("layer", window.getLayer());
      entry.put("bounds", bounds.toShortString());
      entry.put("title", title == null ? "" : title.toString());
      entry.put("active", window.isActive());
      entry.put("focused", window.isFocused());
      result.put(entry);
    }
    return result;
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
