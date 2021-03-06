import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import Divider from '@material-ui/core/Divider';
import HomeIcon from "@material-ui/icons/Home";
import PermIdentityIcon from "@material-ui/icons/PermIdentity";

const useStyles = makeStyles((theme) => ({
	root: {
		color: theme.palette.text.secondary,
		'&:hover': {
			backgroundColor: theme.palette.primary.light,
			color: theme.palette.text.primary,
		},
	},
	selected: {
		'&.Mui-selected': {
			backgroundColor: 'transparent',
			color: theme.palette.text.primary,
			fontWeight: 500,
			'&:hover, &:focus': {
				backgroundColor: theme.palette.primary.main,
			},
		},
	},
}))


function ListItemLink(props) {
	return <ListItem button component="a" {...props} />;
}


export default function Sidebar(props) {
	const classes = useStyles();
	return (
		<div className="sidebar">
			<List component="nav" aria-label="main menu folders">
				{ props.username && <React.Fragment> 
					<ListItem classes={classes} button onClick={(event) => { event.preventDefault(); window.location.href = ''; }}>
						<ListItemIcon>
							<HomeIcon />
						</ListItemIcon>
						<ListItemText primary="Home" />
					</ListItem>
					<ListItem classes={classes} button onClick={(event) => { event.preventDefault(); window.location.href = `/profile/${props.username}`; }}>
						<ListItemIcon>
							<PermIdentityIcon />
						</ListItemIcon>
						<ListItemText primary="Profile" />
					</ListItem>
				</React.Fragment>}
				<ListItem classes={classes} button onClick={(event) => { event.preventDefault(); window.location.href = `/login`; }}>
					<ListItemIcon>
						<HomeIcon />
					</ListItemIcon>
					<ListItemText primary="Login" />
				</ListItem>
				<ListItem classes={classes} button onClick={(event) => { event.preventDefault(); window.location.href = `/register`; }}>
					<ListItemIcon>
						<PermIdentityIcon />
					</ListItemIcon>
					<ListItemText primary="Register" />
				</ListItem>
			</List>
			<Divider />
			<List component="nav" aria-label="secondary mailbox folders">
				<ListItem button>
					<ListItemText primary="Trash" />
				</ListItem>
				<ListItemLink href="#simple-list">
					<ListItemText primary="Spam" />
				</ListItemLink>
			</List>
		</div>
	);
}

