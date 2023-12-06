# Copyright 2023 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Installs Snippet UiAutomator."""

import setuptools

setuptools.setup(
    name='snippet-uiautomator',
    version='1.0.4',
    author='Kolin Lu',
    author_email='kolinlu@google.com',
    description='A Python wrapper for UiAutomator based on Mobly Snippet Lib.',
    license='Apache2.0',
    url='https://github.com/google/snippet-uiautomator',
    packages=['snippet_uiautomator'],
    package_data={'snippet_uiautomator': ['android/app/uiautomator.apk']},
    install_requires=['mobly'],
    python_requires='>=3.7',
    keywords='uiautomator',
)
