from pathlib import Path

import modal


APP_NAME = "yail-university"
DIST_DIR = Path(__file__).parent / "yail-university-ui" / "dist"

image = (
    modal.Image.debian_slim()
    .pip_install("fastapi")
    .add_local_dir(DIST_DIR, remote_path="/assets")
)

app = modal.App(APP_NAME)


@app.function(image=image)
@modal.concurrent(max_inputs=100)
@modal.asgi_app()
def web():
    from fastapi import FastAPI
    from fastapi.responses import FileResponse

    assets = Path("/assets")
    web_app = FastAPI()

    @web_app.get("/{path:path}")
    async def serve_frontend(path: str):
        candidate = assets / (path or "index.html")
        if candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(assets / "index.html")

    return web_app
