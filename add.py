import info

import os
import random

from quotes_files import get_quotes_from_files
from quotes_api import get_quotes_from_api

from PIL import Image, ImageDraw, ImageFont

def get_words(words_list: list[str], start: int, end: int) -> str:
    """Gets the words from the word list at the specified indices"""
    joined = ''
    stop = min(end, len(words_list))
    for i in range(start, stop):
        joined += words_list[i] + ' '
    return joined.strip()

def split_quotes(quote: str) -> list[str]:
    """Splits a quote that is too long and returns a list"""
    words_list = quote.split(' ')
    quotes_list = []
    WORDS_PER_SENTENCE = 3
    for i in range(len(words_list) // WORDS_PER_SENTENCE + 1):
        start = WORDS_PER_SENTENCE * i; end = WORDS_PER_SENTENCE * (i + 1)
        quotes_list.append(get_words(words_list, start, end))
    return quotes_list

def add_quote_to_images(quote: str, author: str, photos_folder: str, output_folder: str, photo: str, font_chosen=None):
    """Add quotes to images in the specified folder."""
    os.makedirs(output_folder + '/' + photo, exist_ok=True)
    for filename in os.listdir(photos_folder + '/' + photo):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            lines_list = split_quotes(quote) if len(quote) >= 30 else [quote]
            if author is not None:
                lines_list.append(f"- {author}")
            img_path = os.path.join(photos_folder + '/' + photo, filename)
            img = Image.open(img_path).convert("L")
            draw = ImageDraw.Draw(img)
            try:
                # TODO: make the font size more dynamic based on the image size, quote length, and font
                # may need to make multiple formulas depending on the context
                font_size = (img.width * img.height) ** 0.5 / (len(lines_list[0]) - 2)
                fonts = ["arial.ttf", "BOOKOSI.TTF", "Candaraz.ttf", "georgia.ttf", "times.ttf", "verdana.ttf", "consola.ttf"]
                if font_chosen is None:
                    font_chosen = random.choice(fonts)
                print("Using font: " + font_chosen)
                font = ImageFont.truetype(font_chosen, font_size)
            except IOError:
                font = ImageFont.load_default()
            y = 0.25 * img.height
            first_line = True
            if random.choice([True, False]): #shadow
                offset = 5
            else:
                offset = 1
            for line in lines_list:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                if first_line:
                    if (text_height + 20) * len(lines_list) > img.height * 0.6:
                        y = 0.1 * img.height
                    else:
                        y = 0.25 * img.height
                    first_line = False
                x = (img.width - text_width) / 2 

                # Add text with black outline for visibility
                draw.text((x-1, y-1), line, font=font, fill="black")
                draw.text((x+1, y-1), line, font=font, fill="black")
                draw.text((x-1, y+1), line, font=font, fill="black")
                draw.text((x+offset, y+offset), line, font=font, fill="black")
                draw.text((x, y), line, font=font, fill="white")
                y += text_height + 20 # the 20 adds a little more spacing
            
            # TODO: hash the image or image name to avoid duplicates
            output_path = os.path.join(output_folder + '/' + photo, photo) + str(random.randint(1, 10000)) + ".png"
            img.save(output_path)
            
            print("Added to " + output_path)

photos_folder = 'photos'
output_folder = 'output'

#import examples_quotes
#quotes = examples_quotes.quotes

#quotes = get_quotes_from_api()


photos_folders = [f for f in os.listdir(photos_folder) if os.path.isdir(os.path.join(photos_folder, f))]

quotes_source = info.QUOTES_DIR
quotes, author = get_quotes_from_files(quotes_source)

for _ in range(5):
    add_quote_to_images(quote=random.choice(quotes), author=author, photos_folder=photos_folder, output_folder=output_folder, photo=random.choice(photos_folders))

#[add_quote_to_images(quote=random.choice(api_quotes), photos_folder=photos_folder, output_folder=output_folder, photo=random.choice(photos_folders)) for _ in range(20)]