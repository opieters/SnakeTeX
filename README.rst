SnakeTeX
========

A LaTeX template system for large and multi-user projects.

Requirements and Installation
-----------------------------

-  Python3
-  `jinja2 <http://jinja.pocoo.org>`__: ``pip3 install jinja2``
-  `TeXLive <https://www.tug.org/texlive/>`__ 2016 (or derivate)

Install SnakeTeX with pip3: ``pip3 install snaketex``.

Documentation
-------------

TODO.

FAQ
---

Will there be Python (2.6 and 2.7) support?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No. Python3 is the future of the Python language. Real all about the
2vs3 debate on the official `Python
wiki <https://wiki.python.org/moin/Python2orPython3>`__.

Will pre-2016 TeXLive distributions be supported?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No. The TeXLive 2016 distribution introduced the ``SOURCE_DATE_EPOCH``
environment variable. This variable pre-sets the date and time, allowing
to check if successive build produce the same PDF.
