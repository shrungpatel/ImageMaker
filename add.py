import os
from PIL import Image, ImageDraw, ImageFont
import random

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
    
def add_quote_to_images(quote: str, photos_folder, output_folder, photo, font_chosen=None):
    """Add quotes to images in the specified folder."""
    os.makedirs(output_folder + '/' + photo, exist_ok=True)
    for filename in os.listdir(photos_folder + '/' + photo):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # does the quote need to be split?
            if len(quote) >= 30:
                lines_list = split_quotes(quote) 
            else:
                lines_list = [quote]               
            img_path = os.path.join(photos_folder + '/' + photo, filename)
            img = Image.open(img_path).convert("L")
            draw = ImageDraw.Draw(img)
            try:
                font_size = img.width / (len(lines_list[0]) - 2)
                fonts = ["arial.ttf", "BOOKOSI.TTF", "Candaraz.ttf", "georgia.ttf", "times.ttf", "verdana.ttf", "consola.ttf"]
                if font_chosen is None:
                    font_chosen = random.choice(fonts)
                print("Using font: " + font_chosen)
                font = ImageFont.truetype(font_chosen, font_size)
            except IOError:
                font = ImageFont.load_default()
            y = 0.25 * img.height
            first_line = True
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

                if random.choice([True, False]): #shadow
                    offset = 5
                else:
                    offset = 1

                # Add text with black outline for visibility
                draw.text((x-1, y-1), line, font=font, fill="black")
                draw.text((x+1, y-1), line, font=font, fill="black")
                draw.text((x-1, y+1), line, font=font, fill="black")
                draw.text((x+offset, y+offset), line, font=font, fill="black")
                draw.text((x, y), line, font=font, fill="white")
                y += text_height + 20 # the 20 adds a little more spacing
            
            output_path = os.path.join(output_folder + '/' + photo, photo) + str(random.randint(1, 10000)) + ".png"
            img.save(output_path)
            
            print("Added to " + output_path)

