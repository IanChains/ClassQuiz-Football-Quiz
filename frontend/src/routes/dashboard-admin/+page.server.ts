// SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)
//
// SPDX-License-Identifier: MPL-2.0

import { redirect } from '@sveltejs/kit';

export const load = async ({ parent }) => {
	const { email } = await parent();
	const { admin_user } = await parent();
	if (!email) {
		throw redirect(302, '/account/login?returnTo=/dashboard-admin');
	} else if (admin_user === false) {
		throw redirect(302, '/dashboard');
	}
	return {
		email
	};
};
