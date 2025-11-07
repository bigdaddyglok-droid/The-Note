import { ChangeEvent, useRef, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { AudioWaveform, Upload, Type, Mic, StopCircle } from "lucide-react";

import { useSession } from "../../hooks/useSession";
import { api } from "../../api/client";
import type { AudioFrame, TranscriptChunk } from "../../api/types";
import { Button } from "../ui/Button";
import { Card } from "../ui/Card";
import { Textarea } from "../ui/Textarea";
import { Input } from "../ui/Input";
import { useLiveAudioCapture } from "../../hooks/useLiveAudioCapture";

const audioContext = () => new AudioContext({ sampleRate: 22_050 });

export const AudioPipeline = () => {
  const { session, pushAudioFrame, events } = useSession();
  const [lastFrame, setLastFrame] = useState<AudioFrame | null>(null);
  const [transcript, setTranscript] = useState("");
  const [language, setLanguage] = useState("en");
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const analysisEvents = events.filter((event) => event.source === "sound_understanding").slice(0, 5);
  const { startCapture, stopCapture, isCapturing } = useLiveAudioCapture();
  const handleStartCapture = () => {
    void startCapture();
  };
  const handleStopCapture = () => {
    stopCapture();
  };

  const transcriptMutation = useMutation({
    mutationFn: async () => {
      if (!session) throw new Error("Session is not active");
      if (!transcript.trim()) throw new Error("Transcript text is required");
      const chunk: TranscriptChunk = {
        session_id: session.metadata.session_id,
        chunk_id: `chunk_${window.crypto.randomUUID().replace(/-/g, "")}`,
        start_ms: 0,
        end_ms: transcript.length * 10,
        text: transcript,
        confidence: 0.95,
        language
      };
      return api.submitTranscript(session.metadata.session_id, chunk);
    },
    onSuccess: () => {
      toast.success("Transcript delivered to language module");
      setTranscript("");
    },
    onError: (error) => {
      toast.error(error instanceof Error ? error.message : "Failed to submit transcript");
    }
  });

  const onFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const input = event.target;
    const file = input.files?.[0];
    const resetInput = () => {
      input.value = "";
    };
    if (!session) {
      toast.error("Start a session before uploading audio.");
      resetInput();
      return;
    }
    if (!file) {
      resetInput();
      return;
    }
    void (async () => {
      try {
        const context = audioContext();
        const arrayBuffer = await file.arrayBuffer();
        const decoded = await context.decodeAudioData(arrayBuffer);
        const channelData = decoded.getChannelData(0);
        const frame = await pushAudioFrame(channelData, decoded.sampleRate);
        setLastFrame(frame);
        toast.success("Audio frame ingested");
      } catch (error) {
        toast.error(error instanceof Error ? error.message : "Failed to ingest audio");
      } finally {
        resetInput();
      }
    })();
  };

  const triggerUpload = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-white">Audio Resonance Pipeline</h1>
      <p className="text-white/70 max-w-3xl">
        Upload stems or captures to stream psychoacoustic features into the Sound Understanding
        Engine. Pair transcripts with audio to align lyric and emotion analyzers.
      </p>

      <div className="grid grid-cols-2 gap-6">
        <Card
          title="Waveform Intake"
          description="FFT-ready buffer ingestion with loudness telemetry and routing into analysis bus."
          actions={
            <div className="flex gap-2">
              <Button onClick={triggerUpload}>
                <Upload className="h-4 w-4" />
                Upload Audio
              </Button>
              <Button
                type="button"
                variant={isCapturing ? "secondary" : "primary"}
                onClick={isCapturing ? handleStopCapture : handleStartCapture}
              >
                {isCapturing ? <StopCircle className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
                {isCapturing ? "Stop Live Capture" : "Start Live Capture"}
              </Button>
            </div>
          }
        >
          <input
            ref={fileInputRef}
            type="file"
            accept="audio/*"
            className="hidden"
            onChange={onFileChange}
          />
          {session ? (
            <div className="space-y-4 text-sm">
              <p className="text-white/60">
                Latest frame metrics will appear after ingest. Audio is resampled to mono before FFT
                to maintain feature parity.
              </p>
              {lastFrame ? (
                <div className="grid grid-cols-2 gap-3 rounded-xl bg-white/5 p-4">
                  <Metric label="Frame ID" value={lastFrame.frame_id.slice(-12)} />
                  <Metric label="Sample Rate" value={`${lastFrame.sample_rate} Hz`} />
                  <Metric
                    label="Duration"
                    value={`${lastFrame.duration_ms.toFixed(1)} ms`}
                  />
                  <Metric label="RMS" value={lastFrame.rms?.toFixed(3) ?? "pending"} />
                </div>
              ) : (
                <div className="flex items-center gap-3 rounded-xl border border-dashed border-white/20 p-4 text-white/50">
                  <AudioWaveform className="h-6 w-6" />
                  <span>Awaiting first frame. Upload wav, aiff, or mp3 to begin.</span>
                </div>
              )}
              {analysisEvents.length > 0 && (
                <div className="rounded-xl bg-white/5 p-4">
                  <p className="text-xs uppercase tracking-[0.3em] text-white/40 mb-2">
                    Live Analysis Feed
                  </p>
                  <ul className="space-y-2">
                    {analysisEvents.map((event, index) => {
                      const payload = event.payload ?? {};
                      const emotion = payload.emotion as Record<string, unknown> | undefined;
                      const pitch = payload.pitch as Record<string, unknown> | undefined;
                      const rhythm = payload.rhythm as Record<string, unknown> | undefined;
                      const pitchNote = typeof pitch?.note === "string" ? pitch.note : "—";
                      const pitchHz = typeof pitch?.hz === "number" ? pitch.hz : null;
                      const rhythmBpm = typeof rhythm?.bpm === "number" ? rhythm.bpm : null;
                      const rhythmSwing = typeof rhythm?.swing === "number" ? rhythm.swing : null;
                      return (
                        <li key={`${event.created_at}-${index}`} className="rounded-lg bg-background/60 px-3 py-2">
                          <div className="flex items-center justify-between text-xs text-white/60">
                            <span>{new Date(event.created_at).toLocaleTimeString()}</span>
                            <span className="text-accent font-medium">
                              {typeof emotion?.label === "string" ? emotion.label : "—"}
                            </span>
                          </div>
                          <div className="mt-1 flex flex-wrap gap-3 text-xs text-white/70">
                            <span>
                              Pitch: {pitchNote} ({pitchHz !== null ? pitchHz.toFixed(2) : "—"} Hz)
                            </span>
                            <span>
                              BPM: {rhythmBpm !== null ? rhythmBpm.toFixed(1) : "—"}
                            </span>
                            <span>
                              Swing: {rhythmSwing !== null ? rhythmSwing.toFixed(2) : "—"}
                            </span>
                          </div>
                        </li>
                      );
                    })}
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <p className="text-sm text-white/50">
              Session must be active. Declare intent in the Session panel first.
            </p>
          )}
        </Card>

        <Card
          title="Transcript Injection"
          description="Align narrative content with spectral analysis for cross-modal intelligence."
        >
          <div className="space-y-3">
            <Textarea
              value={transcript}
              onChange={(event) => setTranscript(event.target.value)}
              placeholder="Paste or dictate transcription aligned to recent audio capture..."
            />
            <div className="grid grid-cols-[1fr_auto] gap-3">
              <Input
                value={language}
                onChange={(event) => setLanguage(event.target.value)}
                placeholder="Language code (en, es, fr...)"
              />
              <Button
                type="button"
                variant="secondary"
                onClick={() => transcriptMutation.mutate()}
                loading={transcriptMutation.isPending}
              >
                <Type className="h-4 w-4" />
                Send Transcript
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

const Metric = ({ label, value }: { label: string; value: string }) => (
  <div>
    <p className="text-xs uppercase tracking-widest text-white/40">{label}</p>
    <p className="text-sm text-white font-medium">{value}</p>
  </div>
);
