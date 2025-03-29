// SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)
//
// SPDX-License-Identifier: MPL-2.0

import { redirect } from '@sveltejs/kit';

export async function load({ locals }) {
	if (!locals.email) {
		throw redirect(302, '/account/login?returnTo=/dashboard');
	} else if (locals.admin_user === true) {
		throw redirect(302, '/dashboard-admin');
	}
	return {
		email: locals.email,
	};
};
