# The Note Backend

This backend implements Phase 0 of **The Note**, a multidimensional music intelligence system.
The application is built with FastAPI and integrates the following subsystems:

- Session controller orchestrating lifecycle and routing.
- Live audio ingestion with feature extraction.
- Sound understanding via psychoacoustic analysis.
- Lyric intelligence for grammar, IPA, and rhyme mapping.
- Creative imagination engine for lyrical and harmonic generation.
- Voice performance synthesis producing rendered audio waveforms.
- Adaptive neural memory with privacy-aware storage.
- Routing hub providing REST and WebSocket interfaces.

## Getting Started

```bash
poetry install
poetry run uvicorn thenote_backend.main:app --reload
```

## Testing

```bash
poetry run pytest
```
