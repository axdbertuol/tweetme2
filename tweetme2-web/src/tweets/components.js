import React, { useEffect, useState } from 'react';
import { Tweet } from './detail';
import { apiTweetDetail } from './lookup';
import { FeedList } from './feed';
import { TweetCreate } from './create';
import { TweetsList } from './list';

export function FeedComponent(props) {
	const [newTweets, setNewTweets] = useState([]);
	const canTweet = props.canTweet === "false" ? false : true;
	const handleNewTweet = (newTweet) => {
		// backend api response handler
		let tempNewTweets = [...newTweets];
		tempNewTweets.unshift(newTweet); // put it to beginning of list
		setNewTweets(tempNewTweets);
	}


	return (
		<div className={props.className}>
			{canTweet === true && <TweetCreate didTweet={handleNewTweet} />}
			<FeedList newTweets={newTweets} {...props} />
		</div>
	)
}

export function TweetsComponent(props) {
	const [newTweets, setNewTweets] = useState([]);
	const canTweet = props.canTweet === "false" ? false : true;
	const handleNewTweet = (newTweet) => {
		// backend api response handler
		let tempNewTweets = [...newTweets];
		tempNewTweets.unshift(newTweet); // put it to beginning of list
		setNewTweets(tempNewTweets);
	}


	return (
		<div className={props.className}>
			{canTweet === true && <TweetCreate didTweet={handleNewTweet} />}
			<TweetsList newTweets={newTweets} {...props} />
		</div>
	)
}


export function TweetDetailComponent(props) {
	const { tweetId } = props;
	const [didLookup, setDidLookup] = useState(false);
	const [tweet, setTweet] = useState(null);

	const handleBackendLookup = (response, status) => {
		if (status === 200) {
			setTweet(response);
		} else {
			alert("There was an error fetching your tweet")
		}
	}

	useEffect(() => {
		if (didLookup === false) {
			apiTweetDetail(tweetId, handleBackendLookup)
			setDidLookup(true); //
		}
	}, [tweetId, didLookup, setDidLookup]);

	return tweet === null ? null : <Tweet tweet={tweet} className={props.className} />
}