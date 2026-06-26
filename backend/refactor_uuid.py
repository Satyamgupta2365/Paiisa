import re

def refactor(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # In models.py
    content = content.replace("Mapped[uuid.UUID] = mapped_column(SA_Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)", "Mapped[str] = mapped_column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))")
    content = content.replace("user_id: Mapped[uuid.UUID] = mapped_column(SA_Uuid(as_uuid=True), ForeignKey('users.id'), index=True)", "user_id: Mapped[str] = mapped_column(String(50), ForeignKey('users.id'), index=True)")
    content = content.replace("user_id: Mapped[uuid.UUID] = mapped_column(SA_Uuid(as_uuid=True)", "user_id: Mapped[str] = mapped_column(String(50)")

    with open(filepath, 'w') as f:
        f.write(content)

refactor('database/models.py')

def refactor_schemas(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    content = content.replace("user_id: Optional[UUID] = None", "user_id: Optional[str] = None")
    content = content.replace("user_id: UUID", "user_id: str")
    content = content.replace("id: UUID", "id: str")

    with open(filepath, 'w') as f:
        f.write(content)

refactor_schemas('models/schemas.py')

def refactor_routes(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    content = content.replace("user_id: UUID", "user_id: str")
    with open(filepath, 'w') as f:
        f.write(content)

import os
for root, dirs, files in os.walk('routes'):
    for file in files:
        if file.endswith('.py'):
            refactor_routes(os.path.join(root, file))

print("Refactored UUIDs!")
