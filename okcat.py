#!/usr/bin/python -u

"""
Copyright (C) 2017 Jacksgong(blog.dreamtobe.cn)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import argparse

from utils.adb import Adb
from utils.helper import LOG_LEVELS, is_path
from utils.logfile_parser import LogFileParser

__author__ = 'JacksGong'
__version__ = '1.0.0'
__description__ = 'This python script used for combine several Android projects to one project.'

print("-------------------------------------------------------")
print("OkCat v" + __version__)
print("-------------------------------------------------------")

parser = argparse.ArgumentParser(description='Filter logcat by package name')
parser.add_argument('package_or_path', nargs='*',
                    help='This can be Application package name(s) or log file path(if the file from path is exist)')
parser.add_argument('-y', '--yml_file_name', dest='yml', help='Using yml file you config on ~/.okcat folder')

# following args are just for parser
# parser.add_argument('-k', '--keyword', dest='keyword', action='append', help='You can filter you care about log by this keyword(s)')

# following args are just for adb
parser.add_argument('-w', '--tag-width', metavar='N', dest='tag_width', type=int, default=23,
                    help='Width of log tag')
parser.add_argument('-l', '--min-level', dest='min_level', type=str, choices=LOG_LEVELS + LOG_LEVELS.lower(),
                    default='V', help='Minimum level to be displayed')
parser.add_argument('--color-gc', dest='color_gc', action='store_true', help='Color garbage collection')
parser.add_argument('--always-display-tags', dest='always_tags', action='store_true',
                    help='Always display the tag name')
parser.add_argument('--current', dest='current_app', action='store_true',
                    help='Filter logcat by current running app')
parser.add_argument('-s', '--serial', dest='device_serial', help='Device serial number (adb -s option)')
parser.add_argument('-d', '--device', dest='use_device', action='store_true',
                    help='Use first device for log input (adb -d option)')
parser.add_argument('-e', '--emulator', dest='use_emulator', action='store_true',
                    help='Use first emulator for log input (adb -e option)')
parser.add_argument('-c', '--clear', dest='clear_logcat', action='store_true',
                    help='Clear the entire log before running')
parser.add_argument('-t', '--tag', dest='tag', action='append', help='Filter output by specified tag(s)')
parser.add_argument('-tk', '--tag_keywords', dest='tag_keywords', action='append',
                    help='Filter output by specified tag keyword(s)')
parser.add_argument('-i', '--ignore-tag', dest='ignored_tag', action='append',
                    help='Filter output by ignoring specified tag(s)')
parser.add_argument('-a', '--all', dest='all', action='store_true', default=False,
                    help='Print all log messages')

args = parser.parse_args()

file_path = None
candidate_path = args.package_or_path
if candidate_path is not None and len(candidate_path) > 0 and is_path(candidate_path[0]):
    file_path = candidate_path[0]

if file_path is None:
    adb = Adb()
    adb.setup(args)
    while True:
        try:
            adb.loop()
        except KeyboardInterrupt:
            break
else:
    parser = LogFileParser(file_path)
    parser.setup(args.yml)
    print parser.parse()