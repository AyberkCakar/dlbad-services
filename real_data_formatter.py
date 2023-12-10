from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json


def get_normal_data(file):
    with open(file, 'r') as file:
        data = json.load(file)

    df_normal = pd.DataFrame(data)
    # df_10x = pd.concat([df_normal] * 10, ignore_index=True)
    return df_normal


def get_anomaly_data(file):
    with open(file, 'r') as file:
        anomaly_data = json.load(file)

    df_anomaly = pd.DataFrame(anomaly_data)
    df_anomaly['tag'] = 'Anomaly'
    # df_anomaly_10x = pd.concat([df_anomaly] * 10, ignore_index=True)
    return df_anomaly


def create_down_sampled_dataframe_from_mp3(mp3_file, target_length):
    audio = AudioSegment.from_mp3(mp3_file)
    samples = np.array(audio.get_array_of_samples())

    # sample_rate = audio.frame_rate
    # time = np.linspace(0, len(samples) / sample_rate, num=len(samples))

    df = pd.DataFrame({
        'sound': samples
    })

    return df.iloc[np.linspace(0, len(df) - 1, target_length).astype(int)]


def show_plt(output):
    plt.figure(figsize=(10, 6))

    # Vibration
    plt.subplot(3, 1, 1)
    plt.plot(output["time"], output["vibration"], marker='o', label='Vibration')
    plt.xlabel('Time')
    plt.ylabel('Vibration')
    plt.title('Time vs Vibration')
    plt.grid(True)

    # Sound
    plt.subplot(3, 1, 2)
    plt.plot(output["time"], output["sound"], marker='o', color='red', label='Sound')
    plt.xlabel('Time')
    plt.ylabel('Sound')
    plt.title('Time vs Sound')
    plt.grid(True)

    # Temperature
    plt.subplot(3, 1, 3)
    plt.plot(output["time"], output["temperature"], marker='o', color='green', label='Temperature')
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.title('Time vs Temperature')
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def save_json_file(output):
    with open('data.json', 'w') as file:
        json.dump(output, file)


def get_formatted_data(df_normal, df_anomaly):
    combined_df = pd.concat([df_normal, df_normal, df_normal, df_anomaly, df_normal, df_anomaly], ignore_index=True)
    json_str = combined_df.to_json(orient='records')

    data = json.loads(json_str)
    output = {"time": [], "vibration": [], "sound": [], "temperature": [], "tag": []}

    for record in data:
        output["time"].append(record.get("time"))
        output["vibration"].append(record.get("vibration"))
        output["sound"].append(record.get("sound"))
        output["temperature"].append(record.get("temperature"))
        output["tag"].append(record.get("tag"))

    return output


def get_data(normal_file, anomaly_file, normal_mp3, anomaly_mp3):
    df_normal = get_normal_data(normal_file)
    df_normal_down_sampled = create_down_sampled_dataframe_from_mp3(normal_mp3, len(df_normal))
    df_normal.reset_index(drop=True, inplace=True)
    df_normal_down_sampled.reset_index(drop=True, inplace=True)
    df_normal['sound'] = df_normal_down_sampled['sound']

    df_anomaly = get_anomaly_data(anomaly_file)
    df_anomaly_down_sampled = create_down_sampled_dataframe_from_mp3(anomaly_mp3, len(df_anomaly))
    df_anomaly.reset_index(drop=True, inplace=True)
    df_anomaly_down_sampled.reset_index(drop=True, inplace=True)
    df_anomaly['sound'] = df_anomaly_down_sampled['sound']

    output = get_formatted_data(df_normal, df_anomaly)
    show_plt(output)
    save_json_file(output)


normal_data_file = 'normal.json'
anomaly_data_file = 'anomali.json'
normal_data_mp3 = 'normal.mp3'
anomaly_data_mp3 = 'anomali.mp3'

get_data(normal_data_file, anomaly_data_file, normal_data_mp3, anomaly_data_mp3)
