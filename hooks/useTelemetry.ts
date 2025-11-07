import { useQuery } from "@tanstack/react-query";

import { api } from "../api/client";

export const useTelemetry = () =>
  useQuery({
    queryKey: ["telemetry"],
    queryFn: () => api.getTelemetry(),
    refetchInterval: 5000,
  });
