import type {
  AudioFrame,
  GenerationBundle,
  LyricInsight,
  MemoryRecord,
  RenderInstruction,
  RenderedAudio,
  SessionMetadata,
  SessionState,
  TranscriptChunk,
  TelemetrySnapshot
} from "./types";

const resolveBaseUrl = () =>
  (import.meta.env.VITE_BACKEND_URL as string | undefined) ?? "http://127.0.0.1:8000";

const baseUrl = resolveBaseUrl();

export const resolveWebSocketUrl = (path: string): string => {
  const url = new URL(baseUrl);
  url.protocol = url.protocol === "https:" ? "wss:" : "ws:";
  url.pathname = path.startsWith("/") ? path : `/${path}`;
  url.search = "";
  return url.toString();
};

const jsonHeaders = {
  "Content-Type": "application/json",
  Accept: "application/json"
};

async function handle<ResponseData>(response: Response): Promise<ResponseData> {
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed with status ${response.status}`);
  }
  if (response.status === 204) {
    return undefined as ResponseData;
  }
  return (await response.json()) as ResponseData;
}

export const api = {
  async createSession(metadata: Omit<SessionMetadata, "session_id" | "created_at">): Promise<SessionState> {
    const response = await fetch(`${baseUrl}/sessions`, {
      method: "POST",
      headers: jsonHeaders,
      body: JSON.stringify(metadata)
    });
    return handle<SessionState>(response);
  },

  async closeSession(sessionId: string): Promise<SessionState> {
    const response = await fetch(`${baseUrl}/sessions/${sessionId}/close`, {
      method: "POST",
      headers: jsonHeaders
    });
    return handle<SessionState>(response);
  },

  async submitAudio(sessionId: string, frame: AudioFrame): Promise<AudioFrame> {
    const response = await fetch(`${baseUrl}/sessions/${sessionId}/audio`, {
      method: "POST",
      headers: jsonHeaders,
      body: JSON.stringify(frame)
    });
    return handle<AudioFrame>(response);
  },

  async submitTranscript(sessionId: string, chunk: TranscriptChunk): Promise<TranscriptChunk> {
    const response = await fetch(`${baseUrl}/sessions/${sessionId}/transcript`, {
      method: "POST",
      headers: jsonHeaders,
      body: JSON.stringify(chunk)
    });
    return handle<TranscriptChunk>(response);
  },

  async analyzeLyrics(sessionId: string, payload: { session_id: string; section_id: string; text: string }): Promise<LyricInsight> {
    const response = await fetch(`${baseUrl}/sessions/${sessionId}/lyrics/analyze`, {
      method: "POST",
      headers: jsonHeaders,
      body: JSON.stringify(payload)
    });
    return handle<LyricInsight>(response);
  },

  async generate(sessionId: string, request: Record<string, unknown>): Promise<GenerationBundle> {
    const response = await fetch(`${baseUrl}/sessions/${sessionId}/generate`, {
      method: "POST",
      headers: jsonHeaders,
      body: JSON.stringify(request)
    });
    return handle<GenerationBundle>(response);
  },

  async renderVoice(sessionId: string, instruction: RenderInstruction): Promise<RenderedAudio> {
    const response = await fetch(`${baseUrl}/sessions/${sessionId}/render`, {
      method: "POST",
      headers: jsonHeaders,
      body: JSON.stringify(instruction)
    });
    return handle<RenderedAudio>(response);
  },

  async storeMemory(sessionId: string, record: MemoryRecord): Promise<MemoryRecord> {
    const response = await fetch(`${baseUrl}/sessions/${sessionId}/memory`, {
      method: "POST",
      headers: jsonHeaders,
      body: JSON.stringify(record)
    });
    return handle<MemoryRecord>(response);
  },

  async getLatestMemory(userId: string): Promise<MemoryRecord | null> {
    const response = await fetch(`${baseUrl}/memory/${userId}`);
    if (response.status === 404) {
      return null;
    }
    return handle<MemoryRecord | null>(response);
  },

  async getTelemetry(): Promise<TelemetrySnapshot> {
    const response = await fetch(`${baseUrl}/telemetry`);
    return handle<TelemetrySnapshot>(response);
  },

  async voiceChat(payload: { session_id: string; transcript: string; audio_features: number[] | null }): Promise<{ response: string; intent: string; consciousness: Record<string, unknown>; session_id: string }> {
    const response = await fetch(`${baseUrl}/voice/chat`, {
      method: "POST",
      headers: jsonHeaders,
      body: JSON.stringify(payload)
    });
    return handle(response);
  }
};
