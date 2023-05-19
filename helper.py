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

    most_busy_users_df = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'users': 'percent'})  # using reset_index() function we can convert it into a dataframe after that we can rename columns name

    return x,most_busy_users_df

def create_wordcloud(selected_user,df):

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
        temp = df[df['users'] != 'group notification']  # dataframe except 'group notification' users
        temp = temp[temp['messages'] != '<Media omitted>\n']  # dataframe except 'group notification'users and '<Media Omitted>\n' messages

        f = open('stop words hinglish.txt', 'r')
        stop_words = f.read()

        words = []
        for message in temp['messages']:
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)

        most_common_words_df = pd.DataFrame(Counter(words).most_common(20))#here Counter used for get the frequency of the words which are in the 'words' list and we convert  'words' list into a dataframe where index column contain the words and value column has the frequency of the words.

        return most_common_words_df

    else:
        new_df = df[df['users'] == selected_user]
        temp = new_df[df['users'] != 'group notification']  # dataframe except 'group notification' users
        temp = temp[temp['messages'] != '<Media omitted>\n']  # dataframe(temp) except 'group notification'users and '<Media Omitted>\n' messages

        f = open('stop words hinglish.txt', 'r')
        stop_words = f.read()

        words = []
        for message in temp['messages']:
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)

        most_common_words_df = pd.DataFrame(Counter(words).most_common(20))

        return most_common_words_df

def emoji_helper(selected_user,df):
    if selected_user == 'Overall':
        #df = df[df['users'] == selected_user]

        emojis = []
        for message in df['messages']:
            emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

        emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

        return emoji_df
    else:
        new_df = df[df['users'] == selected_user]
        emojis = []
        for message in new_df['messages']:
            emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

        emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

        return emoji_df

def montly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()  # adding reset index will give u a dataframe
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    #here we are connecting only two column of a dataframe
    message_df = timeline['messages']
    time_df = timeline['time']
    frames=[time_df,message_df]
    result=pd.concat(frames,axis=1)#horizontal concat

    return result

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap