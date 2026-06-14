import os

def get_quotes_from_files(quotes_source):
    quotes = []
    for filename in os.listdir(quotes_source):
        try:
            if filename.lower().endswith('.txt'):
                with open(os.path.join(quotes_source, filename), 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        quotes.append(line.strip())
        except Exception as e:
            print("Error reading file: " + filename + " - " + str(e))
    return quotes