from pathlib import Path

# content = r'''"""
# Advanced Python Concepts — Consolidated Examples
# ================================================

# How to use:
# 1. Save/run with Python 3.12+ for every example, because Example 23 uses
#    the newer type-parameter syntax. Most examples work on Python 3.11+.
# 2. Each example is independent in concept. Some examples intentionally
#    demonstrate exceptions or runtime-dependent output.
# 3. Explanations and representative outputs are included as comments.
# 4. For examples that intentionally raise exceptions, the exception is caught
#    so the whole file can continue running.

# Note:
# - Bytecode, timings, garbage-collection counts, and some introspection details
#   can vary by Python version and environment.
# - Pickle must never be used to load untrusted data.
# """

# ============================================================
# 1. Metaclasses
# ============================================================

# Example 1A: Understanding type
class Car:
    pass


my_car = Car()

print(type(my_car))
print(type(Car))
print(type(type))

# Output:
# <class '__main__.Car'>
# <class 'type'>
# <class 'type'>
#
# Explanation:
# - my_car is an instance of Car.
# - Car is an instance of type.
# - type is itself an instance of type.


# What __slots__ is for
# __slots__ is used to control what instance attributes a class can have.

# Without it, Python creates a per-instance __dict__, which allows dynamic attributes like:

# With __slots__, you restrict attributes to a fixed set:

class Person:
    __slots__ = ("name", "age")

    def __init__(self, name, age):
        self.name = name
        self.age = age



p = Person()
p.age = 30
# Now Person instances can only have name and age as instance attributes.
# Why it matters
# __slots__ can:

# reduce memory usage
# prevent accidental creation of arbitrary attributes
# make the class layout more explicit

# Example 1B: Creating a class dynamically
def start(self):
    return "Car started"


DynamicCar = type("DynamicCar", (), {"start": start})
my_dynamic_car = DynamicCar()
print(my_dynamic_car.start())
print(type(my_dynamic_car))

# Output:
# Car started
#
# Explanation:
# - type(name, bases, namespace) creates a class at runtime.
# - The namespace dictionary supplies the class's attributes and methods.


# Example 1C: Custom metaclass that uppercases public attribute names
# In Python, __new__ is the constructor, and __init__ is the initializer. 
# When you call a class like MyClass(), Python secretly calls __new__ first 
# to build the empty object, and then hands that object over to __init__ to set up its initial values.
#__new__  Runs first. __init__ Runs second (only if __new__ returns an instance of the same class
# if the __new__ method returns an instance of the different class then __init__ is not called).

class UppercaseMeta(type):
    def __new__(mcls, name, bases, namespace):
        new_namespace = {}
        for key, value in namespace.items():
            if not key.startswith("__"):
                new_namespace[key.upper()] = value
            else:
                new_namespace[key] = value
        return super().__new__(mcls, name, bases, new_namespace)


class Vehicle(metaclass=UppercaseMeta):
    wheels = 4


print(Vehicle.WHEELS)
# # Output:
# # 4
# #
# # Explanation:
# # - The metaclass changes the class namespace before creating the class.
# # - The attribute "wheels" becomes "WHEELS".

# Difference between class attribute and instance attribute
# Class attribute: shared by all instances
# Instance attribute: stored in each object
class Vehicle:
    wheels = 4
v = Vehicle()
print(v.wheels)     # 4
print(Vehicle.wheels)  # 4
#This works because Python looks up wheels on the instance, then on the class if not found there.




# ============================================================
# 2. Descriptors and the Descriptor Protocol
# ============================================================

class PositiveNumber:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name, 0)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Value must be non-negative")
        setattr(instance, self.name, value)


class Engine:
    horsepower = PositiveNumber()


engine = Engine()
engine.horsepower = 150
print(engine.horsepower)

try:
    engine.horsepower = -10
except ValueError as exc:
    print(type(exc).__name__ + ":", exc)

# Output:
# 150
# ValueError: Value must be non-negative
#
# Explanation:
# - __set__ intercepts assignment and validates the value.
# - __get__ intercepts attribute access.
# - __set_name__ tells the descriptor which attribute name it manages.


# # ============================================================
# # 3. Python Data Model and Special Methods
# # ============================================================

# class Money:
#     def __init__(self, amount):
#         self.amount = amount

#     def __add__(self, other):
#         if not isinstance(other, Money):
#             return NotImplemented
#         return Money(self.amount + other.amount)

