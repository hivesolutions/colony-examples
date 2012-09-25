#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import json
import urllib
import urllib2

BASE_URL = "http://localhost:8080/dynamic/rest/mvc/"
""" The base url to be used in the communication
to the omni service """

class ApiError(Exception):
    """
    Error class to be used to encapsulate
    the decoded json information resulting
    from the raising of an omni api error.
    """

    json_data = None
    """ The map containing the information on
    the exception """

    def __init__(self, json_data):
        """
        Constructor of the class.

        @type json_data: Dictionary
        @param json_data: The map containing the information
        on the remote (api) exception.
        """

        self.json_data = json_data

    def _print(self):
        """
        Prints information on the exception to the
        standard output file.
        """

        exception = self.json_data.get("exception", {})
        exception_name = exception.get("exception_name", "NoName")
        message = exception.get("message", "No message")
        traceback = exception.get("traceback", ())

        print "%s - %s" % (exception_name, message)
        print "--------------"
        for line in traceback:
            print line.strip()

def get_vat(vat_name):
    parameters = {
        "filters[]" : "identifier:equals:%s" % vat_name
    }
    return get_first_json("omni/vat_classs.json", parameters)

def create_products(products):
    payload = {
        "product" : products
    }
    return post_json("omni/products.json", payload)

def get_session_id():
    return "41ff2fe77749753d96db9483f36e9b4d"

def handle_error(error):
    data = error.read()
    json_data = json.loads(data)
    raise ApiError(json_data)

def get_first_json(path, parameters = None):
    json_data = get_json(path, parameters)
    if not json_data: return json_data
    return json_data[0]

def get_json(path, parameters = None):
    try: response = get_data(path, parameters)
    except urllib2.HTTPError, error: handle_error(error)
    response_json = json.loads(response)
    return response_json

def post_json(path, json_data, parameters = None):
    data = json.dumps(json_data)
    try: response = post_data(path, parameters, data)
    except urllib2.HTTPError, error: handle_error(error)
    response_json = json.loads(response)
    return response_json

def get_data(path, parameters = None):
    parameters = parameters or {}
    parameters["session_id"] = get_session_id()
    parameters = urllib.urlencode(parameters, True)
    url = BASE_URL + path + "?" + parameters

    file = urllib2.urlopen(url)
    try: response = file.read()
    finally: file.close()
    return response

def post_data(path, parameters = None, data = None):
    parameters = parameters or {}
    parameters["session_id"] = get_session_id()
    parameters = urllib.urlencode(parameters, True)
    url = BASE_URL + path + "?" + parameters
    headers = {
        "Content-Type": "application/json"
    }

    request = urllib2.Request(url, data, headers)
    file = urllib2.urlopen(request)
    try: response = file.read()
    finally: file.close()
    return response

try:
    products = (
        {
            "company_product_code" : "12312543sad64563123",
            "name" : "123123123",
            "vat_class" : {}
        }, {
            "company_product_code" : "12341234asd13456234",
            "name" : "123412341234",
            "vat_class" : {}
        }
    )

    vat = get_vat("IVA23")
    for product in products:
        product["vat_class"] = vat
    create_products(products)
except ApiError, error:
    error._print()
