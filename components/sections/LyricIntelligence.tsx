import { useState } from "react";
import { BookOpen, Sparkles } from "lucide-react";
import { toast } from "sonner";

import { useLyricAnalysis } from "../../hooks/useLyricAnalysis";
import { useSession } from "../../hooks/useSession";
import { Button } from "../ui/Button";
import { Card } from "../ui/Card";
import { Textarea } from "../ui/Textarea";

export const LyricIntelligence = () => {
  const { session } = useSession();
  const { insight, analyze, isLoading } = useLyricAnalysis();
  const [input, setInput] = useState(
    "Shadows bloom beneath the neon tide\nSignals breathe electric lullabies"
  );

  const handleAnalysis = () => {
    void (async () => {
      try {
        await analyze(input);
      } catch (error) {
        toast.error(error instanceof Error ? error.message : "Lyric analysis failed");
      }
    })();
  };

  const hasSession = Boolean(session);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-white">Language + Lyric Intelligence</h1>
      <p className="text-white/70 max-w-3xl">
        Here we map phonetics, stress, rhyme lattices, and metaphor density. Feed the system a
        lyrical fragment to receive IPA decoding, grammar flags, and semantic anchors for the
        Imagination Engine.
      </p>

      <div className="grid grid-cols-2 gap-6">
        <Card
          title="Submit Lyrical Passage"
          description="The module performs IPA rendering, stress contouring, and rhyme extraction."
          actions={
            <Button onClick={handleAnalysis} loading={isLoading} disabled={!hasSession}>
              <Sparkles className="h-4 w-4" />
              Analyze
            </Button>
          }
        >
          <Textarea
            value={input}
            onChange={(event) => setInput(event.target.value)}
            disabled={!hasSession}
            placeholder="Flow lines, metaphors, or raw drafts to refine..."
            className="min-h-[240px]"
          />
          {!hasSession && (
            <p className="text-sm text-white/50">
              Activate a session to contextualize linguistic analysis.
            </p>
          )}
        </Card>

        <Card
          title="Insight Matrix"
          description="Detailed breakdown of syllables, stresses, and vocabulary highlights."
        >
          {insight ? (
            <div className="space-y-4 text-sm">
              {insight.lines.map((line) => (
                <div key={line.original} className="rounded-xl border border-white/10 p-3">
                  <p className="font-medium text-white">{line.original}</p>
                  <p className="text-xs text-white/50 mt-1">IPA: {line.ipa.join(" ")}</p>
                  <p className="text-xs text-accent mt-1">Rhyme key: {line.rhyme_key}</p>
                  <div className="mt-2 flex flex-wrap gap-2 text-[11px] text-white/70">
                    {line.syllables.map((syllable) => (
                      <span
                        key={`${syllable.text}-${syllable.stress}`}
                        className="rounded bg-white/10 px-2 py-1"
                      >
                        {syllable.text} <span className="text-accent">({syllable.stress})</span>
                      </span>
                    ))}
                  </div>
                </div>
              ))}
              {insight.grammar_notes.length > 0 && (
                <div className="rounded-xl bg-warning/20 p-3 text-warning text-sm space-y-1">
                  <p className="uppercase tracking-[0.3em] text-xs">Grammar Signals</p>
                  {insight.grammar_notes.map((note) => (
                    <p key={note}>{note}</p>
                  ))}
                </div>
              )}
              <div>
                <p className="uppercase tracking-[0.3em] text-xs text-white/40">Suggested Terms</p>
                <div className="mt-2 flex flex-wrap gap-2">
                  {insight.term_suggestions.map((term) => (
                    <span key={term} className="rounded-full bg-accent/20 px-2 py-1 text-xs text-accent">
                      {term}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="flex items-center gap-3 text-white/50">
              <BookOpen className="h-5 w-5" />
              <span>Insights will render here after analysis completes.</span>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};
