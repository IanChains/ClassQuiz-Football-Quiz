// SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)
//
// SPDX-License-Identifier: MPL-2.0

import { redirect, error } from '@sveltejs/kit';
import { signedIn } from '$lib/stores';

export async function load({ url, locals }) {
	const quiz_id = url.searchParams.get('quiz_id');
	if (!locals.email) {
		throw redirect(302, `/account/login?returnTo=/dashboard-admin`);
	}

	if (locals.email) {
		signedIn.set(true);
	}

	if (locals.admin_user === false) {
		throw redirect(302, '/dashboard');
	} else if (locals.admin_user === undefined) {
		throw redirect(302, '/dashboard');
	}

	if (quiz_id === null) {
		throw error(404);
	}

	return {
		quiz_id
	};
}
