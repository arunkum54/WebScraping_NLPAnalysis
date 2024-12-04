# WebScraping_NLPAnalysis

This project demonstrates the use of web scraping techniques to extract article content from websites and perform text analysis using Python. The extracted data is processed and analyzed to compute various textual metrics, such as sentiment scores, readability indices, and more.

#Project Overview:

Web Scraping: Extracts article titles and texts from URLs provided in an input file (Input.xlsx), using Python libraries such as BeautifulSoup and Selenium.
Text Analysis: Computes textual analysis variables like Polarity Score, Subjectivity Score, Fog Index, Average Sentence Length, and more.

#Technologies Used:

Python 3.x
BeautifulSoup (for scraping)
Selenium (for scraping dynamic content)
NLTK / TextBlob / spaCy (for text analysis)
Pandas (for data handling)

#Project Structure: 

scraper.py: Python script that performs the web scraping.
analysis.py: Python script for text analysis.
Input.xlsx: Input file containing the list of URLs for scraping.
Output_Data.xlsx: Output file with computed variables from the text analysis.
Text_Analysis.docx: Document defining the variables to compute.
README.md: Project documentation.

#Variables Computed:

Positive Score
Negative Score
Polarity Score
Subjectivity Score
Average Sentence Length
Percentage of Complex Words
Fog Index
Average Words per Sentence
Complex Word Count
Word Count
Syllables per Word
Personal Pronouns
Average Word Length