photos_folder = 'photos'
output_folder = 'output'
quotes = [
    "Mistakes are proof that you are trying.",
    "A mistake will never become an error until you refuse to correct it.",
    "Believe in yourself.",
    "The best is yet to come.",
    "Dream big, work hard.",
    "Stay positive, work hard, make it happen.",
    "Success is not final, failure is not fatal.", 
    "Courage is what counts.", 
    "You are capable of amazing things.",
    "You are stronger than you think.",
    "Every day is a second chance.",
    "Your limitation—it's only your imagination.",
    "Push yourself, because no one else is going to do it for you.",
    "Great things never come from comfort zones.",
    "Dream it. Wish it. Do it.",
    "Success doesn't just find you. You have to go out and get it.",
    "The harder you work for something, the greater you'll feel when you achieve it.",
    "Dream bigger. Do bigger.",
    "Don't stop when you're tired. Stop when you're done.",
    "Wake up with determination. Go to bed with satisfaction.",
    "Do something today that your future self will thank you for.",
    "Little things make big days.",
    "It's going to be hard, but hard does not mean impossible.",
    "The eagle does not escape the storm, it uses the storm to soar higher.",
    "Purity is not in the face; beauty is a light in the heart.",
    "I am not afraid of storms, for I am learning how to sail my ship.",
    "The only way to do great work is to love what you do.",
    "Success usually comes to those who are too busy to be looking for it.",
    "Don't watch the clock; do what it does. Keep going.",
    "You only live once, but if you do it right, once is enough.",
    "Life is what happens when you're busy making other plans.",
    "Get busy living or get busy dying.",
    "You have within you right now, everything you need to deal with whatever the world can throw at you",
    "Believe you can and you're halfway there.",
    "Act as if what you do makes a difference. It does.",
    "Success is not how high you have climbed, but how you make a positive difference to the world.",
    "You are never too old to set another goal or to dream a new dream.",
    "The future belongs to those who believe in the beauty of their dreams.",
    "It does not matter how slowly you go as long as you do not stop.",
    "Everything you can imagine is real.",
    "What lies behind us and what lies before us are tiny matters compared to what lies within us.",
    "Keep your face always toward the sunshine—and shadows will fall behind you.",
    "The only limit to our realization of tomorrow will be our doubts of today.",
    "The only way to achieve the impossible is to believe it is possible.",
    "You are braver than you believe, stronger than you seem, and smarter than you think.",
    "The only person you are destined to become is the person you decide to be.",
    "Your time is limited, so don't waste it living someone else's life.",
    "Don't be trapped by dogma – which is living with the results of other people's thinking.",
    "Life is either a daring adventure or nothing at all.",
    "To live is the rarest thing in the world. Most people exist, that is all.",
    "The purpose of our lives is to be happy.",
    "Get busy living or get busy dying.",
    "You only live once, but if you do it right, once is enough.",
    "In the end, we only regret the chances we didn't take.",
    "Life is what happens when you're busy making other plans.",   
    "The best way to predict the future is to create it.",
    "You miss 100% of the shots you don't take.",
    "Success is not the key to happiness. Happiness is the key to success.",
    "If you love what you are doing, you will be successful.",
    "Success is not in what you have, but who you are.",
    "Success is not about how much money you make, but the difference you make in people's lives.",
    "Success is not about being the best. It's about always getting better.",
    "Success is not about what you accomplish in your life, but what you inspire others to do.",
    "Success is not about what you have, but what you give.",
    "Success is not about what you achieve, but what you overcome.",
    "Success is not about what you do, but how you do it.",
    "Success is not about what you get, but what you become.",
    "If you want to give up, remember why you started.",
    "Always stay humble and kind.",
    "Tell yourself you can and you will.",
    "You are capable of more than you know.",
    "You are stronger than you think.",
    "You are braver than you believe.",
    "You are smarter than you think.",
    "You are more powerful than you know.",
    "You are more resilient than you realize.",
    "Coding is like magic, it can create something out of nothing.",
    "Coding is not just about writing code, it's about solving problems.",
    "Success in coding is not about how much you know, but how much you are willing to learn.",
    "The best way to learn something new is to teach it to someone else.",
    "Always be curious, always be learning.",
    "Make it a mission to do something great today.",
    "Make sure to keep a smile on your face today.",
    "Make sure to keep a positive attitude today.",
    "Make sure to keep a grateful heart today.",
    "Ligten up someone's day with a smile.",
    "A smile is the best makeup anyone can wear.",
    "A smile is the universal language of kindness.",
    "Don't cheat yourself out of something great by being distracted.",
    "Don't let the noise of others' opinions drown out your own inner voice.",
    "Roar like a lion, but be gentle like a lamb.",
    "Be fierce like a lion, but kind like a lamb.",
    "Be strong like a lion, but gentle like a lamb.",
    "Be brave like a lion, but compassionate like a lamb.",
    "Walk like a tiger, run like a cheetah, and soar like an eagle.",
    "A coward dies a thousand times, but a brave only dies but once.",
    "A cow does not know the use of its horns until it is attacked.",
    "A buffalo is not joined to the herd by its horns, but by its heart.",
    "It is not the size of the dog in the fight, but the size of the fight in the dog.",
    "I will not be scared of the dark, for the dark is where the stars shine brightest.",
    "Let it be said of me that I lived life to the fullest and gave everything I had.",
    "Not trying is the only sure way to fail.",
    "Do not go where the path may lead, go instead where there is no path and leave a trail.",
    "Follow what your heart knows to be right.",
    "In a world where you can be anything, be kind.",
    "Kindness is a language which the deaf can hear and the blind can see.",
    "No act of kindness, no matter how small, is ever wasted.",
    "Kindness is the sunshine in which virtue grows.",
    "Carry out a random act of kindness, with no expectation of reward, safe in the knowledge that one day someone might do the same for you.",
    "Set your mind on a definite goal and observe how quickly the world stands aside to let you pass.",
    "The only limit to our realization of tomorrow will be our doubts of today.",
    "The best way to predict the future is to create it."
]

photos_folders = [f for f in os.listdir(photos_folder) if os.path.isdir(os.path.join(photos_folder, f))]
print("Found animal folders: " + str(photos_folders))

[add_quote_to_images(quote=random.choice(quotes), photos_folder=photos_folder, output_folder=output_folder, photo=random.choice(photos_folders)) for _ in range(15)]