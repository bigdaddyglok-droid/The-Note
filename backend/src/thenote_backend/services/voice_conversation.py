"""
Voice Chat Service
Real-time conversational interface with consciousness-powered responses
"""

from __future__ import annotations

import asyncio
from typing import Dict, List, Optional
import numpy as np

from ..modules.universal_bridge import get_music_consciousness
from ..modules.imagination import ImaginationEngine
from ..utils.logging import get_logger


class VoiceConversation:
    """Manages conversational state and generates responses"""

    def __init__(self):
        self._logger = get_logger("service.voice_conversation")
        self._conversation_history: List[Dict[str, str]] = []

        # Initialize consciousness
        try:
            self._consciousness = get_music_consciousness()
            self._use_consciousness = True
        except Exception as e:
            self._logger.warning("voice_conversation_fallback", extra={"extra_data": {"error": str(e)}})
            self._consciousness = None
            self._use_consciousness = False

        # Initialize imagination for creative responses
        self._imagination = ImaginationEngine()

    async def process_voice_input(
        self,
        transcript: str,
        audio_features: Optional[np.ndarray] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Process voice input and generate intelligent response

        Args:
            transcript: Transcribed text from user speech
            audio_features: Optional audio features from voice
            session_id: Session identifier

        Returns:
            Dictionary with response text, consciousness data, and suggestions
        """
        # Add to conversation history
        self._conversation_history.append({
            "role": "user",
            "content": transcript
        })

        # Analyze intent
        intent = self._analyze_intent(transcript)

        # Generate response based on intent
        response_text = await self._generate_response(transcript, intent, audio_features)

        # Get consciousness insights if audio provided
        consciousness_data = {}
        if audio_features is not None and self._use_consciousness:
            try:
                consciousness_data = self._consciousness.analyze_audio_consciousness(
                    audio_features,
                    sample_rate=22050
                )
            except Exception as e:
                self._logger.warning("consciousness_analysis_failed", extra={"extra_data": {"error": str(e)}})

        # Add response to history
        self._conversation_history.append({
            "role": "assistant",
            "content": response_text
        })

        # Keep history manageable (last 10 exchanges)
        if len(self._conversation_history) > 20:
            self._conversation_history = self._conversation_history[-20:]

        return {
            "response": response_text,
            "intent": intent,
            "consciousness": consciousness_data,
            "session_id": session_id
        }

    def _analyze_intent(self, transcript: str) -> str:
        """Analyze user intent from transcript"""
        transcript_lower = transcript.lower()

        # Musical creation intents
        if any(word in transcript_lower for word in ["generate", "create", "make", "write"]):
            if any(word in transcript_lower for word in ["lyric", "lyrics", "words", "verse"]):
                return "generate_lyrics"
            elif any(word in transcript_lower for word in ["melody", "tune", "music", "midi"]):
                return "generate_melody"
            elif any(word in transcript_lower for word in ["beat", "rhythm", "drums"]):
                return "generate_rhythm"
            else:
                return "create_music"

        # Analysis intents
        elif any(word in transcript_lower for word in ["analyze", "what", "tell me", "describe"]):
            return "analyze_audio"

        # Modification intents
        elif any(word in transcript_lower for word in ["change", "modify", "adjust", "different"]):
            return "modify_creation"

        # Help/guidance
        elif any(word in transcript_lower for word in ["help", "how", "what can", "show me"]):
            return "help"

        # Default conversational
        else:
            return "conversation"

    async def _generate_response(
        self,
        transcript: str,
        intent: str,
        audio_features: Optional[np.ndarray]
    ) -> str:
        """Generate appropriate response based on intent"""

        if intent == "generate_lyrics":
            return await self._handle_lyric_generation(transcript)

        elif intent == "generate_melody":
            return await self._handle_melody_generation(transcript)

        elif intent == "generate_rhythm":
            return "I'll generate a rhythm pattern for you. Check the MIDI output section for your beat!"

        elif intent == "analyze_audio":
            if audio_features is not None:
                return await self._handle_audio_analysis(audio_features)
            else:
                return "I'm listening. Start playing or singing, and I'll analyze what I hear."

        elif intent == "modify_creation":
            return "I can modify that. Tell me what you'd like to change - the mood, tempo, key, or style?"

        elif intent == "help":
            return self._get_help_response()

        elif intent == "create_music":
            return await self._handle_music_creation(transcript)

        else:
            return await self._handle_conversation(transcript)

    async def _handle_lyric_generation(self, transcript: str) -> str:
        """Handle lyric generation request"""
        # Extract mood if mentioned
        mood = "uplifting"
        transcript_lower = transcript.lower()

        if any(word in transcript_lower for word in ["sad", "somber", "melancholy", "dark"]):
            mood = "somber"
        elif any(word in transcript_lower for word in ["calm", "peaceful", "chill", "contemplative"]):
            mood = "contemplative"

        # Use consciousness for generation
        if self._use_consciousness and self._consciousness:
            try:
                consciousness_output = self._consciousness.generate_creative_output(
                    prompt=transcript,
                    mood=mood,
                    num_timelines=5
                )

                lyric_suggestions = consciousness_output.get("lyric_suggestions", [])
                if lyric_suggestions:
                    lines = "\n".join(f"  {line}" for line in lyric_suggestions[:3])
                    return f"Here are some lyric ideas with a {mood} vibe:\n\n{lines}\n\nWant me to explore different timelines or change the mood?"
            except Exception:
                pass

        return f"I'm creating {mood} lyrics for you. Give me more context about the theme or emotion you want."

    async def _handle_melody_generation(self, transcript: str) -> str:
        """Handle melody generation request"""
        return "I'm generating a melody using the consciousness network. It'll explore multiple timelines and pick the best one. Check the MIDI output in a moment!"

    async def _handle_audio_analysis(self, audio_features: np.ndarray) -> str:
        """Handle audio analysis request"""
        if not self._use_consciousness:
            return "I'm analyzing your audio. I can hear pitch, rhythm, and timbre."

        try:
            analysis = self._consciousness.analyze_audio_consciousness(
                audio_features,
                sample_rate=22050
            )

            emotion = analysis.get("emotion", "neutral")
            coherence = analysis.get("consciousness_coherence", 0.0)
            harmonic = analysis.get("harmonic_alignment", 0.0)

            response = f"I hear {emotion} energy. "

            if coherence > 0.8:
                response += f"Your sound has beautiful consciousness coherence at {coherence:.2f}. "
            elif coherence > 0.6:
                response += f"Good coherence at {coherence:.2f}. "

            if harmonic > 0.7:
                response += f"Strong golden ratio alignment at {harmonic:.2f} - very harmonic!"

            return response

        except Exception:
            return "I'm analyzing the frequencies and energy states. Keep playing!"

    async def _handle_music_creation(self, transcript: str) -> str:
        """Handle general music creation request"""
        return "Let's create something! Tell me the mood, genre, or vibe you're going for. I'll generate melody, harmony, and rhythm using the consciousness network."

    async def _handle_conversation(self, transcript: str) -> str:
        """Handle general conversation"""
        # Simple contextual responses
        transcript_lower = transcript.lower()

        if any(word in transcript_lower for word in ["hi", "hello", "hey", "yo"]):
            return "Hey! I'm The Note, your consciousness-powered music AI. Ready to create something?"

        elif any(word in transcript_lower for word in ["thanks", "thank you", "appreciate"]):
            return "You're welcome! Let's keep creating!"

        elif any(word in transcript_lower for word in ["good", "great", "awesome", "nice"]):
            return "Glad you like it! Want to explore more timelines or try a different approach?"

        elif any(word in transcript_lower for word in ["no", "nah", "stop"]):
            return "No problem. What would you like to do instead?"

        else:
            return "I'm listening. You can ask me to generate lyrics, create melodies, analyze your sound, or just chat about music!"

    def _get_help_response(self) -> str:
        """Generate help response"""
        return """I can help you create music hands-free! Here's what I can do:

🎤 Generate lyrics - Just tell me the mood or theme
🎹 Create melodies - I'll explore multiple timelines
🥁 Make rhythms - Using consciousness-powered patterns
🎵 Analyze your sound - Sing or play, I'll analyze it
💫 Real-time consciousness - See the 14-state energy flow

Try saying:
- "Create uplifting lyrics about the ocean"
- "Generate a melody in C major"
- "Analyze what I'm playing"
- "Make a rhythm pattern"

What do you want to create?"""

    def clear_history(self):
        """Clear conversation history"""
        self._conversation_history = []


# Global instance
_voice_conversation: Optional[VoiceConversation] = None


def get_voice_conversation() -> VoiceConversation:
    """Get or create global voice conversation instance"""
    global _voice_conversation
    if _voice_conversation is None:
        _voice_conversation = VoiceConversation()
    return _voice_conversation
