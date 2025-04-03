# Tamarin
A small testing framework written in Python.

## Features
Tamarin uses a Test decorator to construct test cases. These decorators allow you to abstract out
boilerplate for generating random inputs or error reporting, keeping tests neat and declarative.

```python
number_range = Random.int(-100, 100)    
   
@Test.given(a = number_range, b = number_range).should("Return the sum")    
def test_my_add(a, b):    
  Assert(my_add(a, b)).equals(a + b)    
    
   
if __name__ == "__main__":    
  run_all()
```

