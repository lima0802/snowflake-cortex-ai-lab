"""
Format Verified Queries - SQL to Literal Block Scalar
======================================================

Rewrites verified_queries.yaml so every `sql:` field uses YAML
literal block style (|) instead of an escaped single-line string.
This makes the SQL human-readable in any text editor.

Usage:
    python scripts/format_verified_queries.py [--file config/semantic_models/verified_queries/verified_queries.yaml]

Author: Li Ma
Date: February 24, 2026
"""

import sys
import argparse
from pathlib import Path

import yaml
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString

# Force UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def try_import_ruamel():
    try:
        from ruamel.yaml import YAML  # noqa: F401
        return True
    except ImportError:
        return False


def format_with_ruamel(input_path: Path, output_path: Path):
    """Use ruamel.yaml to preserve structure and write literal block SQL."""
    from ruamel.yaml import YAML
    from ruamel.yaml.scalarstring import LiteralScalarString

    ryaml = YAML()
    ryaml.preserve_quotes = True
    ryaml.width = 120
    ryaml.best_sequence_indent = 2
    ryaml.best_map_flow_style = False

    with open(input_path, 'r', encoding='utf-8') as f:
        data = ryaml.load(f)

    queries = data.get('verified_queries', [])
    converted = 0
    for q in queries:
        if 'sql' in q and isinstance(q['sql'], str):
            # Normalise escaped newlines, strip trailing whitespace per line
            sql = q['sql'].replace('\\n', '\n')
            lines = [line.rstrip() for line in sql.splitlines()]
            sql_clean = '\n'.join(lines).strip() + '\n'
            q['sql'] = LiteralScalarString(sql_clean)
            converted += 1

    with open(output_path, 'w', encoding='utf-8') as f:
        ryaml.dump(data, f)

    print(f"   ✅ ruamel.yaml: {converted} SQL fields converted to literal block")


def format_with_pyyaml(input_path: Path, output_path: Path):
    """Fallback: use PyYAML with a custom literal representer."""

    class LiteralStr(str):
        pass

    def literal_representer(dumper, data):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

    yaml.add_representer(LiteralStr, literal_representer)

    with open(input_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    queries = data.get('verified_queries', [])
    converted = 0
    for q in queries:
        if 'sql' in q and isinstance(q['sql'], str):
            sql = q['sql'].replace('\\n', '\n')
            lines = [line.rstrip() for line in sql.splitlines()]
            sql_clean = '\n'.join(lines).strip() + '\n'
            q['sql'] = LiteralStr(sql_clean)
            converted += 1

    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False,
                  allow_unicode=True, width=120)

    print(f"   ✅ PyYAML fallback: {converted} SQL fields converted to literal block")


def main():
    parser = argparse.ArgumentParser(
        description='Reformat verified_queries.yaml SQL fields to YAML literal block (|)',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--file', '-f',
        default='config/semantic_models/verified_queries/verified_queries.yaml',
        help='Path to verified_queries.yaml'
    )
    args = parser.parse_args()

    input_path = Path(args.file)
    if not input_path.exists():
        print(f"\n❌ File not found: {input_path}")
        sys.exit(1)

    print("\n" + "="*70)
    print("🔧 VERIFIED QUERIES SQL FORMATTER")
    print("="*70 + "\n")
    print(f"📖 Input:  {input_path}")

    # Write back to same file
    output_path = input_path

    try:
        if try_import_ruamel():
            format_with_ruamel(input_path, output_path)
        else:
            print("   ℹ️  ruamel.yaml not found, using PyYAML fallback")
            format_with_pyyaml(input_path, output_path)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print(f"💾 Output: {output_path}")
    print("\n" + "="*70)
    print("✅ FORMATTING COMPLETE!")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
