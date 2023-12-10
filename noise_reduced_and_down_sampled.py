from pydub import AudioSegment
import pandas as pd
import numpy as np
import noisereduce as nr


def create_noise_reduced_and_down_sampled_from_mp3(mp3_file, target_length):
    audio = AudioSegment.from_mp3(mp3_file)
    samples = np.array(audio.get_array_of_samples())

    sample_rate = audio.frame_rate
    reduced_noise_samples = nr.reduce_noise(y=samples, sr=sample_rate)
    time = np.linspace(0, len(reduced_noise_samples) / sample_rate, num=len(reduced_noise_samples))

    df = pd.DataFrame({
        'Time': time,
        'Amplitude': reduced_noise_samples
    })

    return df.iloc[np.linspace(0, len(df) - 1, target_length).astype(int)]
