// SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)
//
// SPDX-License-Identifier: MPL-2.0

import { redirect } from '@sveltejs/kit';
import { signedIn } from '$lib/stores';
export async function load({ parent, locals }) {
	const { email } = await parent();
	if (!email) {
		throw redirect(302, '/account/login?returnTo=/import-admin');
	} else {
		if (email) {
			signedIn.set(true);
		}
		if (locals.admin_user === false) {
			throw redirect(302, '/dashboard');
		} else if (locals.admin_user === undefined) {
			throw redirect(302, '/dashboard');
		}
	}
	return {
		email
	};
}
