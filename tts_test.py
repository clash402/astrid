from kokoro import KModel, KPipeline
import soundfile as sf

# Initialize the pipeline (English 'a' for American)
pipeline = KPipeline(lang_code="a")

# Generate audio
generator = pipeline(
    "Hello! I am Astrid, running locally. What would you like to talk about?",
    voice="af_bella",
    speed=1,
)

for i, (gs, ps, audio) in enumerate(generator):
    sf.write(f"astrid-tts-test-{i+1}.mp3", audio, 24000)  # Save as WAV file
