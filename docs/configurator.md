# Configurator API Usage

This doc shows how Snippet UiAutomator implements the
[Configurator](https://developer.android.com/reference/androidx/test/uiautomator/Configurator)
to configure UiAutomator.

## Flag

The flag is a bitmask that can be used to control the behavior of the
UiAutomator instance.

-   [FLAG_DONT_SUPPRESS_ACCESSIBILITY_SERVICES](https://developer.android.com/reference/android/app/UiAutomation.html#FLAG_DONT_SUPPRESS_ACCESSIBILITY_SERVICES)

-   [FLAG_DONT_USE_ACCESSIBILITY](https://developer.android.com/reference/android/app/UiAutomation.html#FLAG_DONT_USE_ACCESSIBILITY)

```python
configurator = uiautomator.Configurator(
    flags=[
        uiautomator.Flag.FLAG_DONT_SUPPRESS_ACCESSIBILITY_SERVICES,
    ]
)
ad.services.register(
    uiautomator.ANDROID_SERVICE_NAME,
    uiautomator.UiAutomatorService,
    uiautomator.UiAutomatorConfigs(configurator=configurator),
)
```

## Timeout

By default, Snippet UiAutomator will set `wait_for_selector` to 0 seconds, which
means there will be no waiting for a widget matched by a selector to become
visible.

Timeouts can be also customized via passing
[datetime.timedelta](https://docs.python.org/3/library/datetime.html#timedelta-objects).

-   [key_injection_delay](https://developer.android.com/reference/androidx/test/uiautomator/Configurator#setKeyInjectionDelay\(long\))

-   [action_acknowledgment](https://developer.android.com/reference/androidx/test/uiautomator/Configurator#setActionAcknowledgmentTimeout\(long\))

-   [scroll_acknowledgment](https://developer.android.com/reference/androidx/test/uiautomator/Configurator#setScrollAcknowledgmentTimeout\(long\))

-   [wait_for_idle](https://developer.android.com/reference/androidx/test/uiautomator/Configurator#setWaitForIdleTimeout\(long\))

-   [wait_for_selector](https://developer.android.com/reference/androidx/test/uiautomator/Configurator#setWaitForSelectorTimeout\(long\))

```python
configurator = uiautomator.Configurator(
    timeout=uiautomator.Timeout(
        key_injection_delay=datetime.timedelta(seconds=0),
        action_acknowledgment=datetime.timedelta(seconds=0),
        scroll_acknowledgment=datetime.timedelta(seconds=0),
        wait_for_idle=datetime.timedelta(seconds=0),
        wait_for_selector=datetime.timedelta(seconds=0),
    )
)
ad.services.register(
    uiautomator.ANDROID_SERVICE_NAME,
    uiautomator.UiAutomatorService,
    uiautomator.UiAutomatorConfigs(configurator=configurator),
)
```

## Tool Type

The tool type is the way used to interact with the device's UI. The possible
tool types are:

-   [TOOL_TYPE_UNKNOWN](https://developer.android.com/reference/android/view/MotionEvent#TOOL_TYPE_UNKNOWN)

-   [TOOL_TYPE_FINGER](https://developer.android.com/reference/android/view/MotionEvent#TOOL_TYPE_FINGER)

-   [TOOL_TYPE_STYLUS](https://developer.android.com/reference/android/view/MotionEvent#TOOL_TYPE_STYLUS)

-   [TOOL_TYPE_MOUSE](https://developer.android.com/reference/android/view/MotionEvent#TOOL_TYPE_MOUSE)

-   [TOOL_TYPE_ERASER](https://developer.android.com/reference/android/view/MotionEvent#TOOL_TYPE_ERASER)

```python
configurator = uiautomator.Configurator(
    tool_type=uiautomator.ToolType.TOOL_TYPE_FINGER
)
ad.services.register(
    uiautomator.ANDROID_SERVICE_NAME,
    uiautomator.UiAutomatorService,
    uiautomator.UiAutomatorConfigs(configurator=configurator),
)
```

## Raise Error

By default, Snippet UiAutomator uses a Boolean value to indicate whether an
operation is successful or not.

This behavior can be changed to raise an `errors.UiObjectSearchError` in
`exists`, `wait.exists`, and `wait.gone` APIs.

<section class="zippy" id="UiObjectSearchError">

Example Traceback

```
Details: [AndroidDevice|GOOG1234567890] Not found Selector{'res': 'X', 'enabled': False}
Traceback (most recent call last):
  File "/mobly/base_test.py", line 783, in exec_one_test
    test_method()
  File "/tests/uiobject2_test.py", line 50, in test_exists_when_target_not_exists_and_raised
    if self.ad.ui(res='X', enabled=False).exists:
  File "/snippet_uiautomator/uiobject2.py", line 534, in exists
    raise errors.UiObjectSearchError(
snippet_uiautomator.errors.UiObjectSearchError: [AndroidDevice|GOOG1234567890] Not found Selector{'res': 'X', 'enabled': False}
```

</section>

-   Set up when launched

    ```python
    ad.services.register(
        uiautomator.ANDROID_SERVICE_NAME,
        uiautomator.UiAutomatorService,
        uiautomator.UiAutomatorConfigs(raise_error=True),
    )
    ```

-   Change setting after launched

    ```python
    ad.ui.raise_error = True
    ```

-   One-time setting when calling API

    Note: Not support for `exists` API.

    ```python
    ad.ui(...).wait.exists(timeout, raise_error=True)
    ad.ui(...).wait.gone(timeout, raise_error=True)
    ```

## Skip Installing

By default, Snippet UiAutomator will install its latest apk. This process can
be skipped if Snippet UiAutomator is wrapped to your own apk and has already
installed to the phone.

```python
ad.services.register(
    uiautomator.ANDROID_SERVICE_NAME,
    uiautomator.UiAutomatorService,
    uiautomator.UiAutomatorConfigs(skip_installing=True),
)
```
