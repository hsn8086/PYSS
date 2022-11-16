# PYSS

is a py server script runner, from my strange idea, not much maintenance.

## How to use it:

Create the script you want to allow under `/scripts` and create the function `main` in it.

```python
def main():
    return 'ok'
```

To set the MIME type to be returned enter

```python
return_type = 'text/plain'
```