import { useCallback, useEffect, useRef, useState } from "react";
import { toast } from "sonner";

import { useSession } from "./useSession";

export const useLiveAudioCapture = () => {
  const { session, pushAudioFrame } = useSession();
  const [isCapturing, setIsCapturing] = useState(false);
  const audioContextRef = useRef<AudioContext | null>(null);
  const processorRef = useRef<ScriptProcessorNode | null>(null);
  const sourceRef = useRef<MediaStreamAudioSourceNode | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const stopCapture = useCallback(() => {
    processorRef.current?.disconnect();
    sourceRef.current?.disconnect();
    audioContextRef.current?.close().catch(() => undefined);
    streamRef.current?.getTracks().forEach((track) => track.stop());
    audioContextRef.current = null;
    processorRef.current = null;
    sourceRef.current = null;
    streamRef.current = null;
    setIsCapturing(false);
  }, []);

  const startCapture = useCallback(async () => {
    if (!session) {
      toast.error("Session must be active before capturing audio.");
      return;
    }
    if (isCapturing) {
      return;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
      const context = new AudioContext({ sampleRate: 22_050 });
      const source = context.createMediaStreamSource(stream);
      const processor = context.createScriptProcessor(4096, 1, 1);

      processor.onaudioprocess = (event: AudioProcessingEvent) => {
        const input = event.inputBuffer.getChannelData(0);
        const copy = new Float32Array(input.length);
        copy.set(input);
        void pushAudioFrame(copy, context.sampleRate).catch((error) => {
          console.error("Failed to push live audio frame", error);
          toast.error("Live audio frame could not be ingested.");
        });
      };

      source.connect(processor);
      processor.connect(context.destination);

      audioContextRef.current = context;
      processorRef.current = processor;
      sourceRef.current = source;
      streamRef.current = stream;
      setIsCapturing(true);
      toast.success("Live capture started");
    } catch (error) {
      console.error("Failed to start live capture", error);
      toast.error("Unable to access microphone.");
      stopCapture();
    }
  }, [session, isCapturing, pushAudioFrame, stopCapture]);

  useEffect(() => {
    if (!session?.active && isCapturing) {
      stopCapture();
    }
  }, [session, isCapturing, stopCapture]);
  return { isCapturing, startCapture, stopCapture };
};