#     def __str__(self):
#         return f"₹{self.amount}"


# a = Money(100)
# b = Money(250)
# print(a + b)

# # Output:
# # ₹350
# #
# # Explanation:
# # - __add__ defines how the + operator works for Money objects.
# # - __str__ defines the readable string representation.


# # ============================================================
# # 4. Method Resolution Order (MRO) and C3 Linearization
# # ============================================================

# class A:
#     def show(self):
#         print("A")


# class B(A):
#     def show(self):
#         print("B")


# class C(A):
#     def show(self):
#         print("C")


# class D(B, C):
#     pass


# obj = D()
# obj.show()
# print([cls.__name__ for cls in D.__mro__])

# # Output:
# # B
# # ['D', 'B', 'C', 'A', 'object']
# #
# # Explanation:
# # - Python searches methods using the class's MRO.
# # - B comes before C in D's inheritance order, so B.show() runs first.


# # ============================================================
# # 5. Multiple Inheritance and Cooperative super()
# # ============================================================

# class AProcess:
#     def process(self):
#         print("A")
#         super().process()


# class BProcess(AProcess):
#     def process(self):
#         print("B")
#         super().process()


# class CProcess(AProcess):
#     def process(self):
#         print("C")
#         super().process()


# class EndProcess:
#     def process(self):
#         print("End")


# class DProcess(BProcess, CProcess, EndProcess):
#     pass


# DProcess().process()

# # Output:
# # B
# # C
# # A
# # End
# #
# # Explanation:
# # - super() follows the next class in the MRO, not simply a fixed parent.
# # - All participating methods cooperate to continue the method chain.


# # ============================================================
# # 6. Closures and Late Binding
# # ============================================================

# def make_counter():
#     count = 0

#     def increment():
#         nonlocal count
#         count += 1
#         return count

#     return increment


# counter = make_counter()
# print(counter())
# print(counter())
# print(counter())

# # Output:
# # 1
# # 2
# # 3
# #
# # Explanation:
# # - The inner function retains access to count after make_counter returns.
# # - nonlocal allows increment() to update the enclosing variable.


# # Late-binding example
# functions = []
# for i in range(3):
#     functions.append(lambda: i)

# print([f() for f in functions])

# # Output:
# # [2, 2, 2]
# #
# # Explanation:
# # - All lambdas refer to the same loop variable i.
# # - They look up its value when called, after the loop has ended.


# # Fixing late binding with a default argument
# functions = []
# for i in range(3):
#     functions.append(lambda i=i: i)

# print([f() for f in functions])

# # Output:
# # [0, 1, 2]
# #
# # Explanation:
# # - Each lambda's default argument stores the current value of i.


# # ============================================================
# # 7. Decorators with Arguments and Nested Decorators
# # ============================================================

# import time
# from functools import wraps


# def retry(attempts):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             for attempt in range(attempts):
#                 try:
#                     return func(*args, **kwargs)
#                 except ValueError:
#                     if attempt == attempts - 1:
#                         raise
#                     time.sleep(0.01)
#         return wrapper
#     return decorator


# attempt_counter = {"count": 0}


# @retry(attempts=3)
# def sometimes_fails():
#     attempt_counter["count"] += 1
#     print("Attempt", attempt_counter["count"])
#     if attempt_counter["count"] < 3:
#         raise ValueError("Temporary failure")
#     return "Success"


# print(sometimes_fails())

# # Output:
# # Attempt 1
# # Attempt 2
# # Attempt 3
# # Success
# #
# # Explanation:
# # - retry(3) configures the decorator.
# # - decorator receives the original function.
# # - wrapper runs the function and retries after ValueError.


# # ============================================================
# # 8. Generators, yield, and yield from
# # ============================================================

# def numbers():
#     print("Start")
#     yield 10
#     print("Continue")
#     yield 20
#     print("Finish")


# g = numbers()
# print(next(g))
# print(next(g))

# # Output:
# # Start
# # 10
# # Continue
# # 20
# #
# # Explanation:
# # - A generator suspends at yield and resumes on the next request.
# # - "Finish" would print only if the generator were advanced again.


# def inner():
#     yield 1
#     yield 2


# def outer():
#     yield 0
#     yield from inner()
#     yield 3


# print(list(outer()))

