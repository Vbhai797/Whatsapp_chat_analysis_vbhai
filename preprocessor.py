import re
import pandas as pd
def preprocessor(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({
        "user_message": messages,
        "message_date": dates
    })
    df["message_date"] = (
        df["message_date"]
        .str.replace(" -", "", regex=False)
        .str.strip()
    )
    df["message_date"] = pd.to_datetime(
        df["message_date"],
        dayfirst=True
    )
    df.rename(columns={"message_date": "date"}, inplace=True)
    user = []
    messages = []
    for message in df["user_message"]:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            user.append(entry[1])
            messages.append(entry[2])
        else:
            user.append("group_notifications")
            messages.append(entry[0])
    df["user"] = user
    df["messages"] = messages
    df.drop(columns=["user_message"], inplace=True)
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month_name()
    df["month_num"] = df["date"].dt.month
    df["only_date"] = df["date"].dt.date
    df["day"] = df["date"].dt.day
    df["day_name"] = df["date"].dt.day_name()
    df["minute"] = df["date"].dt.minute
    return df


