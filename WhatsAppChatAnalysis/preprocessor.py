import re
import pandas as pd

def preprocess(data):

    pattern = r"\[(\d{2}/\d{2}/\d{2}), (\d{1,2}:\d{2}:\d{2}\s*[AP]M)\] ?~?\s?([^:]+):\s(.*)"

    messages = re.findall(pattern, data)

    df = pd.DataFrame(messages, columns=["Date", "Time", "user", "message"])

    df["date"] = pd.to_datetime(df["Date"] + " " + df["Time"], format="%d/%m/%y %I:%M:%S %p")
    df.drop(columns=["Date", "Time"], inplace=True)
    df['year'] = df['date'].dt.year
    df['only_date'] = df['date'].dt.date
    df['month_num'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['period'] = period
    return df

