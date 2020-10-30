import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { ProfileBadgeComponent} from './profiles'
import { FeedComponent, TweetsComponent, TweetDetailComponent} from './tweets';
import * as serviceWorker from './serviceWorker';

const appEl = document.getElementById('root');
if (appEl) {
  ReactDOM.render(
    <React.StrictMode>
			<App />
    </React.StrictMode>,
    document.getElementById('root')
  );
}


const e = React.createElement; 
const tweetsEl = document.getElementById('tweetme-2');
if (tweetsEl) {
	const JointComponent = e(TweetsComponent, tweetsEl.dataset);
  ReactDOM.render(JointComponent, tweetsEl);
}
const tweetFeedEl = document.getElementById('tweetme-2-feed');
if (tweetFeedEl) {
	const JointComponent = e(FeedComponent, tweetFeedEl.dataset);
  ReactDOM.render(JointComponent, tweetFeedEl);
}

const tweetDetailElements = document.querySelectorAll(".tweetme-2-detail");

tweetDetailElements.forEach(container => {
	const JointComponent = e(TweetDetailComponent, container.dataset);
	ReactDOM.render(JointComponent, container);
})

const profileBadgeElement = document.querySelectorAll(".tweetme-2-profile-badge");

profileBadgeElement.forEach(container => {
	const JointComponent = e(ProfileBadgeComponent, container.dataset);
	ReactDOM.render(JointComponent, container);
})
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
