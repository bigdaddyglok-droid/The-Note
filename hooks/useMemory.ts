import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useSession } from "./useSession";
import { api } from "../api/client";
import type { MemoryRecord } from "../api/types";

export const useMemory = () => {
  const { session } = useSession();
  const queryClient = useQueryClient();

  const query = useQuery({
    queryKey: ["memory", session?.metadata.user_id],
    enabled: Boolean(session?.metadata.user_id),
    queryFn: () =>
      session ? api.getLatestMemory(session.metadata.user_id) : Promise.resolve(null),
    staleTime: 60_000
  });

  const refresh = () => {
    if (session?.metadata.user_id) {
      void queryClient.invalidateQueries({ queryKey: ["memory", session.metadata.user_id] });
    }
  };

  return { ...query, refresh, record: query.data as MemoryRecord | null };
};
