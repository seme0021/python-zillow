Python-Zillow
=============

A Python wrapper around the Zillow API.

By the [Python-Zillow Developers](mailto:python-zillow@googlegroups.com)


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


Basic Tutorial on Searching Zillow
----------------------------------

Here is some basic python code to query the zillow api using the python-zillow library.

Note: I suggest keeping your key stored in a ./bin/config/zillow_key.conf file

### Initialize the API

```python
import zillow

with open("./bin/config/zillow_key.conf", 'r') as f:
    key = f.readline().replace("\n", "")

api = zillow.ValuationApi()
```

### Find a place given an address

```python
address = "3400 Pacific Ave., Marina Del Rey, CA"
postal_code = "90292"

data = api.GetSearchResults(key, address, postal_code)
```

### Find place using a zillow place id

```python
zpid="2100641621"
detail_data = api.GetZEstimate(key, zpid)
```

### Find comparables
```python
zpid="2100641621"
detail_data = api.GetComps(key, zpid)
```

### Get Deep Search Results
```python
address = "3400 Pacific Ave., Marina Del Rey, CA"
postal_code = "90292"

data = api.GetDeepSearchResults(key, address, postal_code)
```

### Get Deep Comps
```python
zws_id = "<your key>"
zpid = 2100641621
count=10

data = data = api.GetDeepComps(zws_id, zpid, count)
```
