import React, { Component } from 'react'
// Configure Amplify
import Amplify, { Auth } from 'aws-amplify';
import awsmobile from './aws-exports';
Amplify.configure(awsmobile);

class App extends Component {
	render() {
		return (
			<h1>Wow</h1>
		);
	}
}

export default App;