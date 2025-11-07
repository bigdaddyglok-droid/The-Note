/* eslint-disable react-refresh/only-export-components */
import {
  createContext,
  useContext,
  useMemo,
  useState,
  ReactNode,
  useCallback,
  useRef,
  useEffect
} from "react";
import { nanoid } from "nanoid/non-secure";
import { toast } from "sonner";

import type { AudioFrame, SessionEvent, SessionState } from "../api/types";
import { api, resolveWebSocketUrl } from "../api/client";

interface SessionContextValue {
  session: SessionState | null;
  isLoading: boolean;
  ensureSession: (payload: {
    user_id: string;
    intent: SessionState["metadata"]["intent"];
    daw?: string;
    key?: string;
    tempo?: number;
    emotional_goal?: string;
    references: string[];
  }) => Promise<SessionState>;
  closeSession: () => Promise<void>;
  pushAudioFrame: (buffer: Float32Array, sampleRate: number) => Promise<AudioFrame>;
  events: SessionEvent[];
}

const SessionContext = createContext<SessionContextValue | undefined>(undefined);

const isSessionEvent = (value: unknown): value is SessionEvent => {
  if (typeof value !== "object" || value === null) {
    return false;
  }
  const candidate = value as Record<string, unknown>;
  return (
    typeof candidate.session_id === "string" &&
    typeof candidate.source === "string" &&
    typeof candidate.target === "string" &&
    typeof candidate.created_at === "string" &&
    typeof candidate.payload === "object" &&
    candidate.payload !== null
  );
};

export const SessionProvider = ({ children }: { children: ReactNode }) => {
  const [session, setSession] = useState<SessionState | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [events, setEvents] = useState<SessionEvent[]>([]);
  const socketRef = useRef<WebSocket | null>(null);
  const reconnectTimer = useRef<number | null>(null);
  const sessionIdRef = useRef<string | null>(null);

  const disconnectStream = useCallback(() => {
    if (socketRef.current) {
      socketRef.current.close();
      socketRef.current = null;
    }
    if (reconnectTimer.current !== null) {
      window.clearTimeout(reconnectTimer.current);
      reconnectTimer.current = null;
    }
    setEvents([]);
  }, []);

  const connectStream = useCallback((sessionId: string) => {
    const url = resolveWebSocketUrl(`/ws/sessions/${sessionId}`);
    const socket = new WebSocket(url);
    socketRef.current = socket;

    socket.onmessage = (event: MessageEvent<string>) => {
      try {
        const parsed: unknown = JSON.parse(event.data);
        if (isSessionEvent(parsed)) {
          setEvents((prev) => [parsed, ...prev].slice(0, 100));
        } else {
          console.error("Received malformed session event payload", parsed);
        }
      } catch (error) {
        console.error("Failed to parse websocket event", error);
      }
    };

    socket.onclose = () => {
      socketRef.current = null;
      if (sessionIdRef.current === sessionId) {
        reconnectTimer.current = window.setTimeout(() => connectStream(sessionId), 1500);
      }
    };

    socket.onerror = (event) => {
      console.error("WebSocket error", event);
    };
  }, []);

  const ensureSession: SessionContextValue["ensureSession"] = useCallback(
    async (payload) => {
      if (session) {
        sessionIdRef.current = session.metadata.session_id;
        if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) {
          connectStream(session.metadata.session_id);
        }
        return session;
      }
      setIsLoading(true);
      try {
        const state = await api.createSession({
          ...payload,
          references: payload.references ?? []
        });
        setSession(state);
        sessionIdRef.current = state.metadata.session_id;
        connectStream(state.metadata.session_id);
        toast.success("Session initialized");
        return state;
      } catch (error) {
        toast.error(error instanceof Error ? error.message : "Failed to create session");
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    [session, connectStream]
  );

  const closeSession = useCallback(async () => {
    if (!session) return;
    setIsLoading(true);
    try {
      const closed = await api.closeSession(session.metadata.session_id);
      setSession(closed);
      sessionIdRef.current = null;
      disconnectStream();
      toast.success("Session closed");
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Failed to close session");
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [session, disconnectStream]);

  const pushAudioFrame = useCallback(
    async (buffer: Float32Array, sampleRate: number) => {
      if (!session) {
        throw new Error("Session not initialized");
      }
      const frameId = `frame_${nanoid(32)}`;
      const bytes = new Uint8Array(buffer.buffer);
      let binary = "";
      bytes.forEach((byte) => {
        binary += String.fromCharCode(byte);
      });
      const waveform = btoa(binary);
      const durationMs = (buffer.length / sampleRate) * 1000;
      const frame: AudioFrame = {
        session_id: session.metadata.session_id,
        frame_id: frameId,
        sample_rate: sampleRate,
        channels: 1,
        duration_ms: durationMs,
        waveform_base64: waveform,
        timestamp_ms: performance.now()
      };
      return api.submitAudio(session.metadata.session_id, frame);
    },
    [session]
  );

  const value = useMemo(
    () => ({
      session,
      isLoading,
      ensureSession,
      closeSession,
      pushAudioFrame,
      events
    }),
    [session, isLoading, ensureSession, closeSession, pushAudioFrame, events]
  );

  useEffect(
    () => () => {
      disconnectStream();
    },
    [disconnectStream]
  );

  return <SessionContext.Provider value={value}>{children}</SessionContext.Provider>;
};

export const useSessionContext = () => {
  const context = useContext(SessionContext);
  if (!context) {
    throw new Error("SessionContext is not available");
  }
  return context;
};
