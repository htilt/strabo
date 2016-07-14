Basic Markup for Sphinx
=======================

This is a *really* basic summary of how to write documentation using Sphinx. 

Workflow
--------
While in the ``strabo/docs/`` folder...

1. Create files with ``.rst`` extension and write documentation for classes, methods, etc., following ReStructuredText (RST) markup below.
2. Add filenames to ``index.rst`` under the main Table of Contents.
3. Save changes.
4. Type into terminal: ``make html``. (You can also type ``make clean`` to remove all of the previous _build files and ``make html`` to remake them. This is useful if changes aren't showing up, or if you have deleted a file.)
5. Visit the page on your local server to see the documentation in HTML. The local documentation will be in ``/_build/html/index.html``.
6. If everying looks right, push your changes to the master branch on GitHub.
7. Read the Docs should automatically update the documentation. Check it `here <http://strabo.readthedocs.io/en/latest/>`_.
8. Ta-da!


Python
------
The Sphinx autodoc extension should find most (if not all) of the Python files and their internal classes and functions. *Double check them anyway!* The autodoc extension is **not** working perfectly.

At the top of each file create a docstring that describes the main function of the file. For example: ::

  """ 
  This file prints the numbers 1 to 10. 
  """

You can also write docstrings (enclosed by triple-quotes) at the top of classes or methods. **Docstrings will show up on the final Sphinx document.** 

Block comments (begun with a #) will not show up on the final Sphinx document. Use these for programmer notes.

If a module, class, or function does not show up on the autodocumented page, you can manually include a docstring in the original file. Use this formatting: ::

	.. py:module:: name
	.. py:function:: name(parameters)
	.. py:class:: name(parameters)

You can see more at the official Sphinx documentation page for `Python <http://www.sphinx-doc.org/en/stable/domains.html#the-python-domain>`_.


JavaScript
----------
We will have to manually write the documentation for the JavaScript files.

Follow the Sphinx documentation page for `JavaScript <http://www.sphinx-doc.org/en/stable/domains.html#the-javascript-domain>`_ in order to document functions and classes. Specify that we are using the JavaScript domain by using `js`. 

An example: ::

	.. js:function:: count(x)

	   :param x: A number.
	   :returns: The sum of integers 0 to x.

Another example: ::

	.. js:class:: MyAnimal(name[, age])

	   :param string name: The name of the animal
	   :param number age: an optional age for the animal


reST
----
See `this page <http://www.sphinx-doc.org/en/stable/rest.html>`_ for the Sphinx reStructuredText Primer.
