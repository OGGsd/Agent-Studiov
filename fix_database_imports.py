#!/usr/bin/env python3
"""
Fix langflow imports in database stored component code.
This script updates any stored component code in the database that still references langflow imports.
"""

import asyncio
import json
import re
from sqlalchemy import text
from sqlmodel import select
from axie_studio.services.database.models.flow.model import Flow
from axie_studio.services.deps import get_db_service

async def fix_database_imports():
    """Fix langflow imports in stored component data."""
    print("🔧 Fixing langflow imports in database...")

    db_service = get_db_service()

    async with db_service.with_session() as session:
        # Get all flows
        result = await session.exec(select(Flow))
        flows = result.all()

        updated_count = 0

        for flow in flows:
            if flow.data and isinstance(flow.data, dict):
                # Convert to JSON string for easier regex replacement
                data_str = json.dumps(flow.data, indent=2)
                original_data_str = data_str

                # More comprehensive langflow import replacements
                replacements = [
                    # Direct module imports
                    (r'from langflow\.', 'from axie_studio.'),
                    (r'import langflow\.', 'import axie_studio.'),
                    # Specific problematic imports
                    (r'langflow\.base\.prompts\.api_utils', 'axie_studio.base.prompts.api_utils'),
                    (r'langflow\.custom\.custom_component\.component', 'axie_studio.custom.custom_component.component'),
                    (r'langflow\.interface\.custom\.custom_component', 'axie_studio.interface.custom.custom_component'),
                    (r'langflow\.template\.field\.base', 'axie_studio.template.field.base'),
                    (r'langflow\.inputs', 'axie_studio.inputs'),
                    (r'langflow\.schema', 'axie_studio.schema'),
                    # Any remaining langflow references in code strings
                    (r'"langflow\\.', '"axie_studio.'),
                    (r"'langflow\\.", "'axie_studio."),
                ]

                # Apply all replacements
                for pattern, replacement in replacements:
                    data_str = re.sub(pattern, replacement, data_str)

                # If changes were made, update the flow
                if data_str != original_data_str:
                    try:
                        flow.data = json.loads(data_str)
                        session.add(flow)
                        updated_count += 1
                        print(f"✅ Updated flow: {flow.name} (ID: {flow.id})")
                    except json.JSONDecodeError as e:
                        print(f"❌ Error updating flow {flow.name}: {e}")

        if updated_count > 0:
            await session.commit()
            print(f"🎉 Successfully updated {updated_count} flows!")
        else:
            print("ℹ️ No flows needed updating.")

async def clear_component_cache():
    """Clear any component cache that might contain old imports."""
    print("🧹 Clearing component cache...")
    
    # Clear any cached component data
    try:
        from axie_studio.interface.components import component_cache
        if hasattr(component_cache, 'all_types_dict'):
            component_cache.all_types_dict = None
        if hasattr(component_cache, '_cache'):
            component_cache._cache.clear()
        print("✅ Component cache cleared!")
    except Exception as e:
        print(f"⚠️ Could not clear component cache: {e}")

async def main():
    """Main function to fix database imports."""
    print("🚀 Starting database import fix...")
    
    try:
        await fix_database_imports()
        await clear_component_cache()
        print("✅ Database import fix completed successfully!")
        print("\n🔄 Please restart the server to apply changes.")
    except Exception as e:
        print(f"❌ Error fixing database imports: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