# # Output:
# # [0, 1, 2, 3]
# #
# # Explanation:
# # - yield from delegates iteration to another iterable or generator.


# # ============================================================
# # 9. Coroutines and Asynchronous Generators
# # ============================================================

# import asyncio


# async def fetch_data():
#     await asyncio.sleep(0.01)
#     return {"status": "success"}


# async def coroutine_demo():
#     result = await fetch_data()
#     print(result)


# asyncio.run(coroutine_demo())

# # Output:
# # {'status': 'success'}
# #
# # Explanation:
# # - async def defines a coroutine function.
# # - await suspends the current coroutine while the awaited operation is pending.


# async def stream_data():
#     for number in range(3):
#         await asyncio.sleep(0.01)
#         yield number


# async def async_generator_demo():
#     async for item in stream_data():
#         print(item)


# asyncio.run(async_generator_demo())

# # Output:
# # 0
# # 1
# # 2
# #
# # Explanation:
# # - An asynchronous generator yields values over time.
# # - async for consumes an asynchronous iterator.


# # ============================================================
# # 10. asyncio Event Loop and Task Scheduling
# # ============================================================

# async def scheduled_task(name, delay):
#     print(f"{name} started")
#     await asyncio.sleep(delay)
#     print(f"{name} finished")


# async def scheduling_demo():
#     await asyncio.gather(
#         scheduled_task("A", 0.02),
#         scheduled_task("B", 0.01),
#     )


# asyncio.run(scheduling_demo())

# # Typical output:
# # A started
# # B started
# # B finished
# # A finished
# #
# # Explanation:
# # - Both tasks start before either finishes.
# # - The shorter sleep usually completes first.
# # - Exact scheduling details can depend on the environment.


# # ============================================================
# # 11. Concurrency: Threads vs Processes vs Async I/O
# # ============================================================

# from concurrent.futures import ThreadPoolExecutor


# def thread_work(n):
#     time.sleep(0.01)
#     return n * 2


# with ThreadPoolExecutor(max_workers=3) as pool:
#     results = list(pool.map(thread_work, [1, 2, 3]))

# print(results)

# # Output:
# # [2, 4, 6]
# #
# # Explanation:
# # - Threads can overlap blocking I/O and waiting.
# # - Processes are often useful for CPU-bound parallel work.
# # - Async I/O is useful for many concurrent operations that support await.
# # - This example demonstrates threads; it does not benchmark all three models.


# # ============================================================
# # 12. GIL and Free-Threaded Python
# # ============================================================

# import sys
# import sysconfig


# print("Free-threaded build flag:", sysconfig.get_config_var("Py_GIL_DISABLED"))
# print("GIL enabled at runtime:", getattr(sys, "_is_gil_enabled", lambda: "Not available")())

# # Output:
# # Environment-dependent.
# #
# # Explanation:
# # - Py_GIL_DISABLED indicates whether this build supports a free-threaded mode.
# # - _is_gil_enabled() is available in relevant CPython versions/builds.
# # - A free-threaded-capable build may still run with the GIL enabled.


# # ============================================================
# # 13. Memory Management, Reference Counting, and Garbage Collection
# # ============================================================

# import gc


# class Node:
#     pass


# node_a = Node()
# node_b = Node()
# node_a.other = node_b
# node_b.other = node_a

# del node_a
# del node_b

# collected = gc.collect()
# print("Garbage collection ran; collected count:", collected)

# # Output:
# # The exact collected count is environment-dependent.
# #
# # Explanation:
# # - The two Node objects refer to each other, forming a cycle.
# # - Cyclic garbage collection can reclaim unreachable cycles.
# # - The collected count can include other garbage in the process.


# # ============================================================
# # 14. Object Identity, Mutability, and Aliasing
# # ============================================================

# a = [10, 20]
# b = a
# b.append(30)

# print(a)
# print(b)
# print(a is b)

# # Output:
# # [10, 20, 30]
# # [10, 20, 30]
# # True
# #
# # Explanation:
# # - a and b reference the same mutable list.
# # - Mutating the list through b is visible through a.


# a = [10, 20]
# b = a.copy()
# b.append(30)

# print(a)
# print(b)
# print(a is b)

# # Output:
# # [10, 20]
# # [10, 20, 30]
# # False
# #
# # Explanation:
# # - list.copy() creates a new outer list.
# # - This is a shallow copy, so nested objects would still be shared.


