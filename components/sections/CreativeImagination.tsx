import { useEffect, useMemo, useState } from "react";
import { Sparkles, Music3, Network, Lightbulb } from "lucide-react";
import { toast } from "sonner";

import { useGeneration } from "../../hooks/useGeneration";
import { useSession } from "../../hooks/useSession";
import type { GeneratedItem } from "../../api/types";
import { Button } from "../ui/Button";
import { Card } from "../ui/Card";
import { Textarea } from "../ui/Textarea";

const modeLabels: Record<GeneratedItem["type"], string> = {
  lyric: "Lyric",
  melody: "Melody",
  metaphor: "Metaphor",
  structure: "Structure"
};

export const CreativeImagination = () => {
  const { session } = useSession();
  const { bundle, generate, isGenerating } = useGeneration();
  const [prompt, setPrompt] = useState("Ignite the skyline with electric auroras.");
  const [selectedModes, setSelectedModes] = useState<GeneratedItem["type"][]>([
    "lyric",
    "melody",
    "metaphor"
  ]);

  const toggleMode = (mode: GeneratedItem["type"]) => {
    setSelectedModes((prev) =>
      prev.includes(mode) ? prev.filter((item) => item !== mode) : [...prev, mode]
    );
  };

  const triggerGeneration = () => {
    void (async () => {
      try {
        await generate(prompt, selectedModes);
      } catch (error) {
        toast.error(error instanceof Error ? error.message : "Imagination failure");
      }
    })();
  };

  useEffect(() => {
    if (!session) {
      setSelectedModes(["lyric", "melody", "metaphor"]);
    }
  }, [session]);

  const groupedOutputs = useMemo(() => {
    if (!bundle) return null;
    return bundle.outputs.reduce<Record<string, GeneratedItem>>((acc, item) => {
      acc[item.type] = item;
      return acc;
    }, {});
  }, [bundle]);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-white">Imagination Engine</h1>
      <p className="text-white/70 max-w-3xl">
        Blend metaphor, melodic geometry, and narrative arcs. The Imagination Engine translates
        prompts into multi-modal assets, tuned to the session&apos;s tempo, key, and emotional axis.
      </p>

      <div className="grid grid-cols-2 gap-6">
        <Card
          title="Prompt Canvas"
          description="Direct the creative engine with vivid intent. Modes can be toggled as needed."
          actions={
            <Button onClick={triggerGeneration} loading={isGenerating} disabled={!session}>
              <Sparkles className="h-4 w-4" />
              Generate
            </Button>
          }
        >
          <Textarea
            value={prompt}
            onChange={(event) => setPrompt(event.target.value)}
            disabled={!session}
            className="min-h-[200px]"
          />
          <div className="flex flex-wrap gap-2">
            {(["lyric", "melody", "metaphor", "structure"] as GeneratedItem["type"][]).map((mode) => {
              const active = selectedModes.includes(mode);
              return (
                <button
                  key={mode}
                  type="button"
                  onClick={() => toggleMode(mode)}
                  className={`rounded-full px-3 py-1 text-xs transition ${
                    active ? "bg-accent/20 text-accent" : "bg-white/10 text-white/60"
                  }`}
                >
                  {modeLabels[mode]}
                </button>
              );
            })}
          </div>
        </Card>

        <Card
          title="Output Gallery"
          description="Generated assets stream here with confidence scores and payload detail."
        >
          {groupedOutputs ? (
            <div className="space-y-4 text-sm">
              {Object.values(groupedOutputs).map((item) => (
                <div key={item.type} className="rounded-lg border border-white/10 p-4 space-y-3">
                  <header className="flex items-center justify-between">
                    <div className="flex items-center gap-2 text-white">
                      <ModeIcon mode={item.type} />
                      <span className="font-semibold uppercase tracking-[0.3em]">
                        {modeLabels[item.type]}
                      </span>
                    </div>
                    <span className="text-xs text-white/60">
                      Confidence {(item.confidence * 100).toFixed(1)}%
                    </span>
                  </header>
                  <pre className="whitespace-pre-wrap text-sm text-white/80 font-sans">
                    {JSON.stringify(item.payload, null, 2)}
                  </pre>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-white/50">
              Trigger the imagination engine to view generated assets across modalities.
            </p>
          )}
        </Card>
      </div>
    </div>
  );
};

const ModeIcon = ({ mode }: { mode: GeneratedItem["type"] }) => {
  switch (mode) {
    case "lyric":
      return <Lightbulb className="h-4 w-4 text-accent" />;
    case "melody":
      return <Music3 className="h-4 w-4 text-accent" />;
    case "metaphor":
      return <Network className="h-4 w-4 text-accent" />;
    case "structure":
      return <Sparkles className="h-4 w-4 text-accent" />;
    default:
      return null;
  }
};
