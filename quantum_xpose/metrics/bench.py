
import time
from typing import Callable, Dict, Any

def time_call(fn: Callable, *args, **kwargs) -> Dict[str, Any]:
    t0 = time.time()
    out = fn(*args, **kwargs)
    elapsed = time.time() - t0
    return {"result": out, "runtime_sec": elapsed}
