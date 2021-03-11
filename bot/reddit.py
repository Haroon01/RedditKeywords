import praw
import configparser
import re

class Reddit:
    # ---- File Paths -----
    CREDENTIALS_PATH = "./config/creds.ini"
    COMMON_WORDS_PATH = "./config/common_words.txt"
    CUSTOM_WORDS_PATH = "./config/custom_words.txt"

    def __init__(self):
        credentials = configparser.ConfigParser()
        credentials.read(self.CREDENTIALS_PATH)
        common_words_file = open(self.COMMON_WORDS_PATH, "r")
        custom_words_file = open(self.CUSTOM_WORDS_PATH, "r")

        self.reddit = praw.Reddit(client_id=credentials.get("ACCOUNT", "CLIENT_ID"),
                             client_secret=credentials.get("ACCOUNT", "CLIENT_SECRET"),
                             user_agent="Keyword Trends")
        self.name = self.reddit.user.me()
        self.count = {}
        self.common_words = common_words_file.read().splitlines()
        self.custom_words = custom_words_file.read().splitlines()


    def scan(self, subreddit, amount, common, custom):
        for comment in self.reddit.subreddit(subreddit).comments(limit = amount):
            if comment is None:
                break
            self.count_words(comment.body.lower(), common, custom)


        # sort keywords dictionary in ascending order
        keywords = dict(sorted(self.count.items(), key=lambda item: item[1], reverse = True))

        # print out final result to console
        for key, value in keywords.items():
            print(key, value)


    def count_words(self, body, common, custom):

        #--------------------------------Clean comment body----------------------------------------------
        remove_markup = re.sub(r"\[(.+)\]\(.+\)", r"\1", body) # remove any markup links from text
        remove_raw_links = re.sub(r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))", r"", remove_markup) # remove any raw links from text
        stripped_body = re.sub("[^a-zA-Z\s]", "", remove_raw_links) # remove any formatting characters from text
        #------------------------------------------------------------------------------------------------

        words = stripped_body.split()
        for word in words:
            if len(word) > 1:
                if common and word in self.common_words: # if user wants to exclude common words (stored in ./config/common_words.txt)
                    break
                if custom and word not in self.custom_words: # if user wants to search for specified words only
                    break
                if word not in self.count:
                    self.count[word] = 0
                self.count[word] += 1
        return self.count



