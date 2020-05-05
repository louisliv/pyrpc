
pyrpc
-----

Pyrpc is a Django app to handle JSON Remote Procedure Calls 
using Django Rest Framework. 

Installation
^^^^^^^^^^^^

``pip install pyrpc-django``

Quick Setup
^^^^^^^^^^^


1. 
   Add ``rest_framework`` ``pyrpc``\ to your INSTALLED_APPS setting like this:

   .. code-block::

       INSTALLED_APPS = [
           ...
           'rest_framework',
           'pyrpc',
       ]

2. 
   Add the ``safe_method`` decorator to methods in your app.

.. code-block::

   from pyrpc.decorators import safe_method

   @safe_method
   def return_cat_string(*args, **kwargs):
       """ 
       Returns a concatenated string. 
       Extended description of function. 

       @param args: List of strings
       @returns: Concatenated string
       """

       result = ''
       for arg in args:
           result = result + arg
       return result


   class Library():
       @safe_method
       def sum_two_numbers(self, operand1=0, operand2=0):
           """ 
           Returns the sum of two numbers. 
           Extended description of function. 

           @param operand1: Can be any float number.
           @param operand2: Can be any float number.
           @returns: operand1 + operand2. 
           """
           return operand1 + operand2

       @safe_method
       def multiply_two_numbers(self, operand1=0, operand2=0):
           """ 
           Returns the product of two numbers. 
           Extended description of function.

           @param operand1: Can be any float number.
           @param operand2: Can be any float number.
           @returns: operand1 * operand2. 
           """
           return operand1 * operand2


3. Add pyrpc urls to ``urls.py``

.. code-block::

   from django.urls import path
   from django.conf.urls import include
   from pyrpc.urls import urls as pyrpc_urls

   urlpatterns = [
       path('api/', include(pyrpc_urls)),
   ]


4. Start the server: ``python manage.py runserver``

Sending Requests
^^^^^^^^^^^^^^^^


1. Using the above example, POST the folowing JSON to ``127.0.0.1:8000/api/methods/``.

.. code-block::

   {
       "id": 1,
       "jsonrpc": "2.0",
       "method": "sum_two_numbers",
       "params": {
           "args": [],
           "kwargs": {
               "operand1": 5,
               "operand2": 6
           }
       }
   }


2. A JSON response should be returned similar to the folowing:

.. code-block::

   {
       "id": 1,
       "jsonrpc": "2.0",
       "result": 11
   }

Returning a List of Methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^


1. Using the previous example, send a GET request to ``127.0.0.1:8000/api/methods``.
2. A list of methods and their descriptions shold be returned as follows:

.. code-block::

   [
       {
           "name": "multiply_two_numbers",
           "kwargs": {
               "operand1": "Can be any float number.",
               "operand2": "Can be any float number."
           },
           "description": [
               "Returns the product of two numbers.",
               "Extended description of function."
           ],
           "returns": "operand1 * operand2."
       },
       {
           "name": "sum_two_numbers",
           "kwargs": {
               "operand1": "Can be any float number.",
               "operand2": "Can be any float number."
           },
           "description": [
               "Returns the sum of two numbers.",
               "Extended description of function."
           ],
           "returns": "operand1 + operand2."
       }
   ]
