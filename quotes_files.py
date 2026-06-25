import os

def get_quotes_from_files(quotes_source):
    quotes = []
    for filename in os.listdir(quotes_source):
        try:
            if filename.lower().endswith('.txt'):
                with open(os.path.join(quotes_source, filename), 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    author = lines[0].strip()
                    for line in lines[1:]:
                        quotes.append(line.strip() + ' - ' + author)
        except Exception as e:
            print("Error reading file: " + filename + " - " + str(e))
    return quotes