# # ============================================================
# # 15. Shallow Copy vs Deep Copy
# # ============================================================

# import copy


# original = {"name": "Car", "details": {"speed": 100}}
# shallow = copy.copy(original)
# deep = copy.deepcopy(original)

# shallow["details"]["speed"] = 200

# print(original["details"]["speed"])
# print(deep["details"]["speed"])

# # Output:
# # 200
# # 100
# #
# # Explanation:
# # - The shallow copy shares the nested details dictionary.
# # - The deep copy recursively copies nested objects where possible.


# # ============================================================
# # 16. Iterators, Iterables, and Custom Iterator Protocols
# # ============================================================

# class Countdown:
#     def __init__(self, start):
#         self.current = start

#     def __iter__(self):
#         return self

#     def __next__(self):
#         if self.current <= 0:
#             raise StopIteration
#         value = self.current
#         self.current -= 1
#         return value


# for number in Countdown(3):
#     print(number)

# # Output:
# # 3
# # 2
# # 1
# #
# # Explanation:
# # - __iter__ returns the iterator.
# # - __next__ returns the next value and raises StopIteration when exhausted.


# # ============================================================
# # 17. Context Managers and contextlib
# # ============================================================

# class Resource:
#     def __enter__(self):
#         print("Resource acquired")
#         return self

#     def __exit__(self, exc_type, exc_value, traceback):
#         print("Resource released")
#         return False


# with Resource():
#     print("Working")

# # Output:
# # Resource acquired
# # Working
# # Resource released
# #
# # Explanation:
# # - __enter__ runs on entry to the with block.
# # - __exit__ runs on leaving the block, including exceptional exits.
# # - Returning False means an exception is not suppressed.


# # ============================================================
# # 18. Exception Chaining and Exception Groups
# # ============================================================

# try:
#     try:
#         int("abc")
#     except ValueError as exc:
#         raise RuntimeError("Invalid configuration") from exc
# except RuntimeError as exc:
#     print(exc)
#     print(type(exc.__cause__).__name__)

# # Output:
# # Invalid configuration
# # ValueError
# #
# # Explanation:
# # - "raise ... from exc" explicitly records the original exception as the cause.


# try:
#     raise ExceptionGroup(
#         "Multiple failures",
#         [ValueError("Bad value"), TypeError("Wrong type")],
#     )
# except* ValueError as group:
#     print("Value errors:", len(group.exceptions))
# except* TypeError as group:
#     print("Type errors:", len(group.exceptions))

# # Output:
# # Value errors: 1
# # Type errors: 1
# #
# # Explanation:
# # - ExceptionGroup contains multiple exceptions.
# # - except* handles matching subsets of an exception group.
# # - ExceptionGroup and except* require Python 3.11+.


# # ============================================================
# # 19. Dynamic Attribute Access
# # ============================================================

# class Config:
#     def __getattr__(self, name):
#         return f"{name} is not configured"


# config = Config()
# print(config.database)
# print(config.timeout)

# # Output:
# # database is not configured
# # timeout is not configured
# #
# # Explanation:
# # - __getattr__ is called when ordinary attribute lookup fails.
# # - __getattribute__ intercepts almost all ordinary instance attribute lookups.
# # - __setattr__ can intercept assignments.


# # ============================================================
# # 20. __slots__ and Attribute Storage
# # ============================================================

# class Point:
#     __slots__ = ("x", "y")

#     def __init__(self, x, y):
#         self.x = x
#         self.y = y


# point = Point(10, 20)
# print(point.x, point.y)

# try:
#     point.z = 30
# except AttributeError as exc:
#     print(type(exc).__name__)

# # Output:
# # 10 20
# # AttributeError
# #
# # Explanation:
# # - __slots__ declares the permitted instance attributes.
# # - Without an instance dictionary or a slot for z, assigning point.z fails.


# # ============================================================
# # 21. Abstract Base Classes and Virtual Subclasses
# # ============================================================

# from abc import ABC, abstractmethod


# class AbstractVehicle(ABC):
#     @abstractmethod
#     def start(self):
#         pass


# class ConcreteCar(AbstractVehicle):
#     def start(self):
#         return "Engine started"


# car = ConcreteCar()
# print(car.start())

# try:
#     AbstractVehicle()
# except TypeError as exc:
#     print(type(exc).__name__)

