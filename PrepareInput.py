
# Dependencies
import torch                        # Main ML framework
import torchaudio                   # Main audio processing framework
import matplotlib.pyplot as plt     # For displaying the graph
import librosa                      # For converting spectrogram
import librosa.display              # For displaying spectrogram
import numpy as np                  # For utilizing a numpy array
from pydub import AudioSegment      # Audio format conversion
import os.path                      # For managing directory files


class PrepareAudio:
    """The PrepareAudio class processes audio inputs for the purpose of
    generating a mel spectrograph that will ultimately serve as the
    input for a machine learning model."""

    def __init__(self) -> None:
        """Constructor method for PrepareAudio class.
        No values except self.n_mels needs to be tweaked."""

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
            return

        # 2. Convert audio file to .wav and save to /Inputs directory (Does so
        # ...for ALL file types, even .wav for the purpose of uniformity)
        path = self.convert_to_wav(path)

        # 3. Get signal and sample rate of choosen audio file
        waveform, sr = torchaudio.load(path)
        # self.plot_graph(signal, sr, 'Waveform')             # Optional
        # self.plot_graph(signal, sr, 'Vanilla Spectrogram')  # Optional

        # 4. Resample audio signal to match desired sample rate
        # ...if it doesnt already match
        if sr != self.sr:
            waveform = self.resample_signal(waveform, sr)

        # 5. Perform mel transformation on signal
        mel_spectrogram = self.transformer(waveform)
        # self.plot_melspectrogram(mel_spectrogram[0])  # Optional

        # 6. Save image to directory (This img will be the
        # ...output of this program and input of ML model)
        self.generate_melspec_png(mel_spectrogram[0])

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
        path = f'Inputs/{self.file_name}.wav'

        # Convert to .wav and save to directory
        AudioSegment.from_file(path).export(
            path, format='wav')

        # Return path to converted audio file
        return path

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
                axes[c].plot(time_axis, signal[c], linewidth=1)
                axes[c].grid(True)
            else:
                axes[c].specgram(signal[c], Fs=sr)
            if num_channels > 1:
                axes[c].set_ylabel(f'Channel {c+1}')
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
        melspec_db = librosa.power_to_db(melspec, ref=np.max)

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
        melspec_db = librosa.power_to_db(melspec, ref=np.max)
        librosa.display.specshow(
            melspec_db, sr=self.sr, hop_length=self.hop_length)
        plt.tight_layout()

        # Create Outputs/ directory if it doesnt already exist
        if not os.path.exists('Outputs'):
            os.makedirs('Outputs')

        # Save mel spectrogram as .png to said directory
        plt.savefig(f"Outputs/{self.file_name}_ms.png")


if __name__ == "__main__":
    # Instructions: Specify a valid path to desired audio file
    # for the 'file' variable and the class with take care of the rest!

    audio_prepper = PrepareAudio()
    file = "INSERT PATH TO AUDIO FILE HERE"
    audio_prepper.start(file)
