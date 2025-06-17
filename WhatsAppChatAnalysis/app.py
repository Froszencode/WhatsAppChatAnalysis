import matplotlib.pyplot as plt
import streamlit as st
import helper
import preprocessor
import sys
import seaborn as sns


st.sidebar.title("Whatsapp chat analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf8")
    df = preprocessor.preprocess(data)


    #fetch unique user
    user_list = df['user'].unique().tolist()
    rmv_grp_name = user_list[0]
    user_list.remove(rmv_grp_name)
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis with respect to ",user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_messages,num_links = helper.fetch_stats(selected_user,df)
        st.title('Top Statistics')

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)


        #monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #week activity map
        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header('Most busy day')
            busy_day = helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most busy month')
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar( busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # weekly activity heat map
        st.title("Weekly activity map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)





        #most busy user group level
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = helper.fetch_busy_user(df)
            fig,ax = plt.subplots()

            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color = 'red')
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        #WordCloud
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        df_common_words = helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(df_common_words['words'],df_common_words['count'])
        plt.xticks(rotation="vertical")
        st.title("Most Common Words")
        st.pyplot(fig)


        #most commonly used emojis
        emojis_df = helper.most_common_emojis(selected_user,df)
        st.title("Emoji analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emojis_df)
        with col2:
            fig,ax = plt.subplots()

            if sys.platform == "linux":
                emoji_font_path = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"  # Linux
            elif sys.platform == "win32":
                emoji_font_path = "C:/Windows/Fonts/seguiemj.ttf"  # Windows
            else:
                emoji_font_path = None  # Default fallback

            if emoji_font_path:
                prop = fm.FontProperties(fname=emoji_font_path)
                ax.pie(emojis_df['count'].head(), labels=emojis_df['emoji'].head(), textprops={'fontproperties': prop},autopct="%0.2f")
            else:
                ax.pie(emojis_df['count'].head(), labels=emojis_df['emoji'].head())

            st.pyplot(fig)





