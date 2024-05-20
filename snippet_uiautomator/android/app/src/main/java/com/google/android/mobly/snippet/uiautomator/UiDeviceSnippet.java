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

import android.os.RemoteException;
import androidx.test.uiautomator.UiDevice;
import com.google.android.mobly.snippet.Snippet;
import com.google.android.mobly.snippet.rpc.Rpc;
import com.google.android.mobly.snippet.rpc.RpcOptional;
import com.google.android.mobly.snippet.uiautomator.Info.PointInfo;
import com.google.android.mobly.snippet.uiautomator.Info.UiDeviceInfo;
import com.google.android.mobly.snippet.uiautomator.Info.UiObject2Info;
import com.google.android.mobly.snippet.uiautomator.selector.Selector;
import com.google.android.mobly.snippet.uiautomator.selector.SelectorException;
import com.google.android.mobly.snippet.util.Log;
import com.google.common.collect.ImmutableList;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.stream.Collectors;
import org.checkerframework.checker.nullness.qual.Nullable;
import org.json.JSONArray;
import org.json.JSONException;

/**
 * UiDevice snippet class.
 *
 * <p><a
 * href="https://developer.android.com/reference/androidx/test/uiautomator/UiDevice">UiDevice</a>
 */
public class UiDeviceSnippet implements Snippet {
  protected UiDevice uiDevice = UiAutomator.getUiDevice();

  @Rpc(description = "Performs a click at arbitrary coordinates specified by the user.")
  public boolean click(int x, int y) {
    return uiDevice.click(x, y);
  }

  @Rpc(description = "Performs a swipe from one coordinate to another coordinate.")
  public boolean drag(int startX, int startY, int endX, int endY, int steps) {
    return uiDevice.drag(startX, startY, endX, endY, steps);
  }

  @Rpc(description = "Dumps the current window hierarchy to a string.")
  public String dump() throws IOException {
    try (OutputStream outputStream = new ByteArrayOutputStream()) {
      uiDevice.dumpWindowHierarchy(outputStream);
      return outputStream.toString();
    }
  }

  @Rpc(description = "Returns all objects that match the selector criteria.")
  public ImmutableList<UiObject2Info> findObjects(Selector selector) throws SelectorException {
    return ImmutableList.copyOf(
        uiDevice.findObjects(selector.toBySelector()).stream()
            .map(Info::getUiObject2Info)
            .collect(Collectors.toList())
    );
  }

  @Rpc(description = "Disables the sensors and freezes rotation at its current rotation state.")
  public boolean freezeRotation() {
    return tryToExecute(uiDevice::freezeRotation);
  }

  @Rpc(description = "Retrieves the name of the last package to report accessibility events.")
  public String getCurrentPackageName() {
    return uiDevice.getCurrentPackageName();
  }

  @Rpc(description = "Gets the height of the display, in pixels.")
  public int getDisplayHeight() {
    return uiDevice.getDisplayHeight();
  }

  @Rpc(description = "Returns the current rotation of the display, as defined in Surface.")
  public int getDisplayRotation() {
    return uiDevice.getDisplayRotation();
  }

  @Rpc(description = "Returns the display size in dp (device-independent pixel).")
  public PointInfo getDisplaySizeDp() {
    return Info.getPointInfo(uiDevice.getDisplaySizeDp());
  }

  @Rpc(description = "Gets the width of the display, in pixels.")
  public int getDisplayWidth() {
    return uiDevice.getDisplayWidth();
  }

  @Rpc(description = "Retrieves default launcher package name.")
  public String getLauncherPackageName() {
    return uiDevice.getLauncherPackageName();
  }

  @Rpc(description = "Retrieves the product name of the device.")
  public String getProductName() {
    return uiDevice.getProductName();
  }

  @Rpc(description = "Returns all properties of device information.")
  public UiDeviceInfo getDevInfo() {
    return Info.getUiDeviceInfo(uiDevice);
  }

  @Rpc(description = "Returns whether there is a match for the given selector criteria.")
  public boolean hasObject(Selector selector) throws SelectorException {
    return uiDevice.hasObject(selector.toBySelector());
  }

  @Rpc(description = "Checks the power manager if the screen is ON.")
  public boolean isScreenOn() throws RemoteException {
    return uiDevice.isScreenOn();
  }

  @Rpc(description = "Opens the notification shade.")
  public boolean openNotification() {
    return uiDevice.openNotification();
  }

  @Rpc(description = "Opens the Quick Settings shade.")
  public boolean openQuickSettings() {
    return uiDevice.openQuickSettings();
  }

  @Rpc(description = "Simulates a short press on the BACK button.")
  public boolean pressBack() {
    return uiDevice.pressBack();
  }

  @Rpc(description = "Simulates a short press on the CENTER button.")
  public boolean pressDPadCenter() {
    return uiDevice.pressDPadCenter();
  }

