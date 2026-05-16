"""
ASR Service
Automatic Speech Recognition with speaker diarization and emotion detection.
Uses Antigravity for real-time transcription and enterprise audio processing.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import timedelta

from backend.python.utils.logger import get_logger
from backend.python.antigravity_client import AntigravityClient

logger = get_logger(__name__)


@dataclass
class TranscriptSegment:
    text: str
    start_time: float
    end_time: float
    speaker_id: Optional[str]
    confidence: float
    emotion: Optional[str] = None
    is_overlap: bool = False


@dataclass
class ASRResult:
    full_text: str
    segments: List[TranscriptSegment]
    language: str
    duration_seconds: float
    speaker_count: int
    word_count: int
    avg_confidence: float
    emotions_timeline: List[Dict[str, Any]] = field(default_factory=list)


class ASRService:
    """
    Advanced ASR with speaker diarization and emotional analysis.
    Integrates with Antigravity for noise-robust transcription.
    """

    def __init__(self, antigravity_client: Optional[AntigravityClient] = None):
        self.ag = antigravity_client or AntigravityClient()
        logger.info("ASRService initialized")

    async def transcribe(
        self,
        audio_bytes: bytes,
        options: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> ASRResult:
        """
        Agentic transcription pipeline:
        1. Audio preprocessing → 2. Speech detection → 3. Recognition →
        4. Speaker diarization → 5. Emotion analysis → 6. Post-processing
        """
        options = options or {}
        context = context or {}
        
        try:
            # Step 1: Preprocess audio
            preprocessed = await self._preprocess_audio(audio_bytes, options)
            
            # Step 2-3: Transcribe via Antigravity
            raw_transcript = await self.ag.audio.transcribe(preprocessed, {
                "language": options.get("language", "auto"),
                "model": "whisper-large-v3"
            })
            
            # Step 4: Speaker diarization
            diarized = await self._diarize_speakers(preprocessed, raw_transcript)
            
            # Step 5: Emotion analysis
            emotions = await self._analyze_emotions(preprocessed, diarized)
            
            # Step 6: Post-process
            result = self._assemble_result(diarized, emotions, raw_transcript)
            
            logger.info(
                f"Transcription complete: {result.word_count} words, "
                f"{result.speaker_count} speakers"
            )
            return result

        except Exception as e:
            logger.error(f"ASR failed: {e}")
            raise ASRServiceError(f"Transcription failed: {e}") from e

    async def _preprocess_audio(
        self, audio_bytes: bytes, options: Dict
    ) -> bytes:
        """Audio preprocessing: normalization, noise reduction."""
        # In production: use librosa, noisereduce
        return audio_bytes

    async def _diarize_speakers(
        self, audio: bytes, transcript: Dict
    ) -> List[TranscriptSegment]:
        """Identify different speakers in audio."""
        try:
            diarization = await self.ag.audio.diarize(audio)
            segments = []
            for seg in diarization.get("segments", []):
                segments.append(TranscriptSegment(
                    text=seg.get("text", ""),
                    start_time=seg.get("start", 0),
                    end_time=seg.get("end", 0),
                    speaker_id=seg.get("speaker", "unknown"),
                    confidence=seg.get("confidence", 0.9)
                ))
            return segments
        except Exception:
            # Fallback: single speaker
            return [
                TranscriptSegment(
                    text=transcript.get("text", ""),
                    start_time=0,
                    end_time=transcript.get("duration", 0),
                    speaker_id="speaker_0",
                    confidence=transcript.get("confidence", 0.9)
                )
            ]

    async def _analyze_emotions(
        self, audio: bytes, segments: List[TranscriptSegment]
    ) -> List[Dict[str, Any]]:
        """Analyze emotional content per segment."""
        emotions = []
        for seg in segments:
            try:
                emotion = await self.ag.audio.detect_emotion(
                    audio,
                    start=seg.start_time,
                    end=seg.end_time
                )
                seg.emotion = emotion.get("primary_emotion", "neutral")
                emotions.append({
                    "time": seg.start_time,
                    "emotion": seg.emotion,
                    "intensity": emotion.get("intensity", 0.5)
                })
            except Exception:
                seg.emotion = "neutral"
        return emotions

    def _assemble_result(
        self,
        segments: List[TranscriptSegment],
        emotions: List[Dict],
        raw: Dict
    ) -> ASRResult:
        """Assemble final ASR result."""
        full_text = " ".join(s.text for s in segments)
        speakers = set(s.speaker_id for s in segments if s.speaker_id)
        
        return ASRResult(
            full_text=full_text,
            segments=segments,
            language=raw.get("language", "unknown"),
            duration_seconds=raw.get("duration", 0),
            speaker_count=len(speakers),
            word_count=len(full_text.split()),
            avg_confidence=sum(s.confidence for s in segments) / max(len(segments), 1),
            emotions_timeline=emotions
        )

    async def transcribe_stream(
        self,
        audio_stream: Any,  # Async generator of audio chunks
        options: Optional[Dict] = None,
        context: Optional[Dict] = None,
    ):
        """Real-time streaming transcription."""
        buffer = []
        async for chunk in audio_stream:
            buffer.append(chunk)
            if len(buffer) >= 10:  # Process every 10 chunks
                audio = b"".join(buffer)
                result = await self.transcribe(audio, options, context)
                yield result
                buffer = []


class ASRServiceError(Exception):
    pass