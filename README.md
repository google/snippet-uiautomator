# Snippet UiAutomator

[![Latest release](https://img.shields.io/github/release/google/snippet-uiautomator.svg)](https://github.com/google/snippet-uiautomator/releases/latest)
[![APK Build Status](https://github.com/google/snippet-uiautomator/actions/workflows/apk.yml/badge.svg?branch=main)](https://github.com/google/snippet-uiautomator/actions)
[![Python Build Status](https://github.com/google/snippet-uiautomator/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/google/snippet-uiautomator/actions)

This is the Python wrapper based on
[Mobly Snippet Lib](https://github.com/google/mobly-snippet-lib) for calling the
[AndroidX UiAutomator](https://developer.android.com/reference/androidx/test/uiautomator/package-summary)
APIs.

## Requirements

-   Python 3.7+
-   Android 8.0+ (SDK 26+)

## Installation

```shell
pip install snippet-uiautomator
```

### Initial Mobly Android Controller

-   Inside Mobly Test

    To use in a Mobly test, the Android device needs to be initialized in the
    Mobly base test.

    ```python
    from mobly import base_test
    from mobly.controllers import android_device

    class MoblyTest(base_test.BaseTestClass):
      def setup_class(self):
        ad = self.register_controller(android_device)[0]
    ```

-   Outside Mobly Test

    If not using in a Mobly test, such as when running in a Python terminal, the
    Android device can be initialized with its serial number.

    ```python
    from mobly.controllers import android_device

    ad = android_device.AndroidDevice('GOOG1234567890')
    ```

To learn more about Mobly, visit
[Getting started with Mobly](https://github.com/google/mobly/blob/master/docs/tutorial.md).

### Launch UiAutomator Service

Snippet UiAutomator supports launching as one of
[Mobly Android Device Service](https://github.com/google/mobly/blob/master/docs/android_device_service.md).

```python
from snippet_uiautomator import uiautomator

ad.services.register(
    uiautomator.ANDROID_SERVICE_NAME, uiautomator.UiAutomatorService
)

ad.ui(text='OK').click()
```

## Test

Run unit tests for Python part:

```shell
pytest
```

Run tests for Snippet part:

```shell
cd snippet_uiautomator/android
./gradlew test
```

Set up pre-commit hooks, this will run some automated checks during each `git`
commit and possibly update some files that require changes:

```shell
pip install pre-commit
pre-commit install
```

## API Usage

- [Configurator](https://github.com/google/snippet-uiautomator/blob/main/docs/configurator.md)

- [Selector](https://github.com/google/snippet-uiautomator/blob/main/docs/selector.md)

- [UiDevice](https://github.com/google/snippet-uiautomator/blob/main/docs/uidevice.md)

- [UiObject2](https://github.com/google/snippet-uiautomator/blob/main/docs/uiobject2.md)

- [UiWatcher](https://github.com/google/snippet-uiautomator/blob/main/docs/uiwatcher.md)
