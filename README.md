# RedditKeywords
Program that can find the most used words in a chosen subreddit

## Installation
Step 1:

    pip install -r requirements.txt
    
Step 2:

Enter Client ID and Secret in ```config/creds.ini``` ([Help](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps))
## Usage
 *Follow on screen prompts*
 
    Keyword Trends
    ******************************
    Choose an option:
    1) Search for all words
    2) Search for specified words only
    
    Hint: You can specify your own words in custom_words.txt
    >> 

#### Custom Keywords
You also are able to specify keywords to look for by adding them to ```config/custom_words.txt```

    Keyword Trends
    ******************************
    Choose an option:
    1) Search for all words
    2) Search for specified words only
    
    >> 1
    Would you like to exclude common words? (Yes/No) 

#### Common Keywords
You also have the ability to ignore common English words. 

(Located at ```config/common_words.txt```)