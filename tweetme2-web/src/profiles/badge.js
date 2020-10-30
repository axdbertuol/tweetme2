import React, { useState, useEffect } from 'react';
import numeral from 'numeral';
import { apiProfileDetail, apiProfileFollowToggle } from './lookup';
import { UserDisplayLink, UserPicture } from './components';

import {DisplayCount} from './utils';



function ProfileBadge(props) {
	const { user, didFollowToggle, profileLoading } = props;
	const currentVerb = profileLoading ? "Loading..." : (user && user.is_following) ? "Unfollow" : "Follow";
	
	const handleFollowToggle = (event) =>{
		event.preventDefault();
		if (didFollowToggle && !profileLoading){
			didFollowToggle(currentVerb);
		}
	}
	return (user &&
		<div className="d-flex">
			<div className="p-2">
				<UserPicture user={user} />
			</div>
			<div className="p-2">
				<p><UserDisplayLink user={user} includeFullname includeLink></UserDisplayLink></p>
			</div>
			<div className="p-2">
				<span className="badge badge-primary"><DisplayCount color="green" number={user.follower_count} /> follower(s)</span>
			</div>
			<div className="p-2">
				<span className="badge badge-secondary"><DisplayCount number={user.following_count} /> following</span>
			</div>
			<div className="p-2">
				<button className="btn btn-primary" onClick={handleFollowToggle}>{currentVerb}</button>
			</div>
		</div>)
}

export function ProfileBadgeComponent(props) {
	const { username } = props;
	const [didLookup, setDidLookup] = useState(false);
	const [profile, setProfile] = useState(null);
	const [profileLoading, setProfileLoading] = useState(false); // for controlling toggles

	const handleBackendLookup = (response, status) => {
		if (status === 200) {
			setProfile(response);
		}
	}

	useEffect(() => {
		if (didLookup === false) {
			apiProfileDetail(username, handleBackendLookup);
			setDidLookup(true); //
		}
	}, [username, didLookup, setDidLookup]);

	const handleNewFollow = (actionVerb) => {
		apiProfileFollowToggle(username, actionVerb, (response, status) => {
			console.log(response, status);
			if (status === 200) {
				setProfile(response); // set asynchronously
			}
			setProfileLoading(false);
		})
		setProfileLoading(true);
	}
	// if (profile === null) {
	// 	return "Could not render profile."
	// }
	return didLookup === false ? "Loading.." : profile && <ProfileBadge user={profile} didFollowToggle={handleNewFollow} profileLoading={profileLoading}></ProfileBadge>;
}