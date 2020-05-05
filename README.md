## pyrpc

Pyrpc is a Django app to handle JSON Remote Procedure Calls 
using Django Rest Framework. 

## Installaltion

`pip install pyrpc-django`

## Quick Setup

1. Add `rest_framework` `pyrpc`to your INSTALLED_APPS setting like this::
```
    INSTALLED_APPS = [
        ...
        'rest_framework',
        'pyrpc',
    ]
  ```
  
2. Add the `safe_method` decorator to class methods in your app.

```
from pyrpc.decorators import safe_method


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
```

3. Create the view in `<YOUR_APP>.views.py`. Make sure to add

```
from django.shortcuts import render
from pyrpc.views import MethodViewSet
from <YOUR_APP>.methods import Library


class LibraryViewSet(MethodViewSet):
    method_class = Library
```

4. Add your view to a `djangorestframework` router in `urls`

```
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from <YOUR_APP>.views import LibraryViewSet

router = routers.DefaultRouter()
router.register(r'methods', LibraryViewSet, basename="methods")

urlpatterns = [
    path('api/', include(router.urls)),
]
```

5. Start the server: `python manage.py runserver`

## Sending Requests

1. Using the above example, POST the folowing JSON to `127.0.0.1:8000/api/methods/`.

```
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
```

2. A JSON response should be returned similar to the folowing:

```
{
    "id": 1,
    "jsonrpc": "2.0",
    "result": 11
}
```

## Returning a List of Methods

1. Using the previous example, send a GET request to `127.0.0.1:8000/api/methods`.
2. A list of methods and there descriptions shold be returned as follows:

```
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
```
