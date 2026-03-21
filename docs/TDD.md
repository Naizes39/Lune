# LUNE: Technical Design Document (TDD)
**Version:** 1.0
**Target Hardware:** Edge-local (NVIDIA RTX 3050, 4GB VRAM)
**Latency Constraint:** < 500ms Time-to-First-Byte (TTFB)
**Core Function:** Real-time, pedagogical AI agent for mastering spoken English.

---

## 1. System Architecture & The Tech Stack
To maintain a strict 4GB VRAM footprint while achieving conversational parallelism, the system relies on a hybrid Local-Cloud architecture orchestrated via asynchronous Python.

* **The Central Orchestrator:** `FastAPI` (Python). Chosen for its native asynchronous capabilities (`asyncio`) and high-performance WebSocket handling.
* **Acoustic VAD (Local):** `Silero VAD v5`. An ultra-lightweight Voice Activity Detector. It infers in <2ms, detecting speech pauses instantly without occupying the GPU.
* **Speech-to-Text (Cloud):** `Deepgram Nova-2`. A high-speed STT API. It streams via WebSockets and natively returns word-level JSON confidence scores, critical for phonetic articulation grading.
* **The Cognitive Engine (Local):** `Llama-3.2-3B-Instruct` (Quantized to 4-bit AWQ or GGUF format). This quantization compresses the model to approximately 2.2GB, fitting inside the 4GB VRAM limit while leaving room for context buffering.
* **Text-to-Speech (Cloud):** `Cartesia Sonic` or `ElevenLabs Flash v2.5`. Both offer WebSocket streaming with <200ms latency, matching our Semantic Chunking pipeline.
* **Long-Term Memory (Local):** `ChromaDB`. An open-source vector database that runs entirely on the CPU/Drive, requiring zero GPU VRAM.
* **Visual Rendering (Client-Side):** `Three.js` combined with `Rhubarb Lip Sync` (WASM). This runs entirely in the user's web browser, directly mapping audio frequencies to 3D blendshapes without requiring server-side video rendering.

---

## 2. The Input Pipeline (Audio & Acoustic Profiling)
The input layer operates on a continuous, non-blocking WebSocket stream to bypass sequential recording delays and monitor user stress levels.

### 2.1 Buffer & Chunking Physics
1. The client browser captures microphone input at **16,000 Hz** (16-bit PCM).
2. The audio is sliced into **100-millisecond discrete chunks**.
3. These chunks are fired continuously over a persistent WebSocket connection to the local FastAPI server, which proxies them to the Deepgram Cloud STT.

### 2.2 Semantic Endpointing
Instead of interrupting the user during a cognitive pause, the pipeline uses a dual-lock heuristic:
* **Condition A (Acoustic):** Silero VAD detects > 400ms of absolute silence.
* **Condition B (Semantic):** The FastAPI orchestrator analyses the interim text string. If the string ends with a syntactic boundary (e.g., `.`, `?`), the orchestrator evaluates the phrase for completeness.
* Only when both conditions align does the FastAPI router seal the input string and pass the final transcript to the Llama-3B inference queue.

### 2.3 Dynamic Speech Rate Profiling & Articulation
* **WPM Calculation:** FastAPI calculates the user's words per minute: 
  $WPM = (\frac{Word Count}{End Time - Start Time}) \times 60$
  If WPM exceeds 180, the system triggers a pedagogical intervention state, advising the user to slow down and manage stress.
* **Phonetic Grading:** The system extracts the JSON confidence scores from the STT output. Any word falling below a 0.70 confidence threshold is flagged as a mispronunciation, prompting the LLM to offer articulatory corrections.

---

## 3. Cognitive Orchestration & State Machine
To prevent VRAM overflow during extended sessions, LUNE employs Proactive Context Flushing and state-machine logic.

### 3.1 Token Monitoring & Injection
The Python orchestrator continuously monitors the active `token_count`. When the context approaches the hardware limit (e.g., 3,500 tokens), the system injects hidden control states into the LLM prompt.

### 3.2 The <save> and <end> Protocol
* **The <save> State:** The LLM generates a `<save>` token, prompting the TTS to output a latency-hiding phrase (e.g., *"Let me organise my notes on this..."*). The system pauses the microphone, runs a Salience Scorer to extract vital facts, flushes these to ChromaDB (Vector DB), clears the short-term VRAM buffer, and resumes the conversation seamlessly.
* **The <end> State:** Signifies session termination. The VRAM is fully wiped, and the distilled summary is saved. Upon the next startup, ChromaDB retrieves these embeddings to re-establish shared context.

---

## 4. Multimodal Output Pipeline
The output pipeline guarantees natural human prosody and visual synchronisation without triggering GPU bottlenecks.

### 4.1 Semantic Output Chunking
Sequential generation introduces unacceptable delays. Instead:
1. Llama-3B streams generated text tokens into a dynamic buffer.
2. A localised heuristic router monitors the buffer for syntactic boundary markers (e.g., `,`, `.`, `?`, `!`).
3. Upon detecting a boundary, the buffer flushes the complete semantic clause to the TTS inference engine.
4. Audio playback commences on Chunk $N$ while the LLM concurrently generates text for Chunk $N+1$, preserving intonation.

### 4.2 Viseme Synchronisation
Video rendering is entirely bypassed to protect VRAM. 
1. The Cloud TTS returns the generated audio file.
2. A lightweight audio-to-viseme model analyses the frequency amplitudes.
3. The model outputs an array of timestamped float values corresponding to facial phonemes.
4. The client-side browser applies these values directly to the 3D model's predefined blendshapes (e.g., `mouth_open`, `lips_pucker`), resulting in flawless lip-sync with zero GPU rendering cost.

---

## 5. Event-Driven Tool Routing & Latency Hiding
To maintain response speed, external API calls are strictly context-dependent and asynchronously masked.

### 5.1 Event-Driven MCP (Model Context Protocol)
The system does not query external tools (like News APIs) continuously. A lightweight classifier node evaluates the conversation state. The MCP is only invoked during explicit user requests, topic conclusions, or conversational lulls (dead air), ensuring network latency is only introduced when pedagogically valuable.

### 5.2 Asynchronous Latency Hiding
When an MCP tool *is* invoked (e.g., a 2.5-second web search), the FastAPI orchestrator simultaneously fires a pre-computed "filler" string to the TTS engine (e.g., *"That is a brilliant question, let me pull up the latest data..."*). The user listens to the 3D avatar speak this phrase while the system completes the heavy processing in the background, effectively reducing perceived latency to 0ms.
