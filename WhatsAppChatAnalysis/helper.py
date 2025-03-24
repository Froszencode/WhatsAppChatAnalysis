from numpy.lib.function_base import extract
from urlextract import URLExtract
from wordcloud import wordcloud, WordCloud
from collections import Counter
import pandas as pd
import emoji



extract = URLExtract()

# Read stop words from file
with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
    stop_words = set(f.read().splitlines())


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    # Count words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Count media messages using regex (covers all media types like image, sticker, document, etc.)
    media_pattern = r'(\u200e?<Media omitted>|\u200e?\b(image|sticker|GIF|document|video) omitted\b)'
    num_media_messages = df['message'].str.contains(media_pattern, regex=True).sum()

    links = []

    for messages in df['message']:
        links.extend(extract.find_urls(messages))

    return num_messages, len(words), num_media_messages, len(links)


def fetch_busy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter media and empty messages
    filtered_df = df[
        ~df['message'].str.contains(
            r'(\u200e?<Media omitted>|\u200e?\b(image|sticker|GIF|document|video) omitted\b)', regex=True)
    ]
    filtered_df = filtered_df[
        ~filtered_df['message'].str.contains(r'^\s*[\u200e\u200f]*\s*$', regex=True)
    ]

    # Generate WordCloud with custom stop words
    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white',
        stopwords=stop_words  # Add stop_words here
    )
    df_wc = wc.generate(filtered_df['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    filtered_df = df[~df['message'].str.contains(
        r'(?:\u200e?<Media omitted>|\u200e?\b(?:image|sticker|GIF|document|video) omitted\b)',
        regex=True
    )]
    filtered_df = filtered_df[~filtered_df['message'].str.contains(r'^\s*[\u200e\u200f]*\s*$', regex=True)]

    with open("D:\WhatsAppChatAnalysis\stop_hinglish.txt", 'r') as rf:
        stop_words = rf.read()

    words = []
    for i in filtered_df['message']:
        for message in i.lower().split():
            if message not in stop_words:
                words.append(message)

    common_words_df = pd.DataFrame(Counter(words).most_common(20))
    common_words_df.rename(columns={0: 'words', 1: 'count'},inplace=True)
    return common_words_df


def most_common_emojis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    # Handle case when no emojis are found
    if not emojis:
        return pd.DataFrame({'emoji': [], 'count': []})

    emoji_counts = Counter(emojis).most_common()
    common_emoji_df = pd.DataFrame(emoji_counts, columns=['emoji', 'count'])

    # Ensure count column is integer and drop any NaN values
    common_emoji_df['count'] = common_emoji_df['count'].fillna(0).astype(int)

    return common_emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby(['only_date']).count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return user_heatmap






