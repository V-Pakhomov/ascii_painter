from PIL import Image, ImageDraw
import sys
import os


ASCII_CHARS = ['#', 'W', '@', '$', '8', '%', 'w', '=', '*', '+', '~', '-', '"', "'", ' ']


def get_block_color(pix, pix_per_char, i, j):
	color = 0
	for x in range(pix_per_char['x']):
		for y in range(pix_per_char['y']):
			try:
				r, g, b = pix[x + i, y + j][:3]
				pix_color = (r + g + b) / 3
			except ValueError:
				pix_color = 255 - pix[x + i, y + j][1]
			color += pix_color
	return int(color // (pix_per_char['x'] * pix_per_char['y']))


def image_to_txt(image):
	_, filename = os.path.split(image)
	filename = os.path.splitext(filename)[0]
	ascii_name = 'results/' + filename + '.txt'

	try:
		image = Image.open(image)
	except FileNotFoundError as err:
		print(err)
		return None
	draw = ImageDraw.Draw(image)
	width, height = image.size
	pix = image.load()
	pix_per_char = {}
	pix_per_char['x'] = max((1, int(width // 200)))
	pix_per_char['y'] = max((1, pix_per_char['x']*2))
	with open(ascii_name, 'w') as f:
		for j in range(0, height, pix_per_char['y']):
			if j + pix_per_char['y'] > height:
				break
			for i in range(0, width, pix_per_char['x']):
				if i + pix_per_char['x'] > width:
					break
				color = get_block_color(pix, pix_per_char, i, j)
				if color == 255:
					color -= 1
				char = ASCII_CHARS[int((len(ASCII_CHARS)*color) // 255)]
				f.write(char)
				print(char, end='')
			f.write('\n')
			print()
	
	del draw


def ascii_painter(*args):
	if not 'results' in os.listdir():
		os.mkdir('results')
	for image in args:
		_, filename = os.path.split(image)
		print(f'{filename}:'.upper())
		image_to_txt(image)
		print('\n\n')


if __name__ == '__main__':
	if len(sys.argv) == 1:
		print(f'Usage: python3 {sys.argv[0]} images')
		exit(1)
	ascii_painter(*sys.argv[1:])
