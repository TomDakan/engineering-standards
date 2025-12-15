---
title: Delphi Design Guidelines
type: language-guide
language: delphi
topic: design
version: 1.0.0
---

## Modern Object Pascal

* **Interfaces**: Prefer interface-based design over inheritance. Use `IInterface` (or customized descendants) for all service contracts.
* **Generics**: Use `TList<T>`, `TDictionary<K,V>` from `System.Generics.Collections` instead of older `TList` or `TStringList` where improved type safety is possible.
* **Method Injection**: Prefer injecting dependencies via constructor or method arguments rather than creating them inside classes.

## Memory Management

* **Try...Finally**: Every object creation *must* have a matching `try...finally` block if it's not owned by a container.

```delphi
    LObj := TMyClass.Create;
    try
      LObj.DoSomething;
    finally
      LObj.Free;
    end;
```

* **FastMM**: Ensure FastMM is used in FullDebugMode during development to catch leaks.

## Known Pitfalls

* **With Statement**: Avoid the `with` statement. It introduces ambiguity and makes debugging harder.
* **Global Variables**: Severely restrict the use of global variables in initialization sections.
