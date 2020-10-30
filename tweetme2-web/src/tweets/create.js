import React  from 'react';
import { apiTweetCreate } from './lookup';

export function TweetCreate(props) {
	const textAreaRef = React.createRef();
	const { didTweet } = props;

	const handleBackendUpdate = (response, status) => {
		// backend api response handler
		if (status === 201) {
			didTweet(response);
		} else {
			alert("An error occurred while processing new tweet")
		}
	}


	const handleSubmit = (event) => {
		event.preventDefault();
		const newVal = textAreaRef.current.value;
		// backend api request handler
		apiTweetCreate(newVal, handleBackendUpdate);
		textAreaRef.current.value = '';
	}

	return (
		<div className={props.className}>
			<div className="col-12 mb-3">
				<form onSubmit={handleSubmit}>
					<textarea ref={textAreaRef} required={true} className="form-control" name="tweet"></textarea>
					<button type="submit" className="btn btn-primary my-3">Tweet</button>
				</form>
			</div>
		</div>
	)
}