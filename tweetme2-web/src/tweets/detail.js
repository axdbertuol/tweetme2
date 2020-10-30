import React, { useState } from 'react';
import { ActionBtn } from './buttons';
import {UserDisplayLink, UserPicture} from  '../profiles';


const ParentTweet = props => {
	const { tweet, retweeter } = props;
	return tweet.parent ? 
		<div><Tweet isRetweet hideActions retweeter={retweeter} tweet={tweet.parent} /></div> : null;
}

const Tweet = function (props) {
	const { tweet, hideActions, isRetweet, retweeter } = props;
	const [actionTweet, setActionTweet] = useState(props.tweet ? props.tweet : null);
	const path = window.location.pathname;
	const match = path.match(/(?<tweetid>\d+)/);
	const urlTweetId = match ? match.groups.tweetid : -1;
	const isDetail = `${tweet.id}` === `${urlTweetId}`;
	let className = "col-sm-6 mx-auto border rounded py-3 mb-4";
	className = isRetweet ? `${className} bd-highlight border-info` : className;

	const handleLink = (event) => {
		event.preventDefault();
		window.location.href = `/${tweet.id}`
	}
	const handlePerformAction = (newActionTweet, status) => {
		if (status === 200) {
			setActionTweet(newActionTweet);
		} else if (status === 201) {
			// let the tweet list know
			if (props.didRetweet) {
				setActionTweet(newActionTweet);
				props.didRetweet(newActionTweet);
			}
		}
	}
	return (
		<div className={className}>
			<div className="d-flex flex-column">
				{isRetweet && 
				<div className="d-flex justify-content-end">
					<small>
						Retweet via<UserDisplayLink user={retweeter} includeLink  />
					</small>
				</div>}
				<div className="justify-content-start py-3">
					<UserPicture user={tweet.user}/>
					<UserDisplayLink user={tweet.user} includeFullname includeLink />
				</div>
				<div className="justify-content-start">
					<p className="text-break">{tweet.id} - {tweet.content}</p>
					<ParentTweet tweet={tweet} retweeter={tweet.user} />
				</div>
				<div className="btn btn-group justify-content-start flex-grow-0">
					{(actionTweet && hideActions !== true) && <React.Fragment>
						<ActionBtn
							tweet={actionTweet}
							didPerformAction={handlePerformAction}
							action={{ type: 'like', display: 'Like(s)' }}
							className=" btn-primary flex-grow-0">
						</ActionBtn>
						<ActionBtn
							tweet={actionTweet}
							didPerformAction={handlePerformAction}
							action={{ type: 'unlike', display: 'Unlike' }}
							className=" btn-secondary flex-grow-0">
						</ActionBtn>
						<ActionBtn
							tweet={actionTweet}
							didPerformAction={handlePerformAction}
							action={{ type: 'retweet', display: 'Retweet' }}
							className=" btn-outline-dark flex-grow-0"
						>
						</ActionBtn>
					</React.Fragment>
					}
					{!isDetail && <button className="btn btn-sm btn-success flex-grow-0" onClick={handleLink}>View</button>}
				</div>
			</div>
		</div>
	)
}



export {
	ParentTweet,
	Tweet
}