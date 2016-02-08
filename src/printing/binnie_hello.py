#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2016 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import base64

import colony

global manager
global plugins

manager.ensure(plugins.printing_manager)

HELLO_LANGUAGE = "<printing_document name=\"Hello World\" font=\"Calibri\" font_size=\"9\">"\
    "<paragraph><line><text text_align=\"center\">Hello World</text></line></paragraph>"\
"</printing_document>"
""" The (printing) language string containing the basics
for the printing of an hello world message """

# creates a string buffer to receive the binary contents
# of the processed print object
string_buffer = colony.legacy.BytesIO()

# creates the printing options map
printing_options = dict(
    printing_name = "binie",
    file = string_buffer
)

try:
    # prints the template with the printing manager plugin, this should generate
    # the binary contents representing the printing operations (in binie format),
    # then reads the string buffer to retrieve the contents
    plugins.printing_manager.print_printing_language(HELLO_LANGUAGE, printing_options)
    string_buffer.seek(0)
    printing_contents = string_buffer.read()
finally:
    # closes the string buffer
    string_buffer.close()

# encodes the printing contents into base 64 data and
# then prints the value
printing_contents_b64 = base64.b64encode(printing_contents)
print(printing_contents_b64)
