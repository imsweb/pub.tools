formatting
==========

Helper functions. `format_date` will take year/month/day values or a `medlinedate` value
and represent it as a datetime object. The `medlinedate` value is particularly useful for representing
odd date ranges like `Spring 2007` as a datetime object, so that you can sort on that value without changing the
date in the citation. `format_date_str` interprets a string representing a date in several possible formats and
returns a standardized format. See examples below on using these two functions together.

.. currentmodule:: pub.tools.formatting

format_date
---------------

.. autofunction:: format_date


examples:

.. code-block:: python

   >>> formatting.format_date(medlinedate='Spring 2008')
   datetime.datetime(2008, 4, 1, 0, 0)
   >>> formatting.format_date(medlinedate=formatting.format_date_str('11-02-2007'))
   datetime.datetime(2007, 11, 2, 0, 0)
   >>> formatting.format_date(medlinedate=formatting.format_date_str('Nov 2 2007'))
   datetime.datetime(2007, 11, 2, 0, 0)

format_date_str
---------------

.. autofunction:: format_date_str
   :no-index:

examples:

.. code-block:: python

   >>> formatting.format_date_str('Spring 2008')
   '2008 Spring'
   >>> formatting.format_date_str('11-02-2007')
   '2007 Nov 2'
   >>> formatting.format_date_str('Nov 2 2007')
   '2007 Nov 2'
