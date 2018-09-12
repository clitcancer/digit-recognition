new p5(p => {
	const ENV = {
		scale: p.createVector(5, 5),
		imgSize: p.createVector(28, 28),
		canvas: null
	}

	p.setup = () => {
		ENV.canvas = p.createCanvas(ENV.scale.x * ENV.imgSize.x, ENV.scale.y * ENV.imgSize.y)
		p.pixelDensity(1)
		p.background(0)
		ENV.canvas.dragOver(fileOver)
		ENV.canvas.dragLeave(clearCanvas)
		ENV.canvas.drop(fileDropped) // its cancelling out dragOver and dragLeave wtf
	}

	const clearCanvas = () => p.background(0)

	const exportPixelData = () => {
		let copy = ENV.canvas.get() 
		copy.resize(ENV.imgSize.x, ENV.imgSize.y)

		copy.loadPixels()
		let pixels = []
		for (let i = 0; i < copy.width; i++) {
			pixels.push([])
			for (let j = 0; j < copy.height; j++) {
				const pixelIndex = (i * copy.width + j) * 4
				const [r, g, b] = copy.pixels.slice(pixelIndex, pixelIndex + 3)
				pixels[i][j] = (r + g + b) / 3
			}
		}
		copy.updatePixels()
		return pixels.reduce((prev, curr) => [...prev, ...curr], []).map(e => e/255)
	}

	p.draw = () => {
		if(p.mouseIsPressed) {
			p.noStroke()
			p.ellipse(p.mouseX, p.mouseY, ENV.scale.x*2, ENV.scale.y*2);
		}
	}

	const fileOver = () => {
		p.background(255)
			.stroke(0)
			.textSize(16)
			.textAlign(p.CENTER, p.CENTER)
			.text('Dropping file...', p.width / 2, p.height / 2)
	}

	const fileDropped = file => {
		let i = new Image()
		i.onload = () => i.width !== ENV.imgSize.x || i.height !== ENV.imgSize.y || file.type !== 'image' ?
			p.background(255)
				.stroke(0)
				.textSize(16)
				.textAlign(p.CENTER, p.CENTER)
				.text(`file is not ${ENV.imgSize.x}x${ENV.imgSize.y}`, p.width / 2, p.height / 2)
			:
			drawImage(i)
		i.src = file.data
	}

	const drawImage = image => {
		const canvas = document.querySelector('canvas')
		const context = canvas.getContext('2d')
		context.imageSmoothingEnabled = false
		context.drawImage(image, 0, 0, image.width * ENV.scale.x, image.height * ENV.scale.y)
	}

	document.querySelector('#takeGuess').addEventListener('click', event => {
		fetch('/api/guess', {
			method: 'POST',
			body: JSON.stringify({
				pixels: exportPixelData()
			})
		}).then(res => res.json())
			.then(body => document.querySelector('#guess').innerText = body.guess)
			.catch(console.error)
	})

	document.querySelector('#resetCanvas').addEventListener('click', clearCanvas)

	document.querySelector('#saveCanvas').addEventListener('click', event => {
		let img = ENV.canvas.get()
		img.resize(ENV.imgSize.x, ENV.imgSize.y)
		img.save('digit', 'png')
	})

}, 'sketch')
