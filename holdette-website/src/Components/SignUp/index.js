import { Auth } from 'aws-amplify';
import React, { Component } from "react";

class SignUp extends Component {
	constructor(props) {
		super(props);
		this.state = {};
		this.onSubmit = this.onSubmit.bind(this);

	}

	onSubmit(event) {

	}
	render() {
		return (
			<div>
				<form onSubmit={this.handleSubmit}>
			        <label>
			            Name:
			        	<input type="text" value={this.state.value} onChange={this.handleChange} />
				    </label>
				    
			        <input type="submit" value="Submit" />
			    </form>
			</div>
		);
	}
}

