import React from 'react';
import { apiTweetAction } from './lookup';

const ActionBtn = function (props) {
	const { tweet, action, didPerformAction, className } = props;
	const likes = tweet.likes ? tweet.likes : 0;
	let newClassName = 'btn btn-sm' + className;

	const handleActionBackendEvent = (response, status) => {
		console.log(response, status);
		if ((status === 200 || status === 201) && didPerformAction) {
			didPerformAction(response, status);
		}
	}
	const handleClick = (event) => {
		event.preventDefault();
		apiTweetAction(tweet.id, action.type, handleActionBackendEvent)
	}

	return <button className={newClassName} onClick={handleClick}>{action.type === 'like' ? likes + ' ' + action.display : action.display}</button>

}

export {
	ActionBtn
}