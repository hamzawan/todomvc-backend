revision = "0000000006"
down_revision = "0000000005"



def upgrade(migration):
    migration.create_table(
        "task",
        """
            "entity_id" varchar(32) NOT NULL,
            "version" varchar(32) NOT NULL,
            "previous_version" varchar(32) DEFAULT '00000000000000000000000000000000',
            "active" boolean DEFAULT true,
            "changed_by_id" varchar(32) DEFAULT NULL,
            "changed_on" timestamp NULL DEFAULT CURRENT_TIMESTAMP,
            "title" varchar(255) NOT NULL,
            "description" text DEFAULT NULL,
            "status" varchar(50) DEFAULT 'incomplete',
            "priority" varchar(50) DEFAULT 'medium',
            "assigned_to_id" varchar(32) DEFAULT NULL,
            "organization_id" varchar(32) DEFAULT NULL,
            "due_date" timestamp DEFAULT NULL,
            PRIMARY KEY ("entity_id")
        """
    )
    migration.add_index("task", "tasks_assigned_to_id_ind", "assigned_to_id")
    migration.add_index("task", "tasks_organization_id_ind", "organization_id")
    migration.add_index("task", "tasks_status_ind", "status")
    migration.add_index("task", "tasks_priority_ind", "priority")

    migration.create_table(
        "task_audit",
        """
            "entity_id" varchar(32) NOT NULL,
            "version" varchar(32) NOT NULL,
            "previous_version" varchar(32) DEFAULT '00000000000000000000000000000000',
            "active" boolean DEFAULT true,
            "changed_by_id" varchar(32) DEFAULT NULL,
            "changed_on" timestamp NULL DEFAULT CURRENT_TIMESTAMP,
            "title" varchar(255) NOT NULL,
            "description" text DEFAULT NULL,
            "status" varchar(50) DEFAULT 'incomplete',
            "priority" varchar(50) DEFAULT 'medium',
            "assigned_to_id" varchar(32) DEFAULT NULL,
            "organization_id" varchar(32) DEFAULT NULL,
            "due_date" timestamp DEFAULT NULL,
            PRIMARY KEY ("entity_id", "version")
        """
    )

    migration.update_version_table(version=revision)


def downgrade(migration):

    migration.update_version_table(version=down_revision)

