## Usage

```py
import os
from lolzteam import Lolzteam

lt = Lolzteam(api_key=os.environ.get("LOLZTEAM_API_KEY"))
threads = lt.get_thread(forum_id=876)
```
