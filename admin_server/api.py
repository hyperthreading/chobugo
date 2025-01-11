from admin_server.app import app


@app.get("/admin/hc")
async def healthcheck():
    return {"status": "ok"}

@app.get("/admin/nudge")
async def nudge():
    return {"status": "ok"}
