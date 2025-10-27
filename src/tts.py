"""
TTS (Text-to-Speech) 모듈
텍스트 답변을 음성으로 변환
"""

from pathlib import Path
from gtts import gTTS

from config import TTS_LANGUAGE, TTS_SLOW, OUTPUT_DIR


class TextToSpeech:
    """TTS 변환 클래스"""

    def __init__(self, language: str = TTS_LANGUAGE, slow: bool = TTS_SLOW):
        """
        초기화

        Args:
            language: 언어 코드 (기본: 한국어 'ko')
            slow: 느린 속도 여부
        """
        self.language = language
        self.slow = slow
        print("[OK] TTS 모듈 초기화 완료")

    def text_to_speech(self, text: str, output_path: Path) -> Path:
        """
        텍스트를 음성 파일로 변환

        Args:
            text: 변환할 텍스트
            output_path: 저장할 파일 경로

        Returns:
            저장된 파일 경로
        """
        try:
            # gTTS 객체 생성
            tts = gTTS(text=text, lang=self.language, slow=self.slow)

            # 파일 저장
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            tts.save(str(output_path))

            print(f"[OK] 음성 파일 생성 완료: {output_path}")
            return output_path

        except Exception as e:
            print(f"[ERROR] TTS 변환 오류: {e}")
            raise

    def generate_answer_audio(self, text: str, filename: str = "answer") -> Path:
        """
        답변 텍스트를 음성 파일로 변환 (편의 메서드)

        Args:
            text: 답변 텍스트
            filename: 파일명 (확장자 제외)

        Returns:
            저장된 파일 경로
        """
        output_path = OUTPUT_DIR / f"{filename}.mp3"
        return self.text_to_speech(text, output_path)


def test_tts():
    """TTS 테스트 함수"""
    print("=== TTS 테스트 ===\n")

    tts = TextToSpeech()

    test_text = """
    안녕하세요. 당신의 고민을 듣게 되어 기쁩니다.
    모든 어려움은 시간이 지나면 해결될 수 있어요.
    지금 이 순간을 잘 견디고 계신 당신이 정말 대단합니다.
    항상 응원하겠습니다.
    """

    try:
        print("음성 변환 중...")
        output_file = tts.generate_answer_audio(test_text, "test_answer")
        print(f"\n[OK] 테스트 완료!")
        print(f"  파일 위치: {output_file}")
        print(f"  파일 크기: {output_file.stat().st_size} bytes")

    except Exception as e:
        print(f"[ERROR] 테스트 실패: {e}")


if __name__ == "__main__":
    test_tts()
