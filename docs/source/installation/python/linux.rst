.. _sec:lin:

=======
 Linux
=======

*These instruction are for Ubuntu or other Debian-based distributions.
The setup for other Linux distributions should be adapted accordingly.*

.. _sec-lin:python:

Python
------

.. _sec-lin:checking-if-python:

Checking if python exists
~~~~~~~~~~~~~~~~~~~~~~~~~

Before installing please check if you already have python installed on
your computer. To do so open terminal application. Once terminal is open
execute the following commands,

.. code:: bash

   $ python -V

.. code:: bash

   $ python3 -V

If either of them return ``Python 3`` then you can skip the Python
installation section and continue with the rest.

.. _sec-lin:installation-python:

Installation
~~~~~~~~~~~~

To download and install Python use the link :

-  Open terminal application

-  Execute the following command:

   .. code:: bash

      $ sudo apt-get install python3

   The above command will ask you to enter your system password before
   beginning the installation process.

After installation to verify if everything is working open terminal
again and run the commands in section
`4.1.1 <#sec-lin:checking-if-python>`__.

.. _sec-lin:pip:

Pip
---

Python has a huge repository of packages that are widely used for
different functions. In order to obtain these packages there are several
package managers. The one we will be using during this course will be
the official package installer for Python called :math:`pip`.

.. _sec-lin:checking-if-pip:

Checking if pip exists
~~~~~~~~~~~~~~~~~~~~~~

If you installed Python based on the instructions above then pip should
be installed by default. Or it may have been already installed on your
computer if Python had been pre-installed. To check if pip exists, open
terminal and execute the following command:

:math:`pip` or :math:`pip3` depends on your system. Typically they
differentiate ones installed with python2 and python3 respectively.

.. code:: bash

   $ pip --version

.. code:: bash

   $ pip3 --version

If :math:`pip` is already installed then at least one of the above
commands should print the version of the pip along with the python and
its version associated with it. **Make sure that the python version is 3**

.. _sec-lin:installation-pip:

Installation
~~~~~~~~~~~~

If you have verified that pip is not installed on your computer then in
order to install pip you are expected to have either cloned or
downloaded the exercise repository by now.

-  Open terminal application

-  Execute the following command:

   .. code:: bash

      $ sudo apt-get install python3-pip

Check if you have installed everything correctly by referring to
`4.2.1 <#sec-lin:checking-if-pip>`__.

.. _sec-lin:spyder:

Spyder
------

Python programs can be written and run in several ways, it can be simply
done on a terminal by running *python* or *ipython*. While this method
is limited for simple programs, larger programs will be written using a
text-editor or an Integrated Development Environment (IDE). Though it is
not necessary to have an IDE for programming in Python, having one will
bring many features that are useful while starting new

.. _sec-lin:installation-spyder:

Installation
~~~~~~~~~~~~

-  Open terminal

-  Next, install spyder with the command:

   .. code:: bash

      $ pip install spyder

   or

   .. code:: bash

      $ pip3 install spyder

.. _seclin:checking-if-spyder:

Checking spyder
~~~~~~~~~~~~~~~

To check if spyder is installed, execute the following command from a
terminal

.. code:: bash

   $ spyder3

If everything is working then Spyder IDE should open and you are ready
to begin with the exercises.


Requirements
------------

The final step before starting of with the exercise is to install a few
necessary packages. We will be using pip to this.

-  Open terminal (Git Bash on Windows)

-  Navigate in the terminal to the exercise repository on your computer

-  Execute the following command once you are in the root of the
   repository:

   .. code:: bash

      $ pip install -r requirements.txt

   or

   .. code:: bash

      $ pip3 install -r requirements.txt

   Use :math:`pip` or :math:`pip3` depending on the one that refers to python3


The *requirements.txt* installs the following packages:

-  numpy : Scientific computing package for python

-  matplotlib : Matlab like plotting tool for python

-  farms_pylog : Module for logging messages during code runtime

After successfully completing the installation steps in the previous
sections, you can now get started with programming Lab0. Python
is not just a computational tool but a very powerful programming
language. This means having to learn a few more extra concepts to get
your job done. There are a ton of references available online for those
who are interested in learning Python in depth. We will try to provide
the necessary references to help with the concepts that are useful
during the course as and when needed.
