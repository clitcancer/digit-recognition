class CanvasWrapper extends React.Component {
	render() {
		const { id } = this.props

		return (
			<p id={id}></p>
		)
	}
}

class Button extends React.Component {
	render() {
		const { onClick, id, text } = this.props

		return (
			<button id={id} onClick={onClick}>{text}</button>
		)
	}
}

class GuessBox extends React.Component {
	render() {
		return (
			<div id="msg">
				My guess is <span id="guess"></span>
			</div>
		)
	}
}

function App() {
	return (
		<React.Fragment>
			<CanvasWrapper id={'sketch'} />
			<Button
				id={'takeGuess'}
				text={'Guess!'}
			/>
			<Button
				id={'resetCanvas'}
				text={'Reset canvas!'}
			/>
			<Button
				id={'saveCanvas'}
				text={'Save as image!'}
			/>
			<GuessBox />
		</React.Fragment>
	)
}

ReactDOM.render(
	<App />,
	document.getElementById('root')
)

run()
