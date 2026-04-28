#!/usr/bin/env python3
import re, sys
from pathlib import Path
KV = re.compile(r'^(\w+?)\s*=\s*(.*)$')
YES = re.compile(r'":\s*"yes"')
NO  = re.compile(r'":\s*"no"')
NUM = re.compile(r'":\s*"(\d+)"')

def to_json(text: str) -> str:
    fields = [f'    "{m.group(1)}": "{m.group(2)}",' for m in map(KV.match, text.splitlines()) if m]
    if not fields:
        return "{\n}\n"
    content = "\n".join(fields)
    content = YES.sub('": true', NO.sub('": false', NUM.sub(r'": \1', content)))
    lines = content.splitlines()
    lines[-1] = lines[-1].rstrip().rstrip(',')  # remove trailing comma on last field
    return "{\n" + "\n".join(lines) + "\n}\n"

def main():
    cwd = Path.cwd()
    if not any(part.lower() == "game" for part in cwd.parts):
        print(
                "Error: The current working directory is not inside a directory named 'game'.\n"
                f"Current directory: {cwd}\n"
                "Please cd into the 'game' directory (or one of its subdirectories) and run this script again."
                ,file=sys.stderr,)
        sys.exit(1)
    dlc_files = [p for p in cwd.rglob("*.dlc") if p.is_file() and p.parent != cwd]
    if not dlc_files:
        print("No .dlc files found in subdirectories of the working directory.")
        return

    ok = 0
    for p in dlc_files:
        try:
            out = to_json(p.read_text(encoding="utf-8"))
            target = p.with_name(p.name + ".json")  # e.g., file.dlc.json
            target.write_text(out, encoding="utf-8", newline="\n")
            p.unlink()
            print(f"Converted and renamed: {p} -> {target}")
            ok += 1
        except Exception as e:
            print(f"Error processing '{p}': {e}", file=sys.stderr)
    print(f"Done. {ok}/{len(dlc_files)} files processed successfully.")

if __name__ == "__main__":
    main()# Pause so the user can see the result; skip if not an interactive terminal
    try:
        if sys.stdin and sys.stdin.isatty():
            input("Press Enter to exit...")
    except EOFError:
        pass
