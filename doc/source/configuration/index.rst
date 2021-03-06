..
      Copyright 2011 OpenStack Foundation
      All Rights Reserved.

      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

.. _configuration:

Designate Configuration Guide
=============================

Designate configuration is needed for getting it work correctly
either with real OpenStack environment or without OpenStack environment.

**NOTE:** The most of the following operations should performed in designate
directory.

.. index::
    double: configure; designate

#. Create the designate.conf file

    ::

      $ editor designate.conf

#. Copy or mirror the configuration from this sample file here:

    .. literalinclude:: ../examples/basic-config-sample.conf
        :language: ini

#. You can generate full sample *designate.conf* (if it does not already exist)::

    $ oslo-config-generator --config-file etc/designate/designate-config-generator.conf --output-file /etc/designate/designate.conf

.. literalinclude:: ../_static/designate.conf.sample
    :language: ini
