export type IntentType =
  | "creative_session"
  | "mix_feedback"
  | "performance_coaching"
  | "analytics_only";

export interface SessionMetadata {
  session_id: string;
  user_id: string;
  intent: IntentType;
  daw?: string | null;
  key?: string | null;
  tempo?: number | null;
  emotional_goal?: string | null;
  references: string[];
  created_at: string;
}

export interface SessionState {
  metadata: SessionMetadata;
  active: boolean;
  attributes: Record<string, unknown>;
}

export interface AudioFrame {
  session_id: string;
  frame_id: string;
  sample_rate: number;
  channels: number;
  duration_ms: number;
  waveform_base64: string;
  rms?: number | null;
  peak?: number | null;
  timestamp_ms: number;
}

export interface TranscriptChunk {
  session_id: string;
  chunk_id: string;
  start_ms: number;
  end_ms: number;
  text: string;
  confidence: number;
  language: string;
}

export interface Syllable {
  text: string;
  stress: string;
  phonemes: string[];
}

export interface LyricLineInsight {
  original: string;
  normalized: string;
  syllables: Syllable[];
  ipa: string[];
  rhyme_key: string;
}

export interface LyricInsight {
  session_id: string;
  section_id: string;
  lines: LyricLineInsight[];
  grammar_notes: string[];
  term_suggestions: string[];
}

export interface GeneratedItem {
  type: "lyric" | "melody" | "metaphor" | "structure";
  payload: Record<string, unknown>;
  confidence: number;
}

export interface GenerationBundle {
  session_id: string;
  request_id: string;
  outputs: GeneratedItem[];
}

export interface RenderInstruction {
  session_id: string;
  render_id: string;
  text: string;
  melody?: number[] | null;
  voice_profile: string;
  dynamics: string;
  format: string;
}

export interface RenderedAudio {
  session_id: string;
  render_id: string;
  url_or_blob: string;
  duration_ms: number;
  loudness: number;
  checksum: string;
}

export interface MemoryRecord {
  session_id: string;
  user_id: string;
  consent_token: string;
  profile_embedding: number[];
  context_summary: string;
  retention_policy: string;
  created_at: string;
}

export interface SessionEvent {
  session_id: string;
  source: string;
  target: string;
  payload: Record<string, unknown>;
  created_at: string;
}

export type TelemetrySnapshot = Record<string, number>;