# # Output:
# # Engine started
# # TypeError
# #
# # Explanation:
# # - Abstract classes with unimplemented abstract methods cannot be instantiated.
# # - Concrete subclasses must implement the required abstract methods.


# # Virtual subclass registration
# class Flyable(ABC):
#     pass


# class Drone:
#     pass


# Flyable.register(Drone)
# print(issubclass(Drone, Flyable))

# # Output:
# # True
# #
# # Explanation:
# # - Virtual subclass registration affects isinstance/issubclass checks.
# # - It does not add Flyable to Drone's MRO or add methods to Drone.


# # ============================================================
# # 22. Structural Subtyping and Protocols
# # ============================================================

# from typing import Protocol


# class HasStart(Protocol):
#     def start(self) -> str:
#         ...


# class ProtocolCar:
#     def start(self) -> str:
#         return "Started"


# def activate(vehicle: HasStart) -> None:
#     print(vehicle.start())


# activate(ProtocolCar())

# # Output:
# # Started
# #
# # Explanation:
# # - ProtocolCar does not explicitly inherit from HasStart.
# # - Static type checkers can accept it because it has the required method.
# # - Protocol compatibility is primarily a static typing feature.


# # ============================================================
# # 23. Generics, Variance, and Type Bounds
# # ============================================================

# # Python 3.12+ syntax for a generic function.
# def first[T](items: list[T]) -> T:
#     return items[0]


# print(first([10, 20, 30]))
# print(first(["car", "bus"]))

# # Output:
# # 10
# # car
# #
# # Explanation:
# # - T is a type parameter.
# # - A type checker can infer T as int for the first call and str for the second.
# # - Python does not enforce these annotations at runtime by default.


# from typing import Protocol, TypeVar

# T_co = TypeVar("T_co", covariant=True)


# class Producer(Protocol[T_co]):
#     def get(self) -> T_co:
#         ...


# # Output:
# # No runtime output.
# #
# # Explanation:
# # - Covariance allows a producer of a more specific type to be used where a
# #   producer of a more general type is expected.
# # - Variance primarily affects static type checking.


# # ============================================================
# # 24. TypeVar, ParamSpec, and TypeVarTuple
# # ============================================================

# from collections.abc import Callable
# from typing import ParamSpec, TypeVar, TypeVarTuple

# P = ParamSpec("P")
# R = TypeVar("R")
# Ts = TypeVarTuple("Ts")


# def log_call(func: Callable[P, R]) -> Callable[P, R]:
#     @wraps(func)
#     def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
#         print("Calling function")
#         return func(*args, **kwargs)
#     return wrapper


# @log_call
# def add(a: int, b: int) -> int:
#     return a + b


# print(add(2, 3))

# # Output:
# # Calling function
# # 5
# #
# # Explanation:
# # - ParamSpec models a callable's parameter list.
# # - R models its return type.
# # - TypeVarTuple can model a variable-length sequence of types in advanced
# #   generic type declarations; Ts is declared here but not otherwise used.


# # ============================================================
# # 25. Runtime Introspection and Reflection
# # ============================================================

# import inspect


# class Sensor:
#     def read(self, channel: int) -> float:
#         return 12.5


# print(inspect.signature(Sensor.read))
# print(inspect.isclass(Sensor))
# print(hasattr(Sensor, "read"))

# # Output:
# # (self, channel: int) -> float
# # True
# # True
# #
# # Explanation:
# # - inspect.signature reads a callable's signature.
# # - inspect.isclass checks whether an object is a class.
# # - hasattr checks whether an attribute can be found.


# # ============================================================
# # 26. Dynamic Class Creation with type()
# # ============================================================

# def stop(self):
#     return "Vehicle stopped"


# DynamicVehicle = type(
#     "DynamicVehicle",
#     (),
#     {"stop": stop, "category": "automotive"},
# )

# v = DynamicVehicle()
# print(v.stop())
# print(v.category)

# # Output:
# # Vehicle stopped
# # automotive
# #
# # Explanation:
# # - type(name, bases, namespace) creates a class dynamically.
# # - The bases tuple is empty here, so the class inherits from object by default.


# # ============================================================
# # 27. Import System Internals and Custom Import Hooks
# # ============================================================

# import math
# import sys


# print(math.__name__)
# print(math.__spec__.origin)
# print("math" in sys.modules)

