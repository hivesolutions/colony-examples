#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

global manager
global plugins

manager.ensure(plugins.entity_manager)

DESTROY_DATABASE = False
""" Flag that controls if the database should be
destroyed at the end of the execution """

DATABASE_PATH = "database.db"
""" The path to the database to be used in the
testing, note that this will be a sqlite database """

DATABASE_NAME = "sandbox"
""" The name of the database to be used in the
testing operations """

USERNAME = "root"
""" The username to be used in case a remote database
connection is meant to be used """

PASSWORD = "root"
""" The password to be used in case a remote database
connection is meant to be used """

ENGINE_NAME = "mysql"
""" The name of the engine to be used in case no other
is specified """

HOST = "db"
""" The host of the database management system to be used
for remote connections """

PARAMETERS = {
    "file_path" : DATABASE_PATH,
    "database" : DATABASE_NAME,
    "username" : USERNAME,
    "password" : PASSWORD,
    "host" : HOST
}
""" The map containing the parameters to be sent
to the entity manager for the configuration the engine """

def start_em():
    """
    Creates a new entity manager structure/object and
    initializes it with the mock entities.

    The initialization of the entity manager is done
    according to the globally defined values.

    :rtype: EntityManager
    :return: The entity manager object that was created
    and initialized in this function.
    """

    # loads the entity manager and sets the connection
    # parameters according to the specification
    em = plugins.entity_manager.load_entity_manager(ENGINE_NAME)
    em.set_connection_parameters(PARAMETERS)

    # retrieves the mock entities from the entity manager
    # instance and uses them to extend the manager
    mocks = em.get_mock_entities()
    em.extend_module(mocks)

    # opens the entity manager and creates the generator
    # processes
    em.open(start = False)
    em.create_generator()

    # creates a new transaction and inside it creates the
    # various definitions for the entity manager
    em.begin()
    try: em.create_definitions()
    except: em.rollback(); raise
    else: em.commit()

    # returns the initialized entity manager structure
    # to the caller function
    return em

def stop_em(em, destroy = True):
    """
    Stops the entity manager destroying the underlying
    structures in case the flag is set.

    :type em: EntityManager
    :param em: The entity manager to be stopped.
    :type destroy: bool
    :param destroy: If the underlying data structure should
    be destroyed (deleted).
    """

    # closes the entity manager releasing all it's
    # internal data structures
    em.close()

    # destroys the underlying data source, removes
    # all files and structures associated with the
    # current entity manager context
    destroy and em.destroy()

def create_structures(em):
    # retrieves the complete set of mock entities
    # to use them in the construction of new ones
    mocks = em.get_mock_entities()

    # creates a new car entity and saves it in the
    # entity manager's data source
    car = mocks.Car()
    car.tires = 3
    em.save(car)

    # creates a new employee entity and saves it in the
    # entity manager's data source
    employee = mocks.Employee()
    employee.name = "João Magalhães"
    employee.salary = 1200
    employee.cars = [car]
    em.save(employee)

def retrieve_structures(em):
    # retrieves the complete set of mock entities
    # to used them for retrieval and creation
    mocks = em.get_mock_entities()

    # creates a new employee entity and saves it in the
    # entity manager's data source
    employee = mocks.Employee()
    employee.name = "João Magalhães"
    employee.salary = 1200
    em.save(employee)

    # retrieves the person object using the just saved
    # employee object id and then tries to access an
    # employee level attribute, this access should trigger
    # the loading of the underlying layers
    person = em.get(mocks.Person, employee.object_id)
    print(person.salary)

def call_transaction(em, callable):
    em.begin()
    try: callable(em)
    except: em.rollback(); raise
    else: em.commit()

def execute():
    em = start_em()
    try:
        call_transaction(em, create_structures)
        call_transaction(em, retrieve_structures)
    finally:
        stop_em(em, destroy = DESTROY_DATABASE)

execute()
