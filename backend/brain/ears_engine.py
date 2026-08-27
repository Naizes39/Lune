import sounddevice as sd
from faster_whisper import WhisperModel


model_size: str = "large-v3"
model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")


def record(duration: float = 5.0, fs: int = 16000):
    print("Recording started...")
    my_recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  
    print("Recording finished.")
    segments, info = model.transcribe(my_recording, beam_size=5)
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))


if __name__ == "__main__":
    record()