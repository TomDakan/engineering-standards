---
title: Python Concurrency
type: language-guide
language: python
topic: concurrency
version: 1.0.0
---

#### I/O Bound (Network/Disk)

* **Modern**: Use `asyncio` for scalable I/O.
* **Event Loop Blocking**: Strict prohibition of blocking I/O (synchronous `requests`, `time.sleep`) within `async` functions.
* **Task Groups**: Use `asyncio.TaskGroup` (Python 3.11+) or safe wrappers to manage background tasks; never use "fire-and-forget" `create_task` without references.
* **Traceability**: All async functions processing business events must accept and propogate `correlation_id` (via context variables or explicit arguments) to ensure logs are traceable across async boundaries.

#### CPU Bound (Math/Data)

* **Standard**: Use `ProcessPoolExecutor` to utilize multiple cores and bypass the GIL.
* **Constraints**: Arguments must be serializable (pickleable). No lambdas, no open sockets.
* **Overhead**: Avoid offloading tiny tasks (microseconds) to a process pool due to start-up overhead.
* **Safety**: Code using multiprocessing must be guarded by `if __name__ == "__main__":`.

## Verification Checklist

* **Traceability**
  * Do async worker functions accept `correlation_id`?
  * Is context propagated to all background tasks?
* **Safety**
  * Is `asyncio.TaskGroup` (or equivalent) used instead of naked `create_task`?
  * Are blocking calls avoided in the event loop?
