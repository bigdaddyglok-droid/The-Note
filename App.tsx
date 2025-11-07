import { Navigate, Route, Routes } from "react-router-dom";

import { DashboardLayout } from "./components/layout/DashboardLayout";
import { SessionOverview } from "./components/sections/SessionOverview";
import { AudioPipeline } from "./components/sections/AudioPipeline";
import { LyricIntelligence } from "./components/sections/LyricIntelligence";
import { CreativeImagination } from "./components/sections/CreativeImagination";
import { VoicePerformance } from "./components/sections/VoicePerformance";
import { MemoryInsights } from "./components/sections/MemoryInsights";
import { VoiceChat } from "./components/sections/VoiceChat";

const App = () => (
  <DashboardLayout>
    <Routes>
      <Route path="/" element={<Navigate to="/session" replace />} />
      <Route path="/session" element={<SessionOverview />} />
      <Route path="/audio" element={<AudioPipeline />} />
      <Route path="/lyrics" element={<LyricIntelligence />} />
      <Route path="/create" element={<CreativeImagination />} />
      <Route path="/voice" element={<VoicePerformance />} />
      <Route path="/chat" element={<VoiceChat />} />
      <Route path="/memory" element={<MemoryInsights />} />
    </Routes>
  </DashboardLayout>
);

export default App;
