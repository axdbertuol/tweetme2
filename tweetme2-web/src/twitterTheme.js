import { createMuiTheme } from '@material-ui/core/styles';
import blue from '@material-ui/core/colors/blue';
import './App.css';
// import black from '@material-ui/core/colors/black';

const theme = createMuiTheme({
	palette: {
		primary: {
			main: '#50b7f5'
		},
	},
});

export {
	theme
}