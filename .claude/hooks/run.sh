#!/usr/bin/env bash
# Runs vault_hooks.py with the first working Python 3.8+ (python3 on Linux/macOS,
# python on Windows, where "python3" may be the Microsoft Store stub).
for py in python3 python py; do
  if "$py" -c "import sys; sys.exit(sys.version_info < (3, 8))" >/dev/null 2>&1; then
    exec "$py" "$(dirname "$0")/vault_hooks.py" "$@"
  fi
done
echo "vault hooks: Python 3.8+ not found; hooks skipped" >&2
exit 0
