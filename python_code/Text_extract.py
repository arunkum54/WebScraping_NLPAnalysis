import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

# input data load
df = pd.read_excel('Input.xlsx')

# Creating directory for saving extracted texts
if not os.path.exists('Extracted_Texts'):
    os.makedirs('Extracted_Texts')

def extract_article_text(url, retries=5):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for request errors
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the title from the <title> tag
            title_tag = soup.find('title')
            title = title_tag.get_text(strip=True) if title_tag else 'No Title Found'

            # Extract the article text by looking for specific tags and classes
            article_text = ""
            possible_containers = ['article', 'div', 'main', 'section']

            for tag in possible_containers:
                # Look for tags with commonly used classes for article content
                content = soup.find(tag, {'class': lambda x: x and ('content' in x or 'article' in x or 'post' in x)})
                if content:
                    article_text = content.get_text(strip=True)
                    break

            # Fallback: If no specific content is found, attempt to extract from the <body>
            if not article_text:
                body_tag = soup.find('body')
                if body_tag:
                    article_text = body_tag.get_text(strip=True)

            # Combine title and extracted content
            extracted_text = f"{title}\n\n{article_text}"
            return extracted_text.strip()

        except requests.RequestException as e:
            print(f"Request error extracting from {url} (attempt {attempt + 1}): {e}")
            attempt += 1
            time.sleep(2)  # Wait before retrying
        except Exception as e:
            print(f"Error extracting from {url} (attempt {attempt + 1}): {e}")
            attempt += 1
            time.sleep(2)  # Wait before retrying

    # If all retries fail, return None
    return None

# Looped through URLs to extract and save text
for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    
    article_text = extract_article_text(url)
    
    if article_text:
        file_path = f'Extracted_Texts/{url_id}.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(article_text)
