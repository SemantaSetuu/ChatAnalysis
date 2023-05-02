from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_user,df):

    #Total

    if selected_user == 'Overall':
        # 1. fetch number of messages
        num_messages = df.shape[0]

        # 2. fetch number of words
        words = []
        for message in df['messages']:
            words.extend(message.split())

        #fetch number of total media shared
        num_media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]

        #fetch number of link
        links = []
        for message in df ['messages']:
            links.extend(extract.find_urls(message))

        return num_messages, len(words), num_media_messages,len(links)

    # selected user
    else:
        new_df = df[df['users'] == selected_user]
        # 1. fetch number of messages for selected user
        num_messages = new_df.shape[0]

        # 2. fetch number of words for selected user
        words = []
        for message in new_df['messages']:
            words.extend(message.split())

        #fetch number of media shared for selected user
        num_media_messages=new_df[df['messages'] == '<Media omitted>\n'].shape[0]

        # fetch number of link for selected user
        links = []
        for message in new_df['messages']:
            links.extend(extract.find_urls(message))

        return num_messages, len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['users'].value_counts().head()

    df = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'users': 'percent'})

    return x,df

def create_wordcloud(selected_user,df):

#if it is 'Overall' then df will remain as same as before . that is why we did not write code for this
#if not then df will get change,


    #if selected_user != 'Overall':
     #   df = df[df['users'] == selected_user]
      #  wc =WordCloud(width=500,height=500,min_font_size=10,background_color='white')
       # df_wc = wc.generate(df['messages'].str.cat(sep=" "))#generate() function basically generate a image of words. it is taking words from the column of 'messages' of df

        #return df_wc


    if selected_user == 'Overall':

        f = open('stop words hinglish.txt', 'r')
        stop_words = f.read()

        temp = df[df['users'] != 'group notification']  # users except 'group notification'
        tempp = temp[temp['messages'] != '<Media omitted>\n']  # users and messages except 'group notification' and '<Media Omitted>\n'

        def remove_stop_words(message):
            words_except_stopWords=[]
            for word in message.lower().split():
                if word not in stop_words:
                    words_except_stopWords.append(word)
            return " ".join(words_except_stopWords)

        wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
        tempp['messages'] = tempp['messages'].apply(remove_stop_words)
        df_wc = wc.generate(tempp['messages'].str.cat(sep=" "))
        return df_wc

    else:
        new_df = df[df['users'] == selected_user]

        f = open('stop words hinglish.txt', 'r')
        stop_words = f.read()

        temp = new_df[new_df['users'] != 'group notification']  # users except 'group notification'
        tempp = temp[temp['messages'] != '<Media omitted>\n']  # df of messages except users' 'group notification' and '<Media Omitted>\n'

        def remove_stop_words(message):
            words_except_stopWords = []
            for word in message.lower().split():
                if word not in stop_words:
                    words_except_stopWords.append(word)
            return " ".join(words_except_stopWords)

        tempp['messages'] = tempp['messages'].apply(remove_stop_words)# here we got a dataframe which is based on without group notification, media omitted and stop words
        wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
        df_wc = wc.generate(tempp['messages'].str.cat(sep=" "))#here we could not use tempp. will try later
        return df_wc

def most_common_words(selected_user,df):
    if selected_user == 'Overall':
        temp = df[df['users'] != 'group notification']  # users except 'group notification'
        temp = temp[temp['messages'] != '<Media omitted>\n']  # users and messages except 'group notification' and '<Media Omitted>\n'

        f = open('stop words hinglish.txt', 'r')
        stop_words = f.read()

        words = []
        for message in temp['messages']:
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)

        most_common_df = pd.DataFrame(Counter(words).most_common(20))#here we convert  words into a dataframe

        return most_common_df

    else:
        new_df = df[df['users'] == selected_user]
        temp = new_df[df['users'] != 'group notification']  # users except 'group notification'
        temp = temp[temp['messages'] != '<Media omitted>\n']  # users and messages except 'group notification' and '<Media Omitted>\n'

        f = open('stop words hinglish.txt', 'r')
        stop_words = f.read()

        words = []
        for message in temp['messages']:
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)

        most_common_df = pd.DataFrame(Counter(words).most_common(20))

        return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df