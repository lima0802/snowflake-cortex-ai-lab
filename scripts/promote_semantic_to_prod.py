"""
Promote Semantic Model DEV -> PROD
===================================

Reads config/semantic_models/semantic.yaml, replaces all DEV references
with PROD equivalents, and writes the result to
config/semantic_models/prod/semantic_prod.yaml.

Replacements applied:
  SFMC_EMAIL_PERFORMANCE_DEV  ->  SFMC_EMAIL_PERFORMANCE_PROD
  DEV_MARCOM_DB               ->  PROD_MARCOM_DB

Usage:
    python scripts/promote_semantic_to_prod.py [--input ...] [--output ...]

Author: Li Ma
Date: February 24, 2026
"""

import sys
import argparse
from pathlib import Path

# Force UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

REPLACEMENTS = [
    ('SFMC_EMAIL_PERFORMANCE_DEV', 'SFMC_EMAIL_PERFORMANCE_PROD'),
    ('DEV_MARCOM_DB',              'PROD_MARCOM_DB'),
]


def promote(input_path: Path, output_path: Path):
    print("\n" + "="*70)
    print("🚀 SEMANTIC MODEL PROMOTER  DEV -> PROD")
    print("="*70 + "\n")

    print(f"📖 Reading:  {input_path}")
    content = input_path.read_text(encoding='utf-8')

    total = 0
    for dev_str, prod_str in REPLACEMENTS:
        count = content.count(dev_str)
        if count:
            content = content.replace(dev_str, prod_str)
            print(f"   ✅ {dev_str:35s} -> {prod_str}  ({count} occurrence{'s' if count > 1 else ''})")
            total += count
        else:
            print(f"   ⏭️  {dev_str:35s}  (not found, skipped)")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding='utf-8')

    print(f"\n💾 Written:  {output_path}")
    print(f"\n📊 Total replacements: {total}")
    print("\n" + "="*70)
    print("✅ PROMOTION COMPLETE!")
    print("="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Promote semantic model from DEV to PROD',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--input', '-i',
        default='config/semantic_models/semantic.yaml',
        help='Source DEV semantic model (default: config/semantic_models/semantic.yaml)'
    )
    parser.add_argument(
        '--output', '-o',
        default='config/semantic_models/prod/semantic_prod.yaml',
        help='Target PROD file (default: config/semantic_models/prod/semantic_prod.yaml)'
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"\n❌ Input file not found: {input_path}")
        sys.exit(1)

    try:
        promote(input_path, output_path)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
