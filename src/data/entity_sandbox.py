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

global plugins

DATABASE_PATH = "database.db"
""" The path to the database to be used in the
testing, note that this will be a sqlite database """

PARAMETERS = {
    "file_path" : DATABASE_PATH
}
""" The map containing the parameters to be sent
to the entity manager for the configuration the engine """

def start_em():
    """
    Creates a new entity manager structure/object and
    initializes it with the mock entities.

    The initialization of the entity manager is done
    according to the globally defined values.

    @rtype: EntityManager
    @return: The entity manager object that was created
    and initialized in this function.
    """

    # loads the entity manager and sets the connection
    # parameters according to the specification
    em = plugins.entity_manager.load_entity_manager("sqlite")
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
    except: em.rollback()
    else: em.commit()

    # returns the initialized entity manager structure
    # to the caller function
    return em

def stop_em(em, destroy = True):
    """
    Stops the entity manager destroying the underlying
    structures in case the flag is set.

    @type em: EntityManager
    @param em: The entity manager to be stopped.
    @type destroy: bool
    @param destroy: If the underlying data structure should
    be destroyed (deleted).
    """

    # destroys the underlying data source, removes
    # all files and structures associated with the
    # current entity manager context
    destroy and em.destroy()

def create_structures(em):
    mocks = em.get_mock_entities()

    car = mocks.Car()
    car.tires = 3
    em.save(car)

    person = mocks.Employee()
    person.name = "João Magalhães"
    person.salary = 1200
    person.cars = [car]
    em.save(person)

em = start_em()
create_structures(em)
#stop_em(em)
