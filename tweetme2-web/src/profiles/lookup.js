import { backendLookup } from '../lookup';

export function apiProfileDetail(username, callback) {
	let endpoint = "/profiles/";

	if (username) {
		endpoint += `${username}`;
	}
	backendLookup("GET", endpoint, callback);
}

export function apiProfileFollowToggle(username, action, callback) {
	const data = {'action': `${ action && action}`.toLowerCase()};
	backendLookup("POST", `/profile/${username}/follow`, callback, data);
}