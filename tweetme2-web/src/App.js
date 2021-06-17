import React from 'react';
import './App.css';
import { ThemeProvider } from '@material-ui/styles';
import {theme} from './twitterTheme';
import { Sidebar } from './layout';




function App() {

  return (
		<div className="app">
			<ThemeProvider theme={theme}>
				<Sidebar/>
				<div className="tweetme-2-profile-badge" data-username="xad"></div>
			</ThemeProvider>
		</div>
	)
}

export default App;
