# Homework to implement an agent that can perform three core functions:
# 	1. Fetch Web Page – The agent should be able to fetch the content of a web page given its URL.
# 	2. Save Summary – The agent should be able to save a summary of the page it processed.
#   3. Search – The agent should be able to perform a search for relevant or related information
import fetch
import summary


#define variables

webpage = 'https://datatalks.club'

def main():
    page_content = fetch.get_page_content(webpage)
    summary.summarize(page_content)
# 
if __name__ == "__main__":
    main()