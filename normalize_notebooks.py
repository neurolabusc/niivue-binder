#!/usr/bin/env python3
"""
normalize_notebooks.py

Normalize Jupyter notebooks to reduce noisy diffs:
 - clear execution counts
 - clear outputs
 - remove widget model_id fields if present
 - (optionally) clear notebook metadata

Usage:
  # dry-run, only report which files would be changed
  python normalize_notebooks.py --dry-run

  # normalize all notebooks under current directory and overwrite them
  python normalize_notebooks.py

  # operate on specific path(s)
  python normalize_notebooks.py path/to/notebook.ipynb another.ipynb

"""
import argparse
import json
import shutil
from pathlib import Path
from typing import Any, Dict

def remove_widget_model_ids(obj: Any) -> Any:
    """
    Recursively remove 'model_id' keys inside
    application/vnd.jupyter.widget-view+json data structures.
    We walk the dicts/lists and drop 'model_id' keys wherever found.
    """
    if isinstance(obj, dict):
        # If this dict is the widget-view data, remove model_id keys
        # but do not delete other keys. Also handle both 'model_id' and 'modelId' variants.
        if "application/vnd.jupyter.widget-view+json" in obj:
            widget = obj["application/vnd.jupyter.widget-view+json"]
            if isinstance(widget, dict):
                widget.pop("model_id", None)
                widget.pop("modelId", None)
            # continue deeper in case there are nested dicts
            obj["application/vnd.jupyter.widget-view+json"] = remove_widget_model_ids(widget)

        # For any other keys, recursively clean
        for k, v in list(obj.items()):
            obj[k] = remove_widget_model_ids(v)
        # additionally delete any top-level model_id keys if they appear
        obj.pop("model_id", None)
        obj.pop("modelId", None)
        return obj
    elif isinstance(obj, list):
        return [remove_widget_model_ids(v) for v in obj]
    else:
        return obj

def normalize_notebook(nb: Dict[str, Any], clear_metadata: bool = False) -> Dict[str, Any]:
    changed = False

    # Clear top-level execution_count if present (some notebooks may have stray fields)
    if "execution_count" in nb and nb["execution_count"] is not None:
        nb["execution_count"] = None
        changed = True

    # Normalize cells
    cells = nb.get("cells", [])
    for cell in cells:
        # Execution count
        if cell.get("execution_count", None) is not None:
            cell["execution_count"] = None
            changed = True

        # Outputs: replace with empty list if non-empty
        if cell.get("outputs"):
            cell["outputs"] = []
            changed = True

        # Remove widget model_ids inside outputs if you choose to keep outputs in future
        # (for now outputs are cleared above; we still walk the structure to be safe)
        # If you wanted to preserve outputs but strip only widget ids, you'd skip clearing outputs above.
        # We'll still run the cleaner (idempotent).
        if "outputs" in cell:
            cell["outputs"] = remove_widget_model_ids(cell["outputs"])

    nb["cells"] = cells

    # Optionally clear top-level metadata (use with caution)
    if clear_metadata:
        if nb.get("metadata"):
            nb["metadata"] = {}
            changed = True
    else:
        # As a safer default, remove known volatile metadata subkeys that often change:
        md = nb.get("metadata", {})
        for key in ("widgets", "execution", "widgets_state"):
            if key in md:
                md.pop(key, None)
                changed = True
        # Keep kernelspec/language_info normally, but if they contain
        # obviously volatile keys, remove them (this is conservative).
        nb["metadata"] = md

    return nb, changed

def process_file(path: Path, dry_run: bool = False, clear_metadata: bool = False, backup: bool = True) -> bool:
    """
    Return True if the file was modified (or would be modified in dry-run).
    """
    text = path.read_text(encoding="utf-8")
    try:
        nb = json.loads(text)
    except Exception as e:
        print(f"Skipping {path}: failed to parse JSON: {e}")
        return False

    new_nb, changed = normalize_notebook(nb, clear_metadata=clear_metadata)

    if not changed:
        return False

    # Write back deterministically: sort keys to keep order stable.
    new_text = json.dumps(new_nb, ensure_ascii=False, indent=1, sort_keys=True) + "\n"

    if dry_run:
        print(f"[dry-run] would update: {path}")
        return True

    if backup:
        bak = path.with_suffix(path.suffix + ".bak")
        shutil.copy2(path, bak)

    path.write_text(new_text, encoding="utf-8")
    print(f"Updated: {path} (backup -> {bak if backup else 'none'})")
    return True

def find_notebooks(paths):
    for p in paths:
        p = Path(p)
        if p.is_dir():
            for f in p.rglob("*.ipynb"):
                yield f
        elif p.is_file() and p.suffix == ".ipynb":
            yield p
        else:
            # if user passed a glob-like path, try glob
            for f in sorted(Path(".").glob(str(p))):
                if f.suffix == ".ipynb":
                    yield f

def main():
    ap = argparse.ArgumentParser(description="Normalize Jupyter notebooks to reduce noisy diffs.")
    ap.add_argument("paths", nargs="*", default=["."], help="Files or directories to process (default: current dir).")
    ap.add_argument("--dry-run", action="store_true", help="Show which files would be changed without writing.")
    ap.add_argument(
        "--backup",
        action="store_true",
        help="Create .bak backups before overwriting (disabled by default)."
    )
    args = ap.parse_args()
    notebooks = list(find_notebooks(args.paths))
    any_changed = False
    for nb_path in find_notebooks(args.paths):
        try:
            changed = process_file(
                nb_path,
                dry_run=args.dry_run,
                clear_metadata=True,
                backup=args.backup,
            )
            any_changed = any_changed or changed
        except Exception as e:
            print(f"Error processing {nb_path}: {e}")

    if args.dry_run:
        if not any_changed:
            print(f"No notebooks would be changed ({len(notebooks)} checked).")
    else:
        if not any_changed:
            print(f"No notebooks changed ({len(notebooks)} checked).")
        else:
            print(f"Done ({len(notebooks)} checked).")

if __name__ == "__main__":
    main()
