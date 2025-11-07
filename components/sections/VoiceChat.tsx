/**
 * Voice Chat - Real-Time Conversational Interface
 * Talk to The Note hands-free while making music
 */

import { useEffect, useRef, useState } from 'react';
import { Mic, MicOff, Volume2, VolumeX, Loader2 } from 'lucide-react';
import { toast } from 'sonner';

import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { useSession } from '../../hooks/useSession';
import { api } from '../../api/client';

interface VoiceMessage {
  role: 'user' | 'assistant';
  text: string;
  timestamp: Date;
}

interface SpeechRecognitionEvent extends Event {
  results: SpeechRecognitionResultList;
  resultIndex: number;
}

interface SpeechRecognitionErrorEvent extends Event {
  error: string;
}

interface SpeechRecognition extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  start: () => void;
  stop: () => void;
  abort: () => void;
  onresult: (event: SpeechRecognitionEvent) => void;
  onerror: (event: SpeechRecognitionErrorEvent) => void;
  onend: () => void;
}

declare global {
  interface Window {
    SpeechRecognition: new () => SpeechRecognition;
    webkitSpeechRecognition: new () => SpeechRecognition;
  }
}

export function VoiceChat() {
  const { session } = useSession();
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [currentTranscript, setCurrentTranscript] = useState('');
  const [messages, setMessages] = useState<VoiceMessage[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);

  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const synthRef = useRef<SpeechSynthesis | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Initialize speech recognition
  useEffect(() => {
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognition = new SpeechRecognition();

      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = 'en-US';

      recognition.onresult = (event: SpeechRecognitionEvent) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }

        setCurrentTranscript(interimTranscript || finalTranscript);

        // Process final transcript
        if (finalTranscript) {
          handleUserSpeech(finalTranscript);
          setCurrentTranscript('');
        }
      };

      recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
        console.error('Speech recognition error:', event.error);
        if (event.error === 'no-speech') {
          // Ignore no-speech errors
          return;
        }
        toast.error(`Speech recognition error: ${event.error}`);
      };

      recognition.onend = () => {
        if (isListening) {
          // Restart if still supposed to be listening
          try {
            recognition.start();
          } catch (e) {
            // Ignore error if already started
          }
        }
      };

      recognitionRef.current = recognition;
    }

    // Initialize speech synthesis
    if ('speechSynthesis' in window) {
      synthRef.current = window.speechSynthesis;
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.abort();
      }
      if (synthRef.current) {
        synthRef.current.cancel();
      }
    };
  }, [isListening]);

  // Auto-scroll messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleUserSpeech = async (transcript: string) => {
    if (!session) {
      toast.error('Start a session first');
      return;
    }

    if (!transcript.trim()) return;

    // Add user message
    const userMessage: VoiceMessage = {
      role: 'user',
      text: transcript,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);

    // Process with backend
    setIsProcessing(true);
    try {
      const response = await api.voiceChat({
        session_id: session.metadata.session_id,
        transcript: transcript,
        audio_features: null
      });

      // Add assistant message
      const assistantMessage: VoiceMessage = {
        role: 'assistant',
        text: response.response,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);

      // Speak response
      if (synthRef.current) {
        speakText(response.response);
      }

    } catch (error) {
      console.error('Voice chat error:', error);
      toast.error('Failed to process speech');
    } finally {
      setIsProcessing(false);
    }
  };

  const speakText = (text: string) => {
    if (!synthRef.current) return;

    // Cancel any ongoing speech
    synthRef.current.cancel();

    const utterance = new SpeechSynthesisUtterance(text);

    // Find a good voice (prefer female, neural, or enhanced)
    const voices = synthRef.current.getVoices();
    const preferredVoice = voices.find(voice =>
      voice.name.includes('Google') ||
      voice.name.includes('Female') ||
      voice.name.includes('Samantha')
    ) || voices[0];

    if (preferredVoice) {
      utterance.voice = preferredVoice;
    }

    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    synthRef.current.speak(utterance);
  };

  const toggleListening = () => {
    if (!session) {
      toast.error('Start a session first');
      return;
    }

    if (!recognitionRef.current) {
      toast.error('Speech recognition not supported in this browser');
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
      toast.info('Stopped listening');
    } else {
      try {
        recognitionRef.current.start();
        setIsListening(true);
        toast.success('Listening... speak naturally');
      } catch (error) {
        console.error('Failed to start recognition:', error);
        toast.error('Failed to start listening');
      }
    }
  };

  const toggleSpeaking = () => {
    if (!synthRef.current) return;

    if (isSpeaking) {
      synthRef.current.cancel();
      setIsSpeaking(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Voice Chat</h1>
          <p className="text-white/70 mt-2">
            Talk to The Note hands-free. Create music while I listen and respond.
          </p>
        </div>

        <div className="flex gap-3">
          <Button
            onClick={toggleListening}
            variant={isListening ? "primary" : "secondary"}
            className={isListening ? "animate-pulse" : ""}
          >
            {isListening ? <Mic className="h-5 w-5" /> : <MicOff className="h-5 w-5" />}
            {isListening ? 'Listening...' : 'Start Listening'}
          </Button>

          <Button
            onClick={toggleSpeaking}
            variant={isSpeaking ? "primary" : "secondary"}
            disabled={!isSpeaking}
          >
            {isSpeaking ? <Volume2 className="h-5 w-5" /> : <VolumeX className="h-5 w-5" />}
            {isSpeaking ? 'Speaking...' : 'Muted'}
          </Button>
        </div>
      </div>

      {/* Live Transcript */}
      {currentTranscript && (
        <Card className="border-2 border-blue-500/50">
          <div className="flex items-center gap-3">
            <Mic className="h-4 w-4 text-blue-400 animate-pulse" />
            <p className="text-white/80 italic">{currentTranscript}</p>
          </div>
        </Card>
      )}

      {/* Chat Messages */}
      <Card className="h-[500px] flex flex-col">
        <div className="flex-1 overflow-y-auto space-y-4 p-4">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center space-y-4">
              <div className="text-6xl">🎤</div>
              <div className="space-y-2">
                <p className="text-white font-medium">Ready for conversation</p>
                <p className="text-white/60 text-sm max-w-md">
                  Click "Start Listening" and speak naturally. I'll understand your intent and
                  respond using the consciousness network.
                </p>
              </div>
              <div className="text-xs text-white/40 space-y-1">
                <p>Try saying:</p>
                <p>"Create uplifting lyrics about the ocean"</p>
                <p>"Generate a melody in C major"</p>
                <p>"Analyze what I'm playing"</p>
              </div>
            </div>
          ) : (
            <>
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[70%] rounded-lg p-4 ${
                      message.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-white/10 text-white'
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{message.text}</p>
                    <p className="text-xs opacity-60 mt-2">
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))}

              {isProcessing && (
                <div className="flex justify-start">
                  <div className="bg-white/10 rounded-lg p-4 flex items-center gap-2">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    <p className="text-white/60">Thinking...</p>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </>
          )}
        </div>
      </Card>

      {/* Status Bar */}
      <Card>
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${isListening ? 'bg-green-500 animate-pulse' : 'bg-gray-500'}`} />
              <span className="text-white/60">
                {isListening ? 'Listening' : 'Not listening'}
              </span>
            </div>

            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${isSpeaking ? 'bg-blue-500 animate-pulse' : 'bg-gray-500'}`} />
              <span className="text-white/60">
                {isSpeaking ? 'Speaking' : 'Silent'}
              </span>
            </div>
          </div>

          <div className="text-white/40">
            {messages.length} messages
          </div>
        </div>
      </Card>

      {/* Quick Tips */}
      <Card className="bg-white/5">
        <div className="space-y-2">
          <p className="text-white/80 font-medium">💡 Tips for best results:</p>
          <ul className="text-sm text-white/60 space-y-1 list-disc list-inside">
            <li>Speak clearly and naturally</li>
            <li>Be specific about mood, key, or tempo</li>
            <li>Say "help" to learn what I can do</li>
            <li>Use hands-free mode while playing instruments</li>
            <li>I remember our conversation context</li>
          </ul>
        </div>
      </Card>
    </div>
  );
}
