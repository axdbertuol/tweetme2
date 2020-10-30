import React, { useEffect, useState } from 'react';
import { apiTweetList } from './lookup';
import { Tweet } from './detail';

const TweetsList = function (props) {
	const [tweetsInit, setTweetsInit] = useState([]); // initial tweets
	const [tweets, setTweets] = useState([]); // initial + new tweets
	const [nextUrl, setNextUrl] = useState(null);
	const [tweetsDidSet, setTweetsDidSet] = useState(false); // stop constant reloading 

	useEffect(() => {
		console.log("set final tweets")
		let final = [...props.newTweets].concat(tweetsInit);
		if (final.length !== tweets.length) {
			setTweets(final);
		}
	}, [props.newTweets, tweets, tweetsInit])

	useEffect(() => {
		if (tweetsDidSet === false) {
			const handleTweetsListLookup = (response, status) => {
				if (status === 200) {
					setNextUrl(response.next)
					setTweetsInit(response.results);
					setTweetsDidSet(true);
					console.log("handleTweetsListLookup", tweetsDidSet)
				} else {
					// setTweetsDidSet(false);
					alert(response, status);
				}
			}
			apiTweetList(props.username, handleTweetsListLookup)
		}
		// do my lookup to backend
	}, [props.username, tweetsInit, tweetsDidSet, setTweetsDidSet])

	const handleDidRetweet = (newTweet) => {
		const updatedTweetsInit = [...tweetsInit];
		updatedTweetsInit.unshift(newTweet);
		setTweetsInit(updatedTweetsInit);
		const updatedFinalTweets = [...tweets];
		updatedFinalTweets.unshift(tweets);
		setTweets(updatedFinalTweets);
		console.log("updatedFinalTweets", updatedFinalTweets)
	}

	const handleLoadNext = (event) => {
		event.preventDefault();
		if (nextUrl !== null) {
			const handleLoadNextResponse = (response, status) => {
				if (status === 200) {
					console.log("handleLoadNextResponse")
					setNextUrl(response.next)
					const newTweets = [...tweets].concat(response.results)
					setTweetsInit(newTweets);
					setTweets(newTweets)
					// setTweetsDidSet(true);
				} else {
					alert(response, status);
				}
			}
			apiTweetList(props.username, handleLoadNextResponse, nextUrl)
		}
	}
	return <React.Fragment>{tweets.map((item, index) => {
		return <Tweet
			tweet={item}
			didRetweet={handleDidRetweet}
			key={`${index}- ${item.id}`}
			updateTweetsDidSet={(isSet) => { setTweetsDidSet(isSet) }}
		/>
	})}
	{ nextUrl !== null && <button onClick={handleLoadNext} className="btn btn-outline-primary btn-sm">Load next</button>}
	</React.Fragment>


}

export {
	TweetsList
}