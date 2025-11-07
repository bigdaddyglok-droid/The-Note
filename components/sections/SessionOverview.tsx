import type { FormEventHandler } from "react";
import { useForm } from "react-hook-form";
import { Zap, Activity, BarChart3 } from "lucide-react";

import { useSession } from "../../hooks/useSession";
import { useTelemetry } from "../../hooks/useTelemetry";
import { Button } from "../ui/Button";
import { Card } from "../ui/Card";
import { Input } from "../ui/Input";
import { Select } from "../ui/Select";
import { TagInput } from "../ui/TagInput";

type FormValues = {
  user_id: string;
  intent: "creative_session" | "mix_feedback" | "performance_coaching" | "analytics_only";
  daw?: string;
  key?: string;
  tempo?: number;
  emotional_goal?: string;
  references: string[];
};

const defaultValues: FormValues = {
  user_id: "artist_01",
  intent: "creative_session",
  references: []
};

export const SessionOverview = () => {
  const { session, ensureSession, closeSession, isLoading } = useSession();
  const { data: telemetry, isFetching: telemetryLoading } = useTelemetry();
  const { register, handleSubmit, setValue, watch } = useForm<FormValues>({
    defaultValues
  });
  const references = watch("references");

  const submitSession = handleSubmit((values: FormValues) => {
    void ensureSession({
      ...values,
      tempo: values.tempo ? Number(values.tempo) : undefined
    });
  });
  const handleFormSubmit: FormEventHandler<HTMLFormElement> = (event) => {
    void submitSession(event);
  };
  const handleCloseSession = () => {
    void closeSession();
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-white">Session Orchestrator</h1>
      <p className="text-white/70 max-w-3xl">
        Define intent, emotional compass, and sonic references. The controller will route every
        module according to this blueprint, enforcing alignment across audio, language, and memory
        systems.
      </p>

      <div className="grid grid-cols-2 gap-6">
        <Card
          title="Initialize Session"
          description="Set the objectives for this creative run before audio begins to flow."
        >
          <form className="space-y-4" onSubmit={handleFormSubmit}>
            <div className="grid grid-cols-2 gap-4">
              <label className="space-y-2">
                <span className="text-sm text-white/60">Artist Identifier</span>
                <Input placeholder="artist_01" {...register("user_id", { required: true })} />
              </label>
              <label className="space-y-2">
                <span className="text-sm text-white/60">Primary DAW</span>
                <Input placeholder="Ableton, Logic, etc." {...register("daw")} />
              </label>
            </div>

            <div className="grid grid-cols-3 gap-4">
              <label className="space-y-2">
                <span className="text-sm text-white/60">Intent</span>
                <Select {...register("intent", { required: true })}>
                  <option value="creative_session">Creative Session</option>
                  <option value="mix_feedback">Mix Feedback</option>
                  <option value="performance_coaching">Performance Coaching</option>
                  <option value="analytics_only">Analytics Only</option>
                </Select>
              </label>
              <label className="space-y-2">
                <span className="text-sm text-white/60">Key</span>
                <Input placeholder="Am, C#, etc." {...register("key")} />
              </label>
              <label className="space-y-2">
                <span className="text-sm text-white/60">Tempo</span>
                <Input type="number" placeholder="124" {...register("tempo", { valueAsNumber: true })} />
              </label>
            </div>

            <label className="space-y-2">
              <span className="text-sm text-white/60">Emotional Goal</span>
              <Input placeholder="e.g. radiant uplift, nocturnal calm" {...register("emotional_goal")} />
            </label>

            <label className="space-y-2">
              <span className="text-sm text-white/60">Reference Signals</span>
              <TagInput
                value={references}
                onChange={(tags) => setValue("references", tags)}
                placeholder="Add songs, artists, textures"
              />
            </label>

            <div className="flex items-center gap-3">
              <Button type="submit" loading={isLoading}>
                <Zap className="h-4 w-4" />
                {session ? "Session Active" : "Start Session"}
              </Button>
              {session && (
                <Button
                  type="button"
                  variant="ghost"
                  onClick={handleCloseSession}
                  loading={isLoading}
                >
                  Close Session
                </Button>
              )}
            </div>
          </form>
        </Card>

        <Card
          title="Session Telemetry"
          description="Live map of session metadata, including state flags and active module notes."
        >
          {session ? (
            <div className="space-y-3 text-sm">
              <div className="flex items-center justify-between">
                <span className="text-white/60">Session ID</span>
                <span className="font-mono text-xs text-accent">{session.metadata.session_id}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-white/60">Status</span>
                <span className="flex items-center gap-2 text-success">
                  <Activity className="h-4 w-4" />
                  {session.active ? "Online" : "Closed"}
                </span>
              </div>
              <div className="grid grid-cols-2 gap-2">
                <DataPoint label="Intent" value={session.metadata.intent.replace("_", " ")} />
                <DataPoint label="DAW" value={session.metadata.daw ?? "—"} />
                <DataPoint label="Key" value={session.metadata.key ?? "—"} />
                <DataPoint label="Tempo" value={session.metadata.tempo?.toString() ?? "—"} />
              </div>
              <DataPoint label="Emotion" value={session.metadata.emotional_goal ?? "—"} />
              <div>
                <p className="text-xs uppercase tracking-widest text-white/40 mb-1">References</p>
                <div className="flex flex-wrap gap-2">
                  {session.metadata.references.length ? (
                    session.metadata.references.map((item) => (
                      <span key={item} className="rounded-full bg-white/10 px-2 py-1 text-xs">
                        {item}
                      </span>
                    ))
                  ) : (
                    <span className="text-white/40 text-xs">No references captured</span>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <p className="text-white/60 text-sm">
              Initiate the session to unlock module routing, memory capture, and analytics.
            </p>
          )}
        </Card>
        <Card
          title="System Telemetry"
          description="Live counters and timers sampled from the orchestration core."
          className="col-span-2"
          actions={
            <div className="flex items-center gap-2 text-xs text-white/60">
              <BarChart3 className="h-4 w-4" />
              <span>{telemetryLoading ? "Refreshing..." : "Updated live every 5s"}</span>
            </div>
          }
        >
          {telemetry ? (
            <div className="grid grid-cols-4 gap-4 text-sm">
              <TelemetryMetric
                label="Sessions Created"
                value={telemetry["counter.sessions.created"] ?? 0}
              />
              <TelemetryMetric label="Sessions Closed" value={telemetry["counter.sessions.closed"] ?? 0} />
              <TelemetryMetric label="Audio Frames" value={telemetry["counter.audio.frames"] ?? 0} />
              <TelemetryMetric
                label="Voice Renders"
                value={telemetry["counter.voice.renders"] ?? 0}
              />
              <TelemetryMetric
                label="Lyric Analyses"
                value={telemetry["counter.lyrics.analyzed"] ?? 0}
              />
              <TelemetryMetric
                label="Imagination Requests"
                value={telemetry["counter.imagination.requests"] ?? 0}
              />
              <TelemetryMetric
                label="Analysis Mean (ms)"
                value={telemetry["timer.analysis.frame_duration.mean_ms"] ?? 0}
                precision={2}
              />
              <TelemetryMetric
                label="Analysis Count"
                value={telemetry["timer.analysis.frame_duration.count"] ?? 0}
              />
            </div>
          ) : (
            <p className="text-sm text-white/50">Telemetry will populate once activity begins.</p>
          )}
        </Card>
      </div>
    </div>
  );
};

const DataPoint = ({ label, value }: { label: string; value: string }) => (
  <div>
    <p className="text-xs uppercase tracking-widest text-white/40">{label}</p>
    <p className="text-sm text-white">{value}</p>
  </div>
);

const TelemetryMetric = ({
  label,
  value,
  precision = 0
}: {
  label: string;
  value: number;
  precision?: number;
}) => (
  <div className="rounded-xl bg-white/5 p-3">
    <p className="text-xs uppercase tracking-[0.3em] text-white/40">{label}</p>
    <p className="text-lg font-semibold text-white mt-1">
      {Number.isFinite(value) ? value.toFixed(precision) : "0"}
    </p>
  </div>
);