# # Typical output on CPython:
# # math
# # built-in
# # True
# #
# # Explanation:
# # - sys.modules caches imported modules.
# # - The module origin can vary by Python build and implementation.
# # - Custom import hooks can customize module discovery/loading; this example
# #   demonstrates module metadata and caching, not a custom hook.


# # ============================================================
# # 28. Python Bytecode and Disassembly
# # ============================================================

# import dis


# def add_numbers(a, b):
#     return a + b


# dis.dis(add_numbers)

# # Output:
# # A sequence of bytecode instructions, typically including operations
# # equivalent to loading a and b, adding them, and returning the result.
# # Exact instructions and offsets depend on Python version.
# #
# # Explanation:
# # - dis disassembles CPython bytecode into readable instructions.
# # - Bytecode is an implementation detail, not Python source or machine code.


# # ============================================================
# # 29. Abstract Syntax Trees (AST) and Code Objects
# # ============================================================

# import ast


# source = "result = price * quantity"
# tree = ast.parse(source)
# print(ast.dump(tree, indent=2))

# # Output:
# # An AST representation of an assignment whose value is price * quantity.
# # Exact formatting may vary by Python version.
# #
# # Explanation:
# # - The AST represents the grammatical structure of source code.


# source = "print(10 + 20)"
# code = compile(source, "<example>", "exec")
# print(type(code).__name__)

# # Output:
# # code
# #
# # Explanation:
# # - compile() converts source text or an AST into a code object.


# # ============================================================
# # 30. eval(), exec(), and Dynamic Code Execution
# # ============================================================

# result = eval("10 + 20")
# print(result)

# namespace = {}
# exec("x = 5\ny = 7\nresult = x * y", namespace)
# print(namespace["result"])

# # Output:
# # 30
# # 35
# #
# # Explanation:
# # - eval evaluates an expression and returns its value.
# # - exec executes statements in a namespace.
# # - Never execute untrusted input with eval or exec.


# # ============================================================
# # 31. Pickling and Serialization
# # ============================================================

# import pickle


# data = {"vehicle": "Car", "speed": 120}
# serialized = pickle.dumps(data)
# restored = pickle.loads(serialized)

# print(restored)

# # Output:
# # {'vehicle': 'Car', 'speed': 120}
# #
# # Explanation:
# # - pickle serializes Python objects and can reconstruct them.
# # - Never unpickle data from untrusted sources because loading it can execute
# #   arbitrary code.


# # ============================================================
# # 32. Weak References and Weak Dictionaries
# # ============================================================

# import weakref


# class WeakSensor:
#     pass


# sensor = WeakSensor()
# ref = weakref.ref(sensor)

# print(ref() is sensor)

# del sensor
# gc.collect()

# print(ref())

# # Output:
# # True
# # None
# #
# # Explanation:
# # - A weak reference does not keep the object alive by itself.
# # - Once the object is collected, calling the weak reference returns None.


# # ============================================================
# # 33. Function Objects, Frames, and Execution Contexts
# # ============================================================

# def calculate(x):
#     y = x * 2
#     return y


# print(calculate.__name__)
# print(calculate.__code__.co_varnames)
# print(calculate.__code__.co_argcount)

# # Output:
# # calculate
# # ('x', 'y')
# # 1
# #
# # Explanation:
# # - Function objects expose metadata about their code.
# # - A frame represents an active function execution; frames can be inspected
# #   with inspect.currentframe() while a function is running.


# # ============================================================
# # 34. Namespace Resolution: LEGB
# # ============================================================

# x = "global"


# def outer():
#     x = "enclosing"

#     def inner():
#         x = "local"
#         print(x)

#     inner()


# outer()

# # Output:
# # local
# #
# # Explanation:
# # - LEGB means Local, Enclosing, Global, Built-in.
# # - Python searches these scopes in that order for ordinary name lookup.


# def make_incrementer():
#     count = 0

#     def increment():
#         nonlocal count
#         count += 1
#         return count

#     return increment


# incrementer = make_incrementer()
# print(incrementer())
# print(incrementer())

# # Output:
# # 1
# # 2
# #
# # Explanation:
# # - nonlocal rebinds a variable in an enclosing function scope.


# # ============================================================
# # 35. Monkey Patching and Runtime Modification
# # ============================================================

# class PatchableSensor:
#     def read(self):
#         return "Original reading"


# def mock_read(self):
#     return "Mock reading"


