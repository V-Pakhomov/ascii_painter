from PIL import Image, ImageDraw
import sys


ASCII_CHARS = ['#', 'W', '@', '$', '8', '%', 'w', '=', '*', '+', '~', '-', '"', "'", ' ']


def get_block_color(pix, pix_per_char, i, j):
	color = 0
	for x in range(pix_per_char['x']):
		for y in range(pix_per_char['y']):
			color += (sum(pix[x + i, y + j][:3])) / 3
	return int(color // (pix_per_char['x'] * pix_per_char['y']))


def get_pixels_per_char(width, height):
	pix_per_char = {}
	if width > 2*height:
		pix_per_char['x'] = max((1, int(width // 300)))
		pix_per_char['y'] = int(pix_per_char['x'] * 2 * height / width)
	else:
		pix_per_char['y'] = max((1, int(height // 150)))
		pix_per_char['x'] = int(pix_per_char['y'] // (2 * width / height))
	return pix_per_char


def image_to_txt(image):
	ascii_name = 'ascii_' + ''.join(image.split('/')[-1].split('.')[:-1]) + '.txt'

	try:
		image = Image.open(image)
	except FileNotFoundError as err:
		print(err)
		return None
	draw = ImageDraw.Draw(image)
	width, height = image.size
	pix = image.load()
	pix_per_char = {}
	pix_per_char['x'] = max((1, int(width // 300)))
	pix_per_char['y'] = max((1, pix_per_char['x']*2))
	with open(ascii_name, 'w') as f:
		for j in range(0, height, pix_per_char['y']):
			if j + pix_per_char['y'] > height:
				break
			for i in range(0, width, pix_per_char['x']):
				if i + pix_per_char['x'] <= width:
					color = get_block_color(pix, pix_per_char, i, j)
				else:
					break
				if color == 255:
					color -= 1
				char = ASCII_CHARS[int((len(ASCII_CHARS)*color) // 255)]
				f.write(char)
				print(char, end='')
			f.write('\n')
			print()
	
	del draw


def ascii_painter(*args):
	for image in args:
		image_to_txt(image)


if __name__ == '__main__':
	if len(sys.argv) == 1:
		print(f'Usage: python3 {sys.argv[0]} images')
		exit(1)
	ascii_painter(*sys.argv[1:])
