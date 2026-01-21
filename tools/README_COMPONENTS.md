# Component Catalog (Decompile)

This folder contains a generated list of FrooxEngine component types derived
from the decompiled `FrooxEngine` sources.

## Files

- `frooxengine_components.json` - JSON catalog of component type names.
- `extract_components.py` - Script used to generate the catalog.

## Regenerating

```bash
/usr/bin/python tools/extract_components.py \
  --root /mnt/12tb/git/FrooxEngineDecompile/FrooxEngine \
  --out tools/frooxengine_components.json
```

## Notes

- The catalog includes only classes that inherit from `Component`.
- Not all components are safe or useful to add via ResoniteLink.
- For experimental components (e.g., ProtoFlux), use the full type name:
  `[FrooxEngine]FrooxEngine.ProtoFlux.<ComponentName>`
