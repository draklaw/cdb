// This file is part of cdb.
//
// Copyright (C) 2019  the authors (see AUTHORS)
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

import Model from "../../framework/model.js";


export const loginStatus = {
	disconnected: "disconnected",
	pending:      "pending",
	connected:    "connected",
};

export default class LoginModel extends Model {
	constructor(parent) {
		super(parent);

		this.user = null;
		this.status = loginStatus.disconnected;
		this.attempts = 0;
	}
}
