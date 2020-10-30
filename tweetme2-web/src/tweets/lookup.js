import { backendLookup } from '../lookup';

export function apiTweetCreate(newTweet, callback) {
	backendLookup("POST", "/tweets/create", callback, { content: newTweet });
}
export function apiTweetAction(tweetId, action, callback) {
	backendLookup("POST", "/tweets/action", callback, { id: tweetId, action: action });
}

export function apiTweetDetail(tweetId, callback) {
	let endpoint = "/tweets/";

	if (tweetId) {
		endpoint += `${tweetId}`;
	}
	backendLookup("GET", endpoint, callback);
}
export function apiTweetList(username, callback, nextUrl) {
	let endpoint = "/tweets/";

	if (username) {
		endpoint += `?username=${username}`;
	}
	if (nextUrl !== null && nextUrl !== undefined) {
		endpoint = nextUrl.replace("http://localhost:8000/api", "")
	}
	backendLookup("GET", endpoint, callback);
}

export function apiTweetFeed(callback, nextUrl) {
	let endpoint = "/tweets/feed";


	if (nextUrl !== null && nextUrl !== undefined) {
		endpoint = nextUrl.replace("http://localhost:8000/api", "")
	}
	backendLookup("GET", endpoint, callback);
}
