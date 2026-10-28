# Python 3.14 opportunities over 3.13

Use this during feature design, dependency review and bounded modernization.
The starter targets only 3.14. Select features for a concrete benefit; metadata
does not teach an agent their semantics. Record the consumer, benefit, risks and
validation before adopting a changed API. Do not invent work to use new syntax.

| Candidate | Useful when | Required interpretation |
| --- | --- | --- |
| Deferred annotations / annotationlib | Forward references or runtime type introspection | Choose VALUE, FORWARDREF or STRING deliberately; verify schema/Pydantic consumers; future imports retain different stringified semantics |
| Executor.map buffersize | Large task streams need bounded submission | Bound memory/work in flight and test failure/shutdown behavior |
| InterpreterPoolExecutor | Independent CPU tasks justify parallelism | Benchmark against existing execution; check serialization and extension compatibility |
| compression.zstd | A real compression need can use stdlib | Check availability and interoperable formats; preserve stored-data contracts |
| Path.copy / move | File adapters become clearer | Preserve overwrite, symlink, metadata and recovery behavior; no broad replacement |
| Template strings | A processor needs separate literal/interpolated parts | Template is not str; escaping requires the processor; retain parameterized SQL and safe subprocess argument handling |

Ordinary CPython 3.14 does not automatically enable free-threading or the
experimental JIT. Evaluate alternative builds separately; benchmark performance
claims. Check porting changes too, particularly annotation evaluation and the
POSIX process-start default (forkserver on supported non-macOS POSIX systems;
Windows/macOS retain spawn). Syntax parsing alone does not prove that complexity
analyzers score a new construct correctly. Existing compatibility fixtures are
focused evidence, not complete feature coverage.

Keep this Python binding in starter, not SP, gz-skills or expected/deferred SP-BP.
The small starter helper does not need concurrency, compression or template
machinery simply because a larger adopting application might benefit.

Official versioned sources: [release/porting notes](https://docs.python.org/3.14/whatsnew/3.14.html),
[annotationlib](https://docs.python.org/3.14/library/annotationlib.html),
[executors](https://docs.python.org/3.14/library/concurrent.futures.html),
[Zstandard](https://docs.python.org/3.14/library/compression.zstd.html),
[pathlib](https://docs.python.org/3.14/library/pathlib.html), and
[template strings](https://docs.python.org/3.14/library/string.templatelib.html).
