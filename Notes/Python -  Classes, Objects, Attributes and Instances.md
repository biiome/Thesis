# Python - Classes, Objects, Attributes and Instances
---
## Class Setup
```python
class Dog:
	def __init__(self, name, age, puppies):
		self.name = name
		self.age = age
		self.puppies = puppies

	def birthday(self):
		self.age += 1

	def have_puppies(self, number_puppies):
		self.have_puppies += number_puppies
```
- Here we have a **Dog** `class` with the instance attributes of of `name` `age` and `puppies` 
- The class also has the `methods` of `birthday()` and `have_puppies` 

- We create and instance of the class with the following:
```python
teddy = Dog(name='Teddy', age='7', puppies='0')
```

## Accessing Instance Attributes
- To access the the object's instance attributes by suffixing the name of the attribute to the object:
```python
print(teddy.name)

"""
Returns: Teddy
"""
```

## Seeing All Attributes
- One of the easiest ways to access a Python object’s attributes is the `dir()` function
```python
print(dir(teddy))

"""
Returs:
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'age', 'birthday', 'have_puppies', 'name', 'puppies']
"""
```
