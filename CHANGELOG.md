# Snippet UiAutomator Release History

## 1.1.3:
* Support clicking on specific coordinate when registering a UiWatcher
* Support performing a swipe between points in the Point array
* Handle StaleObjectException raised from waiting for specific object appear/disappear
* Support Direct Boot mode

## 1.1.2:
* Support ancestor search in Selector
* Remove ineffectiveness Configurator settings
* Support gesture margin for default Scroll
* Support index search in child Selector

## 1.1.1:
* Migrate -jre flavor of Guava to -android flavor
* Fix the type of percent in scrollUntilFinished and scrollUntil

## 1.1.0:
* Update uiautomator lib to stable 2.3.0
* Print Mobly AndroidDevice object for better evaluated as a proper prefix
* Remove deprecated service registration method
* Add pytype hint to avoid Union[str, pathlib.Path]
* Include device debug tag when raising an error
* Refactor the way to get log path and dump to file
* Handle null value returned from QueryController.getCurrentPackageName
* Update the visibility of uiDevice in UiDeviceSnippet

## 1.0.5:

* Update androidx.test.uiautomator to 2.3.0-beta01
* Support KeyEvent in UiAutomator Python Lib
* Set default value for uiautomator configs and send warning message for deprecation notice
* Enable UiWatcher to monitor the condition without subsequent action

## 1.0.4:

* Handle NullPointerException throw from Until#scrollUntilFinished
* Fix sibling find the grandchildren object
* Implement UiAutomation.clearCache API
* Support updating gesture margin when scrolling
* Implement pause and resume in service
* Parse byte string before decoding to string
* Raise an error when uiautomation service has already registered

## 1.0.3: Improve selector search

* Add latest release version and testing result for apk and python build status
* Fix incorrect selector layer when using a serial of sub selectors
* Fix incorrect UiObject2 being found when using waitForExists and waitUntilGone on 2 or more layers of BySelector
* Fix Selector being overwritten when creating an instance of child UiObject2

## 1.0.2: Fix NullPointerException when calling UiObject2#getParent()

## 1.0.1: Use `typing.Mapping` in type annotations for compatibility to Python 3.6

## 1.0.0: Initial release
