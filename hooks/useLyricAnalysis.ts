import { useState, useCallback } from "react";
import { nanoid } from "nanoid/non-secure";
import { toast } from "sonner";

import { api } from "../api/client";
import type { LyricInsight } from "../api/types";
import { useSession } from "./useSession";

export const useLyricAnalysis = () => {
  const { session } = useSession();
  const [insight, setInsight] = useState<LyricInsight | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const analyze = useCallback(
    async (text: string) => {
      if (!session) {
        throw new Error("Session must be active before analyzing lyrics");
      }
      setIsLoading(true);
      try {
        const result = await api.analyzeLyrics(session.metadata.session_id, {
          session_id: session.metadata.session_id,
          section_id: `section_${nanoid(6)}`,
          text
        });
        setInsight(result);
      } catch (error) {
        toast.error(error instanceof Error ? error.message : "Lyric analysis failed");
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    [session]
  );

  return { insight, analyze, isLoading };
};
