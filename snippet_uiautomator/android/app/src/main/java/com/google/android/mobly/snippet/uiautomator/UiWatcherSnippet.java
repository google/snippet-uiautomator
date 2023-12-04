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

import androidx.test.uiautomator.Direction;
import androidx.test.uiautomator.UiDevice;
import androidx.test.uiautomator.UiObject2;
import com.google.android.mobly.snippet.Snippet;
import com.google.android.mobly.snippet.rpc.Rpc;
import com.google.android.mobly.snippet.uiautomator.selector.Selector;
import java.util.ArrayList;
import java.util.Optional;
import org.checkerframework.checker.nullness.qual.Nullable;

/**
 * UiWatcher snippet class.
 *
 * <p><a
 * href="https://developer.android.com/reference/androidx/test/uiautomator/UiWatcher">UiWatcher</a>
 */
public class UiWatcherSnippet implements Snippet {
  private final UiDevice uiDevice = UiAutomator.getUiDevice();
  private final ArrayList<String> watchers = new ArrayList<>();

  @Rpc(description = "Checks if any registered UiWatcher have triggered.")
  public boolean hasAnyWatcherTriggered() {
    return uiDevice.hasAnyWatcherTriggered();
  }

  @Rpc(description = "Checks if a specific registered UiWatcher has triggered.")
  public boolean hasWatcherTriggered(String watcherName) {
    return uiDevice.hasWatcherTriggered(watcherName);
  }

  @Rpc(description = "Gets all registered UiWatchers.")
  public ArrayList<String> getWatchers() {
    return watchers;
  }

  @Rpc(description = "Registers a UiWatcher to run automatically when expected condition happened.")
  public void registerWatcher(String name, Selector condition, @Nullable Selector action) {
    uiDevice.registerWatcher(
        name,
        () -> {
          Optional<UiObject2> conditionUiObject2 =
              Optional.ofNullable(condition.toUiObject2NoWait());
          if (conditionUiObject2.isPresent()) {
            if (action == null) {
              conditionUiObject2.get().click();
              return true;
            } else {
              Optional<UiObject2> actionUiObject2 = Optional.ofNullable(action.toUiObject2NoWait());
              actionUiObject2.ifPresent(UiObject2::click);
              return actionUiObject2.isPresent();
            }
          }
          return false;
        });
    watchers.add(name);
  }

  @Rpc(description = "Registers a UiWatcher to run automatically when expected condition happened.")
  public void registerWatcherForKeycodes(String name, Selector condition, Integer[] keyCodes) {
    uiDevice.registerWatcher(
        name,
        () -> {
          if (condition.toUiObject2NoWait() == null) {
            return false;
          }
          for (int keyCode : keyCodes) {
            uiDevice.pressKeyCode(keyCode);
          }
          return true;
        });
    watchers.add(name);
  }

  @Rpc(description = "Registers a UiWatcher to run automatically when expected condition happened.")
  public void registerWatcherForSwipe(
      String name,
      Selector condition,
      @Nullable Selector action,
      String direction,
      int percent,
      int speed) {
    uiDevice.registerWatcher(
        name,
        () -> {
          UiObject2 conditionUiObject2 = condition.toUiObject2NoWait();
          if (conditionUiObject2 == null) {
            return false;
          }

          if (action == null) {
            conditionUiObject2.swipe(Direction.valueOf(direction), percent / 100f, speed);
            return true;
          } else {
            Optional<UiObject2> actionUiObject2 = Optional.ofNullable(action.toUiObject2NoWait());
            actionUiObject2.ifPresent(
                swipeObject ->
                    swipeObject.swipe(Direction.valueOf(direction), percent / 100f, speed));
            return actionUiObject2.isPresent();
          }
        });
    watchers.add(name);
  }

  @Rpc(description = "Removes a previously registered UiWatcher.")
  public void removeWatcher(String name) {
    uiDevice.removeWatcher(name);
    watchers.remove(name);
  }

  @Rpc(description = "Removes all registered UiWatchers.")
  public void removeWatchers() {
    for (String watcherName : watchers) {
      uiDevice.removeWatcher(watcherName);
    }
    watchers.clear();
  }

  @Rpc(description = "Resets a UiWatcher that has been triggered.")
  public void resetWatcherTriggers() {
    uiDevice.resetWatcherTriggers();
  }

  @Rpc(description = "Forces all registered watchers to run.")
  public void runWatchers() {
    uiDevice.runWatchers();
  }

  @Override
  public void shutdown() {}
}
