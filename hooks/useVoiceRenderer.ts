import { useState, useCallback } from "react";
import { nanoid } from "nanoid/non-secure";
import { toast } from "sonner";

import { api } from "../api/client";
import type { RenderedAudio } from "../api/types";
import { useSession } from "./useSession";

export const useVoiceRenderer = () => {
  const { session } = useSession();
  const [render, setRender] = useState<RenderedAudio | null>(null);
  const [isRendering, setIsRendering] = useState(false);

  const renderVoice = useCallback(
    async (text: string, profile: string, dynamics: string) => {
      if (!session) throw new Error("Session must be active to render voice");
      setIsRendering(true);
      try {
        const response = await api.renderVoice(session.metadata.session_id, {
          session_id: session.metadata.session_id,
          render_id: `render_${nanoid(32)}`,
          text,
          voice_profile: profile,
          dynamics,
          format: "wav"
        });
        setRender(response);
        toast.success("Voice render complete");
      } catch (error) {
        toast.error(error instanceof Error ? error.message : "Voice rendering failed");
        throw error;
      } finally {
        setIsRendering(false);
      }
    },
    [session]
  );

  return { render, renderVoice, isRendering };
};