# sensor = PatchableSensor()
# PatchableSensor.read = mock_read

# print(sensor.read())

# # Output:
# # Mock reading
# #
# # Explanation:
# # - The class method is replaced at runtime.
# # - Existing instances normally observe the new method through class lookup.


# # ============================================================
# # 36. Re-entrant Functions and Recursive State Management
# # ============================================================

# def factorial(n):
#     if n <= 1:
#         return 1
#     return n * factorial(n - 1)


# print(factorial(5))

# # Output:
# # 120
# #
# # Explanation:
# # - Each recursive invocation has its own local variables and execution frame.
# # - Recursion depth is limited; very deep recursion can raise RecursionError.


# # ============================================================
# # 37. Operator Overloading and Reflected Operations
# # ============================================================

# class Number:
#     def __init__(self, value):
#         self.value = value

#     def __add__(self, other):
#         if isinstance(other, Number):
#             return Number(self.value + other.value)
#         return NotImplemented

#     def __radd__(self, other):
#         return Number(other + self.value)


# n = Number(10)
# print((n + Number(5)).value)
# print((5 + n).value)

# # Output:
# # 15
# # 15
# #
# # Explanation:
# # - __add__ handles normal addition when the custom object is on the left.
# # - __radd__ can handle reflected addition when the custom object is on the right.
# # - NotImplemented tells Python to try other applicable operation methods.


# # ============================================================
# # 38. Hashing, Equality, and Dictionary/Set Internals
# # ============================================================

# class Key:
#     def __init__(self, value):
#         self.value = value

#     def __eq__(self, other):
#         if not isinstance(other, Key):
#             return NotImplemented
#         return self.value == other.value

#     def __hash__(self):
#         return hash(self.value)


# key_a = Key(10)
# key_b = Key(10)
# items = {key_a: "first"}

# print(key_a == key_b)
# print(items[key_b])

# # Output:
# # True
# # first
# #
# # Explanation:
# # - Equal keys must have equal hashes.
# # - The dictionary can find the value using key_b because key_a and key_b compare
# #   equal and have matching hashes.
# # - Key hash/equality behavior must remain stable while used as a dictionary key.


# # ============================================================
# # 39. Class Decorators and Metaprogramming
# # ============================================================

# registry = {}


# def register(cls):
#     registry[cls.__name__] = cls
#     return cls


# @register
# class RegisteredCar:
#     pass


# @register
# class RegisteredBus:
#     pass


# print(sorted(registry))

# # Output:
# # ['RegisteredBus', 'RegisteredCar']
# #
# # Explanation:
# # - A class decorator receives a class after class creation.
# # - This decorator registers the class by name.
# # - Class decorators are often simpler than metaclasses for registration tasks.


# # ============================================================
# # 40. Performance Profiling, Memory Profiling, and Complexity
# # ============================================================

# from time import perf_counter
# import cProfile


# start_time = perf_counter()
# total = sum(range(1_000_000))
# elapsed = perf_counter() - start_time

# print(total)
# print(f"Elapsed: {elapsed:.4f} seconds")

# # Output:
# # 499999500000
# # Elapsed: <measured time> seconds
# #
# # Explanation:
# # - perf_counter measures elapsed wall-clock time.
# # - The measured time depends on hardware, Python version, and system load.


# def find_linear(items, target):
#     for item in items:
#         if item == target:
#             return True
#     return False


# def find_set(items, target):
#     return target in set(items)


# sample = list(range(100))
# print(find_linear(sample, 99))
# print(find_set(sample, 99))

# # Output:
# # True
# # True
# #
# # Explanation:
# # - Linear search is O(n) in the worst case.
# # - Building a set costs O(n) expected time; membership afterward is O(1)
# #   expected time. Rebuilding the set for each lookup adds conversion cost.


# def profiling_work():
#     return sum(i * i for i in range(100_000))


# cProfile.run("profiling_work()")

# # Output:
# # A profile report with function-call counts and timing statistics.
# # Exact measurements vary by machine and Python version.
# #
# # Explanation:
# # - cProfile identifies where time is spent.
# # - Profile before optimizing rather than guessing which code is slow.
# '''

# path = Path("/mnt/data/advanced_python_concepts_all_examples.py")
# path.write_text(content, encoding="utf-8")
# print(f"Created: {path}")
# print(f"File size: {path.stat().st_size:,} bytes")
