import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "sonner";
import { BrowserRouter } from "react-router-dom";

import App from "./App";
import { SessionProvider } from "./context/SessionContext";
import "./styles/tailwind.css";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 30_000
    }
  }
});

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <SessionProvider>
          <App />
          <Toaster richColors position="bottom-right" />
        </SessionProvider>
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>
);
