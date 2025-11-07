# The Note – Phase 0 Architecture

## System Topology

```
┌───────────────────┐
│ Interface Layer   │  React + Vite dashboard
│  • Session setup  │  Routes: /session /audio /lyrics /create /voice /memory
│  • Audio upload   │
│  • Lyric insight  │
└─────────┬─────────┘
          │ HTTPS (REST + WebSocket reserved)
┌─────────▼─────────┐
│ Routing Hub (API) │  FastAPI gateway, async endpoints
│  • Auth hooks     │
│  • Rate limiting  │
│  • Event dispatch │
└─────────┬─────────┘
          │ Module events via in-memory bus
┌─────────▼───────────────────────────────┐
│ Main Controller / Session Engine        │
│  • Session state, lifecycle             │
│  • Policy enforcement                   │
│  • Broadcast events                     │
├─────────┬───────────────────────────────┤
│ Live Audio Input                        │
│  • WebRTC-ready ingest pathway          │
│  • RMS / peak computation               │
│  • Publishes frames to analysis         │
├─────────┬───────────────────────────────┤
│ Sound Understanding Engine              │
│  • Autocorrelation pitch detector       │
│  • Beat envelope rhythm estimator       │
│  • FFT spectral energy map              │
│  • Emotion + timbre synthesis           │
│  • Stores per-frame analysis            │
├─────────┬───────────────────────────────┤
│ Language + Lyric Intelligence           │
│  • IPA conversion, stress tagging       │
│  • Rhyme key extraction                 │
│  • Vocabulary suggestion engine         │
│  • Streams payload to imagination       │
├─────────┬───────────────────────────────┤
│ Imagination Engine                      │
│  • Prompt-to-lyric / melody / metaphor  │
│  • Configurable generation modes        │
│  • Confidence scoring                   │
├─────────┬───────────────────────────────┤
│ Voice Performance Synth                 │
│  • Procedural harmonic renderer         │
│  • Dynamic shaping + checksum           │
│  • Publishes renders to memory          │
├─────────┬───────────────────────────────┤
│ Adaptive Memory                         │
│  • JSON-backed consented storage        │
│  • Embedding aggregation                │
│  • Retention policy enforcement         │
└─────────────────────────────────────────┘
```

## Key Data Contracts

| Contract             | Origin Module          | Consumer(s)              | Notes                                                                 |
|----------------------|------------------------|--------------------------|-----------------------------------------------------------------------|
| `SessionMetadata`    | Interface → Controller | All modules              | Carries intent, DAW, key, tempo, emotional goal, references.          |
| `AudioFrame`         | Live Audio Input       | Sound Understanding      | Mono-normalised Float32, base64 encoded, includes RMS/peak.           |
| `AnalysisFrame`      | Sound Understanding    | Language / UI            | Pitch (Hz/note), rhythm (BPM/swing), spectral bands, emotion, timbre. |
| `LyricInsight`       | Language Module        | Imagination / UI         | IPA arrays, stress map, term suggestions, grammar notes.              |
| `GenerationBundle`   | Imagination Engine     | Voice Synth / UI         | Mode-tagged creative payloads + confidence scores.                    |
| `RenderedAudio`      | Voice Synth            | Adaptive Memory / UI     | Base64 WAV + duration, loudness, checksum.                            |
| `MemoryRecord`       | Adaptive Memory        | Interface Layer          | Consent token, profile embedding mean, contextual summary.            |

Schema definitions live under `backend/src/thenote_backend/schemas` and are mirrored in `frontend/src/api/types.ts`.

## Module Responsibilities

### Backend
- **Session Controller** keeps authoritative state, validates lifecycle transitions, and broadcasts session events onto the event bus.
- **Event Bus** is an in-memory async dispatcher. Targets are module enum names or `broadcast`.
- **Live Audio Input** normalises incoming frames, computes RMS/peak, and publishes to Sound Understanding.
- **Sound Understanding** performs pure NumPy DSP to avoid heavyweight dependencies: autocorrelation pitch, amplitude envelope tempo, FFT spectral distribution, and derived emotion/timbre metrics.
- **Language & Lyric** uses deterministic utilities for IPA mapping, syllable stress, rhyme extraction, plus vocabulary frequency signals for suggestions.
- **Imagination Engine** delivers seeded creative outputs per mode; random seeds ensure variety while mapping to mood.
- **Voice Performance** generates deterministic audio using additive synthesis and exports WAV data + checksum.
- **Adaptive Memory** persists entries to JSON with optional data-dir override; aggregates embeddings as simple averages.
- **Routing Hub** exposes REST endpoints aligning to the blueprint: session management, audio ingest, lyric analysis, generation, rendering, memory storage.

### Frontend
- **React Dashboard**: Vite + Tailwind interface with navigation for each subsystem.
- **Session Context**: Handles creation/closure, audio frame submission, exposes hooks across the app.
- **Sections**: Dedicated panels for audio ingest, lyric analysis, imagination, voice rendering, and memory oversight.
- **API Client**: Thin fetch wrapper honouring `VITE_BACKEND_URL` with consistent error handling.
- **Hooks**: `useLyricAnalysis`, `useGeneration`, `useVoiceRenderer`, `useMemory` encapsulate async flows with toast feedback.

## Operational Considerations
- **Environment**: Backend expects Python 3.11+, optional virtualenv (`.venv`). Frontend uses Node 20+.
- **Testing**: `tests/test_workflow.py` executes end-to-end cycle (session → audio → lyrics → generation → voice → close).
- **Telemetry**: TODO for Phase 1 is to wire structured logging and metrics exporters (OpenTelemetry).
- **Scaling Path**:
  1. Replace in-memory bus with Redis/NATS for horizontal module scaling.
  2. Swap deterministic DSP implementations with GPU-backed models.
  3. Introduce WebSocket streaming to push analysis frames to UI in real time.
  4. Implement auth / RBAC on routing hub once multi-user needed.

## Next Steps
1. **Stabilise Testing**: Ensure pytest suite completes locally (resolving long runtime) and add frontend vitest coverage.
2. **Feature Streaming**: Extend API with `/sessions/{id}/stream` WebSocket bridging event bus to clients.
3. **Persistent Store**: Replace JSON memory with encrypted database + rotation policies.
4. **Audio Capture**: Implement browser WebRTC capture to feed live buffers without uploads.
5. **CI/CD**: Set up GitHub Actions (lint, type-check, tests) and container build for backend/frontend.
