import os
main_path = "backend/app/main.py"
if os.path.exists(main_path):
    with open(main_path, "r", encoding="utf-8") as f:
        content = f.read()
    if "core_api.router" not in content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "from fastapi" in line:
                lines.insert(i + 1, "from app.routers import core_api")
                break
        for i, line in enumerate(lines):
            if "app.include_router" in line:
                lines.insert(i + 1, "app.include_router(core_api.router)")
                break
        with open(main_path, "w", encoding="utf-8") as f:
            f.write('\n'.join(lines))
