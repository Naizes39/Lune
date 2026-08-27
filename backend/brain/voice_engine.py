import wave
from piper.voice import PiperVoice


lune_voice = PiperVoice.load("backend/models/voice/en_GB-alba-medium.onnx")


def synthesize_speech(text: str, output_path: str):
    with wave.open(output_path, "wb") as wav_file:
        wav_file.setnchannels(1) 
        wav_file.setsampwidth(2)
        wav_file.setframerate(lune_voice.config.sample_rate)
        lune_voice.synthesize(text, wav_file)


if __name__ == "__main__":
    synthesize_speech("test speech", "test_audio.wav")
