## Installation

```sh
pip install git+https://github.com/cardisnotvalid/lolzteam-api.git
```

## Usage

```python
import os
from lolzteam import Lolzteam

lolzteam = Lolzteam(api_key=os.environ.get("LOLZTEAM_API_KEY"))
user = lolzteam.get_user("me")
lolzteam.close()
```

You can also use the context manager.

```python
with Lolzteam(api_key=api_key) as lolzteam:
    user = lolzteam.get_user("me")
```
