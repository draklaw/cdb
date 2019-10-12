#!/usr/bin/env python3

# This file is part of cdb.
#
# Copyright (C) 2019  the authors (see AUTHORS)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
import aiofiles

import cdb_api

app = Starlette(debug=True)

static_files = StaticFiles(directory="static")
app.mount("/static", static_files, name="static")

app.mount("/api", cdb_api.app)


@app.route("/")
async def index(request: Request):
    path, _ = await static_files.lookup_path("index.html")
    async with aiofiles.open(path, "r") as f:
        index = await f.read()
    return HTMLResponse(index.format(
        lang="en",
        title="Collections",
        stylesheet=request.url_for("static", path="/style.css"),
        main_js=request.url_for("static", path="/cdb.js")
    ))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
