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

import { ce } from "../../framework/element.js";
import View from "../../framework/view.js";


export default class MainView extends View {
	constructor(app, props) {
		super(app, props);
	}

	render() {
		const {
			cdb,
			innerView = null,
			innerViewProps = {},
		} = this.props;

		const { title } = cdb;

		return ce("div", { class: "cdbApp" },
			ce("header", { class: "cdbHeader" },
				ce("h1", {}, title)
			),
			innerView? ce(innerView, innerViewProps): undefined,
		);
	}
}
