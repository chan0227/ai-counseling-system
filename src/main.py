"""
AI 고민상담 자동 답변 시스템 - 메인 실행 파일
"""

import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Optional

# colorama로 콘솔 색상 지원
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    # colorama가 없으면 더미 객체 사용
    class Fore:
        RED = GREEN = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ""

    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""

from config import validate_config, OUTPUT_DIR
from matcher import AnswerMatcher
from generator import AnswerGenerator
from tts import TextToSpeech


def remove_emojis(text: str) -> str:
    """이모지 및 특수문자 제거 (Windows 콘솔 호환성)"""
    # 이모지 패턴 제거
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # 얼굴 이모지
        "\U0001F300-\U0001F5FF"  # 기호 및 픽토그램
        "\U0001F680-\U0001F6FF"  # 교통 및 지도
        "\U0001F700-\U0001F77F"  # 알케미 기호
        "\U0001F780-\U0001F7FF"  # 기하학적 도형
        "\U0001F800-\U0001F8FF"  # 화살표
        "\U0001F900-\U0001F9FF"  # 추가 기호
        "\U0001FA00-\U0001FA6F"  # 체스 기호
        "\U0001FA70-\U0001FAFF"  # 기호 및 픽토그램 확장
        "\U00002702-\U000027B0"  # 딩뱃
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)


class CounselingSystem:
    """고민상담 자동 답변 시스템"""

    def __init__(self):
        """초기화"""
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}AI 고민상담 자동 답변 시스템 MVP")
        print(f"{Fore.CYAN}{'='*60}\n")

        try:
            # 설정 검증
            validate_config()

            # 각 모듈 초기화
            print(f"{Fore.YELLOW}시스템 초기화 중...\n")
            self.matcher = AnswerMatcher()
            self.generator = AnswerGenerator()
            self.tts = TextToSpeech()

            print(f"\n{Fore.GREEN}[OK] 시스템 초기화 완료!\n")

        except Exception as e:
            print(f"{Fore.RED}[ERROR] 초기화 오류: {e}")
            sys.exit(1)

    def process_question(self, question: str, enable_tts: bool = True) -> Optional[str]:
        """
        질문을 처리하여 답변 생성

        Args:
            question: 사용자 질문
            enable_tts: TTS 활성화 여부

        Returns:
            생성된 답변 텍스트
        """
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}질문 처리 시작")
        print(f"{Fore.CYAN}{'='*60}\n")

        try:
            # 1. 유사 답변 검색
            print(f"{Fore.YELLOW}[1/4] 유사한 답변 검색 중...")
            matches = self.matcher.find_best_matches(question)

            if matches:
                print(f"{Fore.GREEN}[OK] {len(matches)}개의 유사 답변을 찾았습니다.")
                for i, (answer, score) in enumerate(matches, 1):
                    print(f"  {i}. [{answer['category']}] {answer['title']} ({score:.1%})")
            else:
                print(f"{Fore.YELLOW}! 유사한 답변을 찾지 못했습니다. 일반 답변을 생성합니다.")

            # 2. Claude API로 답변 생성
            print(f"\n{Fore.YELLOW}[2/4] AI 답변 생성 중...")
            if matches:
                answer_text = self.generator.generate_answer(question, matches)
            else:
                answer_text = self.generator.generate_simple_answer(question)

            print(f"{Fore.GREEN}[OK] 답변 생성 완료")

            # 3. 답변 출력 (이모지 제거)
            clean_answer = remove_emojis(answer_text)
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"{Fore.CYAN}생성된 답변")
            print(f"{Fore.CYAN}{'='*60}\n")
            print(f"{Fore.WHITE}{clean_answer}\n")
            print(f"{Fore.CYAN}{'='*60}\n")

            # 4. 답변 저장
            print(f"{Fore.YELLOW}[3/4] 답변 저장 중...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            text_path = OUTPUT_DIR / f"answer_{timestamp}.txt"

            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(f"질문: {question}\n\n")
                f.write(f"답변:\n{answer_text}\n\n")
                f.write(f"생성 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

            print(f"{Fore.GREEN}[OK] 텍스트 파일 저장: {text_path}")

            # 5. TTS 변환 (선택적)
            if enable_tts:
                print(f"\n{Fore.YELLOW}[4/4] 음성 변환 중...")
                audio_path = self.tts.generate_answer_audio(answer_text, f"answer_{timestamp}")
                print(f"{Fore.GREEN}[OK] 음성 파일 저장: {audio_path}")
            else:
                print(f"\n{Fore.YELLOW}[4/4] 음성 변환 건너뛰기 (TTS 비활성화)")

            # 완료 메시지
            print(f"\n{Fore.GREEN}{'='*60}")
            print(f"{Fore.GREEN}[OK] 모든 처리 완료!")
            print(f"{Fore.GREEN}{'='*60}\n")

            return answer_text

        except Exception as e:
            print(f"\n{Fore.RED}[ERROR] 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return None

    def interactive_mode(self):
        """대화형 모드"""
        print(f"{Fore.CYAN}대화형 모드를 시작합니다.")
        print(f"{Fore.CYAN}종료하려면 'quit' 또는 'exit'를 입력하세요.\n")

        while True:
            try:
                # 질문 입력
                print(f"{Fore.MAGENTA}고민을 입력해주세요:")
                question = input(f"{Fore.WHITE}> ").strip()

                # 종료 명령어 확인
                if question.lower() in ['quit', 'exit', '종료', 'q']:
                    print(f"\n{Fore.CYAN}시스템을 종료합니다. 좋은 하루 되세요!")
                    break

                # 빈 입력 체크
                if not question:
                    print(f"{Fore.YELLOW}질문을 입력해주세요.\n")
                    continue

                # TTS 사용 여부 확인
                print(f"\n{Fore.MAGENTA}음성 답변을 생성할까요? (y/n, 기본: y)")
                tts_input = input(f"{Fore.WHITE}> ").strip().lower()
                enable_tts = tts_input != 'n'

                # 질문 처리
                self.process_question(question, enable_tts)

                # 계속 여부 확인
                print(f"\n{Fore.MAGENTA}다른 고민이 있으신가요? (계속하려면 Enter)")
                input()

            except KeyboardInterrupt:
                print(f"\n\n{Fore.CYAN}시스템을 종료합니다.")
                break
            except Exception as e:
                print(f"\n{Fore.RED}[ERROR] 오류: {e}\n")


def main():
    """메인 함수"""
    # 시스템 초기화
    system = CounselingSystem()

    # 명령행 인자 확인
    if len(sys.argv) > 1:
        # 질문이 인자로 제공된 경우
        question = ' '.join(sys.argv[1:])
        system.process_question(question)
    else:
        # 대화형 모드
        system.interactive_mode()


if __name__ == "__main__":
    main()
