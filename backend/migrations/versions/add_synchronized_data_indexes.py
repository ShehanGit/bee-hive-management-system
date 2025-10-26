"""Add performance indexes to synchronized_data table

Revision ID: add_performance_indexes
Revises: 9f9859268411
Create Date: 2024-01-20 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_performance_indexes'
down_revision = '9f9859268411'
branch_labels = None
depends_on = None


def upgrade():
    # Add composite index for performance predictions
    # This speeds up queries that filter by hive_id and collection_timestamp
    try:
        op.create_index(
            'idx_hive_timestamp',
            'synchronized_data',
            ['hive_id', 'collection_timestamp'],
            unique=False
        )
        print("✅ Created idx_hive_timestamp index")
    except Exception as e:
        print(f"⚠️ Index idx_hive_timestamp might already exist: {e}")
    
    # Add individual index on hive_id for faster filtering
    try:
        op.create_index(
            'idx_hive_id',
            'synchronized_data',
            ['hive_id'],
            unique=False
        )
        print("✅ Created idx_hive_id index")
    except Exception as e:
        print(f"⚠️ Index idx_hive_id might already exist: {e}")
    
    # Note: collection_timestamp already has an index defined in the model (line 12)


def downgrade():
    # Drop the indexes
    try:
        op.drop_index('idx_hive_timestamp', table_name='synchronized_data')
        print("✅ Dropped idx_hive_timestamp index")
    except Exception as e:
        print(f"⚠️ Could not drop idx_hive_timestamp: {e}")
    
    try:
        op.drop_index('idx_hive_id', table_name='synchronized_data')
        print("✅ Dropped idx_hive_id index")
    except Exception as e:
        print(f"⚠️ Could not drop idx_hive_id: {e}")

