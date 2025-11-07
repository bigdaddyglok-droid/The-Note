import { useEffect, useRef, useState } from "react";
import { toast } from "sonner";
import { Play, StopCircle, Waves } from "lucide-react";

import { useVoiceRenderer } from "../../hooks/useVoiceRenderer";
import { useGeneration } from "../../hooks/useGeneration";
import { useSession } from "../../hooks/useSession";
import { Button } from "../ui/Button";
import { Card } from "../ui/Card";
import { Textarea } from "../ui/Textarea";
import type { GeneratedItem } from "../../api/types";

const voiceProfiles = [
  { id: "luminous_alto", label: "Luminous Alto" },
  { id: "radiant_tenor", label: "Radiant Tenor" },
  { id: "velvet_baritone", label: "Velvet Baritone" }
];

export const VoicePerformance = () => {
  const { session } = useSession();
  const { bundle } = useGeneration();
  const { render, renderVoice, isRendering } = useVoiceRenderer();
  const [text, setText] = useState("Ignite the skyline, breathe the silver fire.");
  const [profile, setProfile] = useState("luminous_alto");
  const [dynamics, setDynamics] = useState("mezzo-forte");
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    if (!bundle) return;
    const lyricPayload = bundle.outputs.find(
      (item: GeneratedItem) => item.type === "lyric"
    )?.payload;
    if (lyricPayload && isLyricPayload(lyricPayload)) {
      setText(lyricPayload.lines.join("\n"));
    }
  }, [bundle]);

  const triggerRender = () => {
    void (async () => {
      try {
        await renderVoice(text, profile, dynamics);
      } catch (error) {
        toast.error(error instanceof Error ? error.message : "Render failed");
      }
    })();
  };

  const playAudio = () => {
    if (!render) return;
    const audio = audioRef.current ?? new window.Audio();
    audioRef.current = audio;
    audio.src = `data:audio/wav;base64,${render.url_or_blob}`;
    audio.play().catch((error) => {
      toast.error(error instanceof Error ? error.message : "Playback error");
    });
  };

  const stopAudio = () => {
    audioRef.current?.pause();
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-white">Voice Performance Synth</h1>
      <p className="text-white/70 max-w-3xl">
        Convert generated text into tone-matched vocal renderings. Adjust profiles and dynamics to
        audition emotional contours in seconds.
      </p>

      <div className="grid grid-cols-2 gap-6">
        <Card
          title="Performance Directive"
          description="Define text, select timbre, and choose expressive intensity."
          actions={
            <Button onClick={triggerRender} loading={isRendering} disabled={!session}>
              <Waves className="h-4 w-4" />
              Render Voice
            </Button>
          }
        >
          <Textarea
            value={text}
            onChange={(event) => setText(event.target.value)}
            disabled={!session}
            className="min-h-[200px]"
          />
          <div className="grid grid-cols-2 gap-4">
            <label className="space-y-1 text-xs text-white/60 uppercase tracking-[0.3em]">
              Voice Profile
              <div className="flex gap-2">
                {voiceProfiles.map((option) => (
                  <button
                    key={option.id}
                    type="button"
                    onClick={() => setProfile(option.id)}
                    className={`flex-1 rounded-xl border px-3 py-2 text-sm transition ${
                      profile === option.id
                        ? "border-accent bg-accent/10 text-accent"
                        : "border-white/10 text-white/70 hover:border-white/30"
                    }`}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </label>
            <label className="space-y-1 text-xs text-white/60 uppercase tracking-[0.3em]">
              Dynamics
              <input
                value={dynamics}
                onChange={(event) => setDynamics(event.target.value)}
                className="w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm text-white focus:border-accent focus:outline-none"
                placeholder="mezzo-forte"
              />
            </label>
          </div>
        </Card>

        <Card
          title="Rendered Output"
          description="Listen back to the synthetic performance. Peak data updates with each render."
        >
          {render ? (
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <Button onClick={playAudio} variant="secondary">
                  <Play className="h-4 w-4" />
                  Play
                </Button>
                <Button onClick={stopAudio} variant="ghost">
                  <StopCircle className="h-4 w-4" />
                  Stop
                </Button>
              </div>
              <dl className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <dt className="text-white/40 uppercase tracking-[0.3em] text-xs">Duration</dt>
                  <dd className="text-white">{render.duration_ms.toFixed(0)} ms</dd>
                </div>
                <div>
                  <dt className="text-white/40 uppercase tracking-[0.3em] text-xs">Loudness</dt>
                  <dd className="text-white">{render.loudness.toFixed(3)} LUFS proxy</dd>
                </div>
                <div>
                  <dt className="text-white/40 uppercase tracking-[0.3em] text-xs">Checksum</dt>
                  <dd className="text-white font-mono text-xs">{render.checksum.slice(0, 16)}</dd>
                </div>
              </dl>
            </div>
          ) : (
            <p className="text-white/50 text-sm">
              Render audio to reveal performance metrics and playback controls.
            </p>
          )}
        </Card>
      </div>
    </div>
  );
};

const isLyricPayload = (
  payload: Record<string, unknown>
): payload is { lines: string[]; prompt: string } => Array.isArray(payload.lines);
