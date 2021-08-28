# Updating reNgine

Updating is as simple as running the following command:

```bash
make down && git pull && make build && make up
```

## Detailed Update Instructions

1. Bring all reNgine services down
```bash
make down
```
2. Get the latest changes
```bash
git pull
```
3. Rebuild the latest changes
```bash
make build
```
4. Start reNgine services
```bash
make up
```
