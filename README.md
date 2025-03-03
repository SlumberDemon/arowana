# Arowana

Arowana provides a simple local base and drive. Base is a NoSQL wrapper for sqlite3 and drive is a wrapper for the filesystem.
Arowana is a sister project of [fishweb](https://github.com/slumberdemon/fishweb).

## Installation

```sh
pip install arowana
```

## Base

Base is a simple NoSQL wrapper for sqlite3. To get started define the location and name of the base.

```py
from arowana import Arowana

arowana = Arowana("data")  # Creates 'data' folder
base = arowana.Base("testing") # Creates base/table 'testing'
```

### `put`

Put item into base. Overrides existing item if key already exists

Args:
  - data: The data to be stored
  - key: The key to store the data under. If None, a new key will be generated

Returns:
  - Item: Added item details

```py
# Key is automatically generated
base.put({"name": "sofa", "price": 20})

# Set key as "one"
base.put({"name": "sofa", "price": 20}, "one")

# The key can also be included in the object
base.put({"name": "sofa", "price": 20, "key": "test"})

# Supports multipe types
base.put("hello, worlds")
base.put(7)
base.put(True)

# "success" is the value and "smart_work" is the key.
base.put(data="sofa", key="name")
```

### `puts`

Put multiple items into base

Args:
  - items: Items to add

Returns:
  - Items: Added item details

```py
base.puts(
    [
        {"name": "sofa", "hometown": "Sofa islands", "key": "slumberdemon"},  # Key provided.
        ["nemo", "arowana", "fishweb", "clownfish"],  # Key auto-generated.
        "goldfish",  # Key auto-generated.
    ],
)
```


### `insert`

Insert item to base. Does not override existing item if key already exists

Args:
  - data: The data to be stored
  - key: The key to store the data under. If None, a new key will be generated

Returns:
  - Item: Added item details

```py
# Will succeed and auto generate a key
base.insert("hello, world")

# Will succeed with key "greeting1"
base.insert({"message": "hello, world"}, "greeting1")

# Will raise an error as key "greeting1" already exists
base.insert({"message": "hello, there"}, "greeting1")
```

### `get`

Get item from base.

Args:
  - key: key of the item to retrieve

Returns:
  - Item: Retrieved item details

```py
base.get("sofa")
```

### `delete`

Delete item from base.

Args:
  - key: key of the item to delete

```py
base.delete("sofa")
```

### `update`

Update item in base

Args:
  - data: Attributes to update
  - key: Key of the item to update

```py
base.update(
    {
        "name": "sofa",  # Set name to "sofa"
        "status.active": True,  # Set "status.active" to True
        "description": base.util.trim(),  # Remove description element
        "likes": base.util.append("fishing"),  # Append fishing to likes array
        "age": base.util.increment(1),  # Increment age by 1
    },
    "slumberdemon",
)
```

### `all`

Get all items in base

```py
base.all()
```

### `drop`

Delete base from database

```py
base.drop()
```

### `utils`

- `util.trim()` - Remove element from dict
- `util.increment(value)` - Increment element by value
- `util.append(value)` - Append element to list

## Drive

Drive makes it super easy to store and manage files.

```py
from arowana import Arowana

arowana = Arowana("data")  # Creates 'data' folder
drive = arowana.Drive("testing") # Creates folder/drive 'testing'
```

### `put`

Put file

Args:
  - name: Name and path of the file
  - data: Data content of file
  - path: Path of file to get content from

Returns:
  - str: Name of the file

```py
# Put content directly
drive.put("hello.txt", "Hello world")
drive.put(b"hello.txt", "Hello world")

import io

# Provide file content object
drive.put("arowana.txt", io.StringIO("hello world"))
drive.put("arowana.txt", io.BytesIO(b"hello world"))

with open("./arowana.txt", "r") as file:
    drive.put("arowana.txt", file)

# Provide a path to a file.
drive.put("arowana.txt", path="./arowana.txt")
```

### `get`

Get file content

Args:
  - name: Name and path of the file

Returns:
  - bytes: File bytes

```py
drive.get("arowana.txt")
```

### `list`

List all files

Args:
  - prefix: Prefix that file names start with

Returns:
  - list: List of file names

```py
drive.list()
```

### `delete`

Delete file

Args:
  - name: Name and path of the file

Returns:
  - str: Name of the deleted file

```py
drive.delete("arowana.txt")
```

## Fishweb

To learn more about using arowana with fishweb read the [documentation](https://fishweb.sofa.sh/content/concepts/arowana).

## Inspirations

- [deta-python](https://github.com/deta/deta-python)
- [KenobiDB](https://github.com/patx/kenobi)
- [OakDB](https://github.com/abdelhai/oakdb)
