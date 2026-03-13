# Working Memory

## set_working_memory

**When to use:** Track state across tool calls—active task, current step, important values.

**How:**
- `key`: Name (e.g. "current_task", "active_dag").
- `value`: Value to store (string).

**Examples:**
- Track task: `set_working_memory("current_task", "installing deps")`
- DAG state: `set_working_memory("active_dag", "yes")`

**Tips:** Working memory is included in your context on every turn. Use it so you remember what you're in the middle of. The DAG tools set it automatically when a DAG is active.
