from PIL import Image

ASCII_CHARS = ['⠀', '⠄', '⠆', '⠖', '⠶', '⡶', '⣩', '⣪', '⣫', '⣾', '⣿']
ASCII_CHARS.reverse()
ASCII_CHARS = ASCII_CHARS[::-1]

class Renderer:
    @staticmethod
    def resize(image, new_width):
        (old_width, old_height) = image.size
        aspect_ratio = float(old_height) / float(old_width)
        new_height = int((aspect_ratio * new_width) / 2)
        new_dim = (new_width, new_height)
        new_image = image.resize(new_dim)
        return new_image

    @staticmethod
    def grayscalify(image):
        return image.convert('L')

    @staticmethod
    def modify(image, buckets=25):
        initial_pixels = list(image.getdata())
        new_pixels = [ASCII_CHARS[pixel_value // buckets] for pixel_value in initial_pixels]
        return ''.join(new_pixels)

    @staticmethod
    def do(image, new_width):
        image = Renderer.resize(image, new_width)
        image = Renderer.grayscalify(image)

        pixels = Renderer.modify(image)
        len_pixels = len(pixels)

        new_image = [pixels[index:index + int(new_width)] for index in range(0, len_pixels, int(new_width))]

        return '\n'.join(new_image)

    @staticmethod
    def runner(path, width):
        image = None
        try:
            image = Image.open(path)
        except Exception:
            print("Unable to find image in", path)
            return
        image = Renderer.do(image, width)

        return image
