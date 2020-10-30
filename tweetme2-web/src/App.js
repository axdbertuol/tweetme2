import React from 'react';
import logo from './logo.svg';
import './App.css';
import { ThemeProvider } from '@material-ui/styles';
import {theme} from './twitterTheme';
import { Sidebar } from './layout';

import { FeedComponent } from './tweets';



function App() {

  return (
		<div className="app">
			<ThemeProvider theme={theme}>
				<Sidebar/>
			</ThemeProvider>
		</div>
	)
}

export default App;
