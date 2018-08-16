function run() {
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
			p.loadPixels()
			if (!p.pixels.length) throw Error('Pixels arent loaded')
			let pixels = []
			for (let i = 0; i < p.width; i += ENV.scale.x) {
				pixels.push([])
				for (let j = 0; j < p.height; j += ENV.scale.y) {
					const pixelIndex = (i * p.width + j) * 4
					const [r, g, b] = p.pixels.slice(pixelIndex, pixelIndex + 3)
					pixels[i / ENV.scale.x][j / ENV.scale.y] = (r + g + b) / 3
				}
			}
			p.updatePixels()
			return pixels
		}

		const drawUnderMouse = () => {
			const scaledGrid = p.createVector(
				p.mouseX - p.mouseX % ENV.scale.x,
				p.mouseY - p.mouseY % ENV.scale.y
			)
			p.loadPixels()
			for (let i = scaledGrid.x; i < scaledGrid.x + ENV.scale.x; i++) {
				for (let j = scaledGrid.y; j < scaledGrid.y + ENV.scale.y; j++) {
					const pixelIndex = (j * p.width + i) * 4
					p.pixels[pixelIndex] = 255
					p.pixels[pixelIndex + 1] = 255
					p.pixels[pixelIndex + 2] = 255
				}
			}
			p.updatePixels()
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

		p.mouseDragged = drawUnderMouse
		p.mousePressed = drawUnderMouse

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
	}, 'sketch')
}
