// SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)
//
// SPDX-License-Identifier: MPL-2.0

import type { Handle } from '@sveltejs/kit';
import jws from 'jws';

/** @type {import('@sveltejs/kit').Handle} */
export const handle: Handle = async ({ event, resolve }) => {
	const access_token = event.cookies.get('access_token');
	if (!access_token) {
		event.locals.email = null;
		event.locals.admin_user = false;
		return resolve(event);
	}
	const jwt = jws.decode(access_token.replace('Bearer ', ''));
	// if token expires, do a request to get a new one and set the response-cookies on the response
	if (Date.now() >= jwt.payload.exp * 1000) {
		const res = await fetch(`${process.env.API_URL}/api/v1/users/check`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				Cookie: event.request.headers.get('cookie') || ''
			}
		});
		if (res.ok) {
			const userData = await res.json();
			event.locals.email = userData.email;
			event.locals.admin_user = userData.admin_user;
			const resp = await resolve(event);
			try {
				resp.headers.set('Set-Cookie', res.headers.get('set-cookie'));
			} catch {
				/* empty */
			}
			return resp;
		}
	}

	event.locals.email = jwt.payload.sub;

	const res = await fetch(`${process.env.API_URL}/api/v1/users/check`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Cookie: event.request.headers.get('cookie') || ''
		}
	});
	if (res.ok) {
		const userData = await res.json();
		event.locals.admin_user = userData.admin_user;
	} else {
		event.locals.admin_user = false; // Default to false if the request fails
	}

	return resolve(event);
};