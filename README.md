Python Zillow
=============

A Python wrapper around the Zillow API.

By the [Python-Zillow Developers](<python-zillow@googlegroups.com>)


Introduction
------------

This library provides a Python interface for the [Zillow API](http://www.zillow.com/howto/api/APIOverview.htm). It works with Python versions from 2.6+.

[Zillow](www.zillow.com) provides a service that allows people to research the value of home across the United States. 
Zillow exposes this information via a web services API and this library is intended to make it easier for Python developers to use.


Installing
----------

You can install python-zillow using:

```shell
    pip install python-zillow
```

Getting the code
----------------

The code is hosted at https://github.com/seme0021/python-zillow

Check out the latest development version anonymously with::
```shell
    $ git clone git://github.com/seme0021/python-zillow.git
    $ cd python-zillow
```

Setup a virtual environment and install dependencies:

```shell
	$ virtualenv env
```

Activate the virtual environment created:

```shell
	$ source env/bin/activate
```

Running Tests
-------------
Note that tests require ```pip install nose``` and optionally ```pip install coverage```:

To run the unit tests:
```shell
	make test
```

to also run code coverage:

```shell
    make coverage
```