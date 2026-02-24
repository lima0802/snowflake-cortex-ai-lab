"""
Split Semantic Model into Modular Components
=============================================

This script splits a large semantic.yaml file into three separate components
inside config/semantic_models/:
  schema/            - One YAML file per table
  instructions/      - Business rules and guidelines
  verified_queries/  - Example questions and SQL

Only replaces files that already exist in each folder.

Usage:
    python scripts/split_semantic_model.py [--input config/semantic_models/semantic.yaml]

Author: Li Ma
Date: February 24, 2026
"""

import os
import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# Force UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class SemanticModelSplitter:
    """Split a monolithic semantic model into modular components"""

    def __init__(self, input_file: str):
        self.input_file = Path(input_file)
        self.config_dir = self.input_file.parent  # config/semantic_models/

    def load_model(self) -> Dict[str, Any]:
        """Load the semantic model from YAML file"""
        print(f"📖 Loading semantic model from: {self.input_file}")
        with open(self.input_file, 'r', encoding='utf-8') as f:
            model = yaml.safe_load(f)
        print(f"✅ Loaded model: {model.get('name', 'Unknown')}")
        return model

    def _write_yaml(self, data: Dict[str, Any], path: Path):
        """Write YAML to path, only if the file already exists."""
        if not path.exists():
            print(f"   ⏭️  Skipped (not found): {path.name}")
            return False
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False,
                      allow_unicode=True, width=120)
        print(f"   ✅ Updated: {path.name}")
        return True

    def split_schema(self, model: Dict[str, Any]):
        """Write one YAML per table into schema/, replacing only existing files."""
        schema_dir = self.config_dir / 'schema'
        tables = model.get('tables', [])
        updated, skipped = 0, 0

        print(f"\n📂 schema/  ({len(tables)} tables in source)")
        for table in tables:
            table_name = table.get('name', 'unknown').lower()
            path = schema_dir / f"{table_name}.yaml"
            if self._write_yaml(table, path):
                updated += 1
            else:
                skipped += 1

        print(f"   → {updated} updated, {skipped} skipped")

    def split_instructions(self, model: Dict[str, Any]):
        """Replace instructions/instructions.yaml if it exists."""
        instructions_dir = self.config_dir / 'instructions'
        path = instructions_dir / 'instructions.yaml'
        data = {'instructions': model.get('instructions', [])}
        count = len(data['instructions']) if isinstance(data['instructions'], list) else 0

        print(f"\n📋 instructions/  ({count} rules in source)")
        self._write_yaml(data, path)

    def split_verified_queries(self, model: Dict[str, Any]):
        """Replace verified_queries/verified_queries.yaml if it exists."""
        vq_dir = self.config_dir / 'verified_queries'
        path = vq_dir / 'verified_queries.yaml'
        data = {'verified_queries': model.get('verified_queries', [])}
        count = len(data['verified_queries']) if isinstance(data['verified_queries'], list) else 0

        print(f"\n✅ verified_queries/  ({count} queries in source)")
        self._write_yaml(data, path)

    def split(self):
        """Main splitting logic"""
        print("\n" + "="*70)
        print("🔧 SEMANTIC MODEL SPLITTER")
        print("="*70 + "\n")

        # Load model
        model = self.load_model()

        print(f"\n📁 Output base: {self.config_dir}\n")

        # Split into modular files (only replaces existing)
        self.split_schema(model)
        self.split_instructions(model)
        self.split_verified_queries(model)

        print("\n" + "="*70)
        print("✅ SPLITTING COMPLETE!")
        print("="*70)
        print(f"\n📂 Config modular files: {self.config_dir}")
        print(f"   - schema/           (one file per table)")
        print(f"   - instructions/     instructions.yaml")
        print(f"   - verified_queries/ verified_queries.yaml")
        print(f"\n🚀 Next steps:")
        print(f"   1. Review the updated files")
        print(f"   2. Run: python scripts/merge_semantic_models.py")
        print(f"   3. Deploy: python scripts/deploy_semantic_model.py")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Split semantic model into modular components (replaces existing files only)',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--input',
        '-i',
        default='config/semantic_models/semantic.yaml',
        help='Input semantic model file (default: config/semantic_models/semantic.yaml)'
    )

    args = parser.parse_args()

    splitter = SemanticModelSplitter(args.input)

    try:
        splitter.split()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
