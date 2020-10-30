import React  from 'react';

export function UserDisplayLink(props) {
	const { user, includeFullname, includeLink } = props;

	const handleUserLink = (event) => {
		window.location.href = `/profile/${user.username}`;
	}

	return (
		<React.Fragment>
			{includeFullname && <span className="pl-3">{user.first_name} {user.last_name}</span>}
			{includeLink && 
				<span className="pl-1 pointer" onClick={handleUserLink}>@{user.username}</span>
			}
		</React.Fragment>
	)
}
export function UserPicture(props) {
	const { user } = props;
	return (
		<span className="px-3 py-2 rounded-circle bg-dark text-white">
			{user.username[0]}
		</span>
	)
}