1. python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculation.proto

```json
{
    "calculation_type": "LATEX",
    "expression": "Piecewise((x**2, x < 0), (sin(x)**2 + cos(x)**2, True))",
    "parameters": [
        {
            "name": "x",
            "value": -2
        }
    ]
}
```