# Snippet UiAutomator Release History

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
