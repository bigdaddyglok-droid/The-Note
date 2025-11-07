import { useCallback, useState } from "react";
import { nanoid } from "nanoid/non-secure";
import { toast } from "sonner";

import { api } from "../api/client";
import type { GenerationBundle } from "../api/types";
import { useSession } from "./useSession";

export const useGeneration = () => {
  const { session } = useSession();
  const [bundle, setBundle] = useState<GenerationBundle | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const generate = useCallback(
    async (prompt: string, modes: GenerationBundle["outputs"][number]["type"][]) => {
      if (!session) {
        throw new Error("Session must be active to generate content");
      }
      setIsGenerating(true);
      try {
        const requestId = `gen_${nanoid(32)}`;
        const response = await api.generate(session.metadata.session_id, {
          session_id: session.metadata.session_id,
          request_id: requestId,
          prompt,
          modes,
          emotional_goal: session.metadata.emotional_goal,
          tempo: session.metadata.tempo,
          key: session.metadata.key
        });
        setBundle(response);
        toast.success("Imagination engine synthesized new material");
      } catch (error) {
        toast.error(error instanceof Error ? error.message : "Creative generation failed");
        throw error;
      } finally {
        setIsGenerating(false);
      }
    },
    [session]
  );

  return { bundle, generate, isGenerating };
};