  @Rpc(description = "Simulates a short press on the DOWN button.")
  public boolean pressDPadDown() {
    return uiDevice.pressDPadDown();
  }

  @Rpc(description = "Simulates a short press on the LEFT button.")
  public boolean pressDPadLeft() {
    return uiDevice.pressDPadLeft();
  }

  @Rpc(description = "Simulates a short press on the RIGHT button.")
  public boolean pressDPadRight() {
    return uiDevice.pressDPadRight();
  }

  @Rpc(description = "Simulates a short press on the UP button.")
  public boolean pressDPadUp() {
    return uiDevice.pressDPadUp();
  }

  @Rpc(description = "Simulates a short press on the DELETE key.")
  public boolean pressDelete() {
    return uiDevice.pressDelete();
  }

  @Rpc(description = "Simulates a short press on the ENTER key.")
  public boolean pressEnter() {
    return uiDevice.pressEnter();
  }

  @Rpc(description = "Simulates a short press on the HOME key.")
  public boolean pressHome() {
    return uiDevice.pressHome();
  }

  @Rpc(description = "Simulates a short press using a key code.")
  public boolean pressKeyCode(int keyCode, @RpcOptional Integer metaState) {
    return metaState == null
        ? uiDevice.pressKeyCode(keyCode)
        : uiDevice.pressKeyCode(keyCode, metaState);
  }

  @Rpc(description = "Simulates short press one or more keys using key code.")
  public boolean pressKeyCodes(JSONArray keyCodes, @RpcOptional Integer metaState)
      throws JSONException {
    int[] keyCodeArray = new int[keyCodes.length()];
    for (int i = 0; i < keyCodes.length(); i++) {
      keyCodeArray[i] = keyCodes.getInt(i);
    }
    return metaState == null
        ? uiDevice.pressKeyCodes(keyCodeArray)
        : uiDevice.pressKeyCodes(keyCodeArray, metaState);
  }

  @Rpc(description = "Simulates a short press on the MENU key.")
  public boolean pressMenu() {
    return uiDevice.pressMenu();
  }

  @Rpc(description = "Simulates a short press on the RECENT APPS button.")
  public boolean pressRecentApps() throws RemoteException {
    return uiDevice.pressRecentApps();
  }

  @Rpc(description = "Simulates a short press on the SEARCH button.")
  public boolean pressSearch() {
    return uiDevice.pressSearch();
  }

  @Rpc(description = "Enables or disables layout hierarchy compression.")
  public void setCompressedLayoutHierarchy(boolean compressed) {
    uiDevice.setCompressedLayoutHierarchy(compressed);
  }

  @Rpc(
      description =
          "Simulates orienting the device to the left and also freezes rotation by disabling the"
              + " sensors.")
  public boolean setOrientationLeft() {
    return tryToExecute(uiDevice::setOrientationLeft);
  }

  @Rpc(
      description =
          "Simulates orienting the device into its natural orientation and also freezes rotation by"
              + " disabling the sensors.")
  public boolean setOrientationNatural() {
    return tryToExecute(uiDevice::setOrientationNatural);
  }

  @Rpc(
      description =
          "Simulates orienting the device to the right and also freezes rotation by disabling the"
              + " sensors.")
  public boolean setOrientationRight() {
    return tryToExecute(uiDevice::setOrientationRight);
  }

  @Rpc(
      description =
          "Simulates a short press on the POWER button if the screen is ON, do nothing if the"
              + " screen is already OFF.")
  public boolean sleep() {
    return tryToExecute(uiDevice::sleep);
  }

  @Rpc(description = "Performs a swipe from one coordinate to another.")
  public boolean swipe(int startX, int startY, int endX, int endY, int steps) {
    return uiDevice.swipe(startX, startY, endX, endY, steps);
  }

  @Rpc(
      description =
          "Re-enables the sensors and un-freezes the device rotation allowing its contents to"
              + " rotate with the device physical rotation.")
  public boolean unfreezeRotation() {
    return tryToExecute(uiDevice::unfreezeRotation);
  }

  @Rpc(description = "Waits for the current application to idle.")
  public void waitForIdle(long timeoutInMillis) {
    uiDevice.waitForIdle(timeoutInMillis);
  }

  @Rpc(description = "Waits for a window content update event to occur.")
  public boolean waitForWindowUpdate(@Nullable String packageName, long timeoutInMillis) {
    return uiDevice.waitForWindowUpdate(packageName, timeoutInMillis);
  }

  @Rpc(
      description =
          "Simulates a short press on the POWER button if the screen OFF, do nothing if the screen"
              + " is already ON.")
  public boolean wakeUp() {
    return tryToExecute(uiDevice::wakeUp);
  }

  private interface ThrowingRunnable {
    void run() throws Exception;
  }

  private static boolean tryToExecute(ThrowingRunnable func) {
    try {
      func.run();
      return true;
    } catch (Exception e) {
      Log.e(e);
      return false;
    }
  }

  @Override
  public void shutdown() {}
}
