""" This module prepares the audio file for further processing. """

import os.path                      # For managing directory files
import torch                        # Main ML framework
import torchaudio                   # Main audio processing framework
import matplotlib.pyplot as plt     # For displaying the graph
import librosa                      # For audio processing
import librosa.display              # For displaying spectrogram
import numpy as np                  # For utilizing a numpy array
from pydub import AudioSegment      # Audio format conversion


class PrepareAudio:
    """The PrepareAudio class processes audio inputs for the purpose of
    generating a mel spectrograph that will ultimately serve as the
    input for a machine learning model."""

    def __init__(self):
        """Constructor method for PrepareAudio class.
        No values except self.n_mels needs to be tweaked."""

        # List of accepted file types (Feel free to add to this as you please)
        self.accepted_file_types = ['.mp3', '.mp4', '.au', '.wav']

        # For the purpose of naming the output file. Updated after start().
        self.file_name = None

        # Sample rate (Samples per second). Default = 44.1kHz aka 441000hz
        self.sr = 44100

        # Size of Fast Fourier Transform (FFT). Also used for window length
        self.n_fft = 2048

        # Step or stride between windows. The amount we are transforming
        # ...each fft to the right. Should be < than n_fft
        self.hop_length = 512

        # Number of mel bands (Your mel spectrogram willvary depending on
        # ...what value you specify here. Use power of 2: 32, 64 or 128)
        self.n_mels = 64

        # Transformer object used for wavefrom signal -> mel spectrogram
        self.transformer = torchaudio.transforms.MelSpectrogram(
            sample_rate=self.sr,
            n_fft=self.n_fft,
            hop_length=self.hop_length,
            n_mels=self.n_mels
        )

    def check_file_exists(self, path):
        """Checks if the specified file exists.
        Args: Path = path to audio file.
        Return: True if file exists, False otherwise.
        """

        if os.path.exists(path):
            return True
        else:
            return False

    def check_file_type(self, path):
        """Check if the file type is accetable.
        Args: Path = path to audio file.
        Return: True if file is accepted, False otherwise.
        """
        file_ext = os.path.splitext(path)[1]
        if file_ext in self.accepted_file_types:
            return True
        else:
            return False

    def start(self, path):
        """Main driver function for the PrepareAudio class.
        *No other methods need to be directly called.
        Args: Path = path to audio file.
        Return: None
        """

        # 1. Check if file exists. If it does not exist,
        # ...print message and exit return
        if not os.path.exists(path):
            print("The specified file does not exist. Please try again.")
            return False

        # 2. Check if the file is accepted
        file_ext = os.path.splitext(path)[1]  # Extract file extension
        if file_ext not in self.accepted_file_types:
            print("The specified file is not accepted. Please try again.")
            return False

        # 3. Convert audio file to .wav and save to /Inputs directory (Does so
        # ...for ALL file types, even .wav for the purpose of uniformity)
        path = self.convert_to_wav(path)

        # 4. Get signal and sample rate of choosen audio file
        waveform, sr = torchaudio.load(path)  # type: ignore

        # self.plot_graph(signal, sr, 'Waveform')             # Optional
        # self.plot_graph(signal, sr, 'Vanilla Spectrogram')  # Optional

        # 5. Resample audio signal to match desired sample rate
        # ...if it doesnt already match
        if sr != self.sr:
            waveform = self.resample_signal(waveform, sr)

        # 6. Perform mel transformation on signal
        mel_spectrogram = self.transformer(waveform)
        # self.plot_melspectrogram(mel_spectrogram[0])  # Optional

        # 7. Save image to directory (This img will be the
        # ...output of this program and input of ML model)
        self.generate_melspec_png(mel_spectrogram[0])
        return True

    def convert_to_wav(self, path):
        """Converts the input audio file to .wav format and places
        in directory: Inputs/*.wav. Note, the file name is unchanged
        and only the format is converted.
        Args: Path = path to audio file.
        Return: Path to converted file
        """

        # Extract name of file from path variable
        path_parts = os.path.split(path)
        file_name_with_ext = path_parts[len(path_parts)-1]
        idx = len(file_name_with_ext) - file_name_with_ext.index('.')
        self.file_name = file_name_with_ext[:len(file_name_with_ext)-idx]
        path_to_wav = f'Inputs/{self.file_name}.wav'

        # Create an Inputs/ folder if it doesnt already exist
        if not os.path.exists('Inputs'):
            os.mkdir('Inputs')  # type: ignore

        # Convert input file to .wav and save to Inputs/ directory
        AudioSegment.from_file(path).export(
            path_to_wav, format='wav')

        # Return path to converted audio file
        return path_to_wav

    def resample_signal(self, signal, sr):
        """Resamples the passed audio signal to a desired sample rate
        before returning to caller.
        Args: signal = waveform signal, sr = sample rate of signal.
        Return: signal with new sample rate.
        """

        sr_modifier = torchaudio.transforms.Resample(sr, self.sr)
        new_signal = sr_modifier(signal)
        return new_signal

    def plot_graph(self, signal, sr, title):
        """Displays the graph that you pass in (raw waveform or vanilla
        spectrogram). This function is only for visualization purposes
        and is not vital for processsing the audio file.
        Args: signal = waveform signal, sr = sample rate of signal.
        Return: None
        """

        signal = signal.numpy()

        num_channels, num_frames = signal.shape
        time_axis = torch.arange(0, num_frames) / sr

        figure, axes = plt.subplots(num_channels, 1)
        if num_channels == 1:
            axes = [axes]
        for c in range(num_channels):
            if title == "Waveform":
                axes[c].plot(time_axis, signal[c], linewidth=1)  # type: ignore
                axes[c].grid(True)  # type: ignore
            else:
                axes[c].specgram(signal[c], Fs=sr)  # type: ignore
            if num_channels > 1:
                axes[c].set_ylabel(f'Channel {c+1}')  # type: ignore
        figure.suptitle(title)
        plt.show(block=True)

    def plot_melspectrogram(self, melspec):
        """Displays the mel spectrogram. This function is only for
        visualization purposes and is not vital for processsing the
        audio file.
        Args: melspec = mel spectrogram signal.
        Return: None
        """

        # Convert the power value to a decibel value
        melspec_db = librosa.power_to_db(melspec, ref=np.max)  # type: ignore

        librosa.display.specshow(
            melspec_db, sr=self.sr, hop_length=self.hop_length)

        plt.title("Mel spectrogram")
        plt.colorbar(format="%+2.0f dB")
        plt.tight_layout()
        plt.show()

    def generate_melspec_png(self, melspec):
        """Saves the mel spectrogram as a .png to directory: Outputs/*_ms.png.
        Note, the output file name is identical to the input file name 
        except with a '_ms" appended to the end.
        Args: melspec = mel spectrogram signal.
        Return: None
        """

        # Convert the power value to a decibel value
        melspec_db = librosa.power_to_db(melspec, ref=np.max)  # type: ignore
        librosa.display.specshow(
            melspec_db, sr=self.sr, hop_length=self.hop_length)
        plt.tight_layout()

        # Create Outputs/ directory if it doesnt already exist
        if not os.path.exists('Outputs'):
            os.makedirs('Outputs')  # type: ignore

        # Save mel spectrogram as .png to said directory
        plt.savefig(f"Outputs/{self.file_name}_ms.png")


if __name__ == "__main__":
    # Instructions: Specify a valid path to desired audio file
    # for the 'file' variable and the class with take care of the rest!

    audio_prepper = PrepareAudio()
    file = 'PATH_TO_AUDIO_FILE'
    audio_prepper.start(file)
