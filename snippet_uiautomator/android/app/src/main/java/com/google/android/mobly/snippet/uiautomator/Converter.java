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

import com.google.android.mobly.snippet.SnippetObjectConverter;
import com.google.android.mobly.snippet.uiautomator.Info.ConfiguratorInfo;
import com.google.android.mobly.snippet.uiautomator.Info.PointInfo;
import com.google.android.mobly.snippet.uiautomator.Info.RectInfo;
import com.google.android.mobly.snippet.uiautomator.Info.UiDeviceInfo;
import com.google.android.mobly.snippet.uiautomator.Info.UiObject2Info;
import com.google.android.mobly.snippet.uiautomator.selector.Selector;
import java.lang.reflect.Type;
import org.json.JSONException;
import org.json.JSONObject;

/** Defines how the complex type should be converted against JSONObject. */
public class Converter implements SnippetObjectConverter {
  @Override
  public JSONObject serialize(Object object) throws JSONException {
    JSONObject obj = new JSONObject();
    if (object instanceof PointInfo) {
      PointInfo pointInfo = (PointInfo) object;
      obj.put("x", pointInfo.x());
      obj.put("y", pointInfo.y());
      return obj;
    } else if (object instanceof RectInfo) {
      RectInfo rectInfo = (RectInfo) object;
      obj.put("top", rectInfo.top());
      obj.put("bottom", rectInfo.bottom());
      obj.put("left", rectInfo.left());
      obj.put("right", rectInfo.right());
      return obj;
    } else if (object instanceof ConfiguratorInfo) {
      ConfiguratorInfo configuratorInfo = (ConfiguratorInfo) object;
      obj.put("toolType", configuratorInfo.toolType());
      obj.put("uiAutomationFlags", configuratorInfo.uiAutomationFlags());
      obj.put("waitForIdleTimeout", configuratorInfo.waitForIdleTimeout());
      return obj;
    } else if (object instanceof UiDeviceInfo) {
      UiDeviceInfo uiDeviceInfo = (UiDeviceInfo) object;
      obj.put("naturalOrientation", uiDeviceInfo.naturalOrientation());
      obj.put("displayRotation", uiDeviceInfo.displayRotation());
      obj.put("displayHeight", uiDeviceInfo.displayHeight());
      obj.put("displaySizeDpX", uiDeviceInfo.displaySizeDpX());
      obj.put("displaySizeDpY", uiDeviceInfo.displaySizeDpY());
      obj.put("displayWidth", uiDeviceInfo.displayWidth());
      obj.put("sdkInt", uiDeviceInfo.sdkInt());
      obj.put("currentPackageName", uiDeviceInfo.currentPackageName());
      obj.put("productName", uiDeviceInfo.productName());
      return obj;
    } else if (object instanceof UiObject2Info) {
      UiObject2Info uiObjectInfo = (UiObject2Info) object;
      obj.put("childCount", uiObjectInfo.childCount());
      obj.put("displayId", uiObjectInfo.displayId());
      obj.put("className", uiObjectInfo.className());
      obj.put("contentDescription", uiObjectInfo.contentDescription());
      obj.put("hint", uiObjectInfo.hint());
      obj.put("packageName", uiObjectInfo.packageName());
      obj.put("resourceId", uiObjectInfo.resourceId());
      obj.put("text", uiObjectInfo.text());
      obj.put("checkable", uiObjectInfo.checkable());
      obj.put("checked", uiObjectInfo.checked());
      obj.put("clickable", uiObjectInfo.clickable());
      obj.put("enabled", uiObjectInfo.enabled());
      obj.put("focusable", uiObjectInfo.focusable());
      obj.put("focused", uiObjectInfo.focused());
      obj.put("longClickable", uiObjectInfo.longClickable());
      obj.put("scrollable", uiObjectInfo.scrollable());
      obj.put("selected", uiObjectInfo.selected());
      obj.put("visibleBounds", serialize(uiObjectInfo.visibleBounds()));
      obj.put("visibleCenter", serialize(uiObjectInfo.visibleCenter()));
      return obj;
    }
    return null;
  }

  @Override
  public Object deserialize(JSONObject jsonObject, Type type) throws JSONException {
    if (type == Selector.class) {
      return new Selector(jsonObject);
    } else if (type == ConfiguratorInfo.class) {
      return ConfiguratorInfo.create(
          jsonObject.has("toolType") ? jsonObject.getInt("toolType") : null,
          jsonObject.has("uiAutomationFlags") ? jsonObject.getInt("uiAutomationFlags") : null,
          jsonObject.has("waitForIdleTimeout") ? jsonObject.getLong("waitForIdleTimeout") : null);
    }
    return null;
  }
}
