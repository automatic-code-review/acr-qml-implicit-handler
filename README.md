# acr-qml-implicit-handler

This ACR (Automatic Code Review) extension detects the use of **implicit signal handlers** in QML, such as:

```qml
onClicked: {
    doSomething(value)
}
```

Although this pattern is valid in QML, it relies on the parameter names defined in the original `signal`. If the parameter name changes, the handler may break silently at runtime.

---

## ✅ Recommended Style

Always use **explicit anonymous functions** in signal handlers:

```qml
onClicked: function(value) {
    doSomething(value)
}
```

Even when no parameters are used, prefer:

```qml
onSomething: function() {
    // ...
}
```

This makes the code more resilient, clear, and less dependent on signal internals.

---

## Configuration (`config.json`)

```json
{
  "stage": "static",
  "language": "PYTHON",
  "data": {
    "message": "Evite o uso de signal handlers implícitos no QML (`onX: { ... }`), em vez disso use funções anônimas explícitas (`onX: function(...) { ... }`).<br><br><hr><br>${OCCURRENCES}"
  }
}
```

---

## Tags

- QML
- Signal
- Handler
- Code Style
- Best Practices

---

## License

Read LICENSE.md
