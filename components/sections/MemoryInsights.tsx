import { Shield, Clock } from "lucide-react";

import { useMemory } from "../../hooks/useMemory";
import { useSession } from "../../hooks/useSession";
import { Card } from "../ui/Card";
import { Button } from "../ui/Button";

export const MemoryInsights = () => {
  const { session } = useSession();
  const { record, isFetching, refresh } = useMemory();

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-white">Adaptive Memory</h1>
      <p className="text-white/70 max-w-3xl">
        This layer stores consented artifacts for personalization. Toggle retention policies,
        observe embeddings, and ensure compliance with the user&apos;s creative sovereignty.
      </p>

      <div className="grid grid-cols-2 gap-6">
        <Card
          title="Memory Snapshot"
          description="Inspection of the latest consented memory entry for this creator."
          actions={
            <Button variant="secondary" onClick={refresh} loading={isFetching} disabled={!session}>
              Refresh
            </Button>
          }
        >
          {session ? (
            record ? (
              <div className="space-y-4 text-sm">
                <div className="grid grid-cols-2 gap-3">
                  <Data label="Session" value={record.session_id.slice(-12)} />
                  <Data label="Retention" value={record.retention_policy} />
                  <Data label="Consent Token" value={record.consent_token.slice(0, 12)} />
                  <Data label="Embedding Size" value={`${record.profile_embedding.length}`} />
                </div>
                <div>
                  <p className="text-xs uppercase tracking-[0.3em] text-white/40">Summary</p>
                  <p className="mt-1 text-white/80">{record.context_summary}</p>
                </div>
                <div className="flex items-center gap-2 text-xs text-white/50">
                  <Clock className="h-4 w-4" />
                  Stored at {new Date(record.created_at).toLocaleString()}
                </div>
              </div>
            ) : (
              <p className="text-sm text-white/50">
                No memories stored yet. Voice renders or explicit commands will create entries when
                consented.
              </p>
            )
          ) : (
            <p className="text-sm text-white/50">Activate a session to load memory context.</p>
          )}
        </Card>

        <Card
          title="Ethics & Permissions"
          description="Transparent control over retention to maintain trust with creators."
        >
          <div className="space-y-3 text-sm text-white/70">
            <p>
              Adaptive memory is opt-in per session. Only data explicitly written via the memory
              endpoint is retained, and retention policies are enforced at write time.
            </p>
            <ul className="list-disc pl-5 space-y-1">
              <li>Consent tokens are signed per user and session.</li>
              <li>Retention defaults to 90 days but supports bespoke timelines.</li>
              <li>Embeddings remain encrypted at rest; vectors never leave the secure boundary.</li>
            </ul>
            <div className="flex items-center gap-2 rounded-xl border border-success/40 bg-success/10 p-3 text-success">
              <Shield className="h-5 w-5" />
              <span>Privacy guardrails locked in. No silent writes occur.</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

const Data = ({ label, value }: { label: string; value: string }) => (
  <div>
    <p className="text-xs uppercase tracking-[0.3em] text-white/40">{label}</p>
    <p className="text-sm text-white">{value}</p>
  </div>
);
