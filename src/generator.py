"""
답변 생성 모듈
Claude API를 활용하여 질문에 대한 맞춤형 답변 생성
"""

from typing import List, Dict, Tuple
from anthropic import Anthropic

from config import CLAUDE_API_KEY, CLAUDE_MODEL, MAX_TOKENS, TEMPERATURE


class AnswerGenerator:
    """Claude API 기반 답변 생성 클래스"""

    def __init__(self):
        """초기화"""
        if not CLAUDE_API_KEY:
            raise ValueError("CLAUDE_API_KEY가 설정되지 않았습니다.")

        self.client = Anthropic(api_key=CLAUDE_API_KEY)
        print("[OK] Claude API 클라이언트 초기화 완료")

    def generate_answer(
        self,
        question: str,
        reference_answers: List[Tuple[Dict, float]]
    ) -> str:
        """
        질문과 참고 답변을 바탕으로 맞춤형 답변 생성

        Args:
            question: 사용자 질문
            reference_answers: (답변, 유사도) 튜플 리스트

        Returns:
            생성된 답변 텍스트
        """
        # 시스템 프롬프트
        system_prompt = """당신은 공감 능력이 뛰어난 전문 고민 상담사입니다.
사용자의 고민에 진심으로 공감하고, 따뜻하면서도 실질적인 조언을 제공합니다.

답변 작성 원칙:
1. 공감과 이해: 먼저 상대방의 감정을 공감하고 이해한다는 것을 표현
2. 긍정적 관점: 문제를 다룰 때도 희망적이고 건설적인 관점 유지
3. 구체적 조언: 추상적인 조언보다 실천 가능한 구체적 방법 제시
4. 격려와 지지: 마무리는 항상 따뜻한 격려와 응원의 메시지로

답변 구조:
- 공감 표현 (2-3문장)
- 상황 이해 및 분석 (2-3문장)
- 구체적 조언 및 방법 (4-5문장)
- 격려 및 마무리 (2-3문장)

주의사항:
- 의료적/법률적 조언은 하지 않고 전문가 상담 권유
- 위기 상황(자살, 폭력 등)은 즉시 전문 기관 연락 권유
- 판단하거나 비난하지 않는 중립적 태도 유지
- 이모지나 특수문자는 사용하지 말고 순수한 한글 텍스트만 사용"""

        # 참고 답변 정리
        reference_text = self._format_references(reference_answers)

        # 사용자 프롬프트
        user_prompt = f"""다음은 사용자의 고민입니다:

"{question}"

위 고민에 대해 따뜻하고 공감적인 답변을 작성해주세요.

참고할 수 있는 유사한 고민에 대한 답변들:
{reference_text}

위 참고 답변들의 핵심 내용을 활용하되, 사용자의 구체적인 상황에 맞게 새롭게 작성해주세요.
답변은 자연스러운 한국어로, 300-500자 정도로 작성해주세요."""

        try:
            # Claude API 호출
            response = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            answer = response.content[0].text
            return answer.strip()

        except Exception as e:
            print(f"[ERROR] Claude API 호출 오류: {e}")
            raise

    def _format_references(self, reference_answers: List[Tuple[Dict, float]]) -> str:
        """참고 답변을 프롬프트용으로 포맷팅"""
        if not reference_answers:
            return "참고할 유사한 답변이 없습니다."

        formatted = []
        for i, (answer, score) in enumerate(reference_answers, 1):
            formatted.append(
                f"\n[참고 {i}] {answer['title']} (카테고리: {answer['category']}, 유사도: {score:.0%})\n"
                f"{answer['content']}\n"
            )

        return "\n".join(formatted)

    def generate_simple_answer(self, question: str) -> str:
        """
        참고 답변 없이 질문만으로 답변 생성 (폴백용)

        Args:
            question: 사용자 질문

        Returns:
            생성된 답변
        """
        system_prompt = """당신은 공감 능력이 뛰어난 전문 고민 상담사입니다.
사용자의 고민에 진심으로 공감하고, 따뜻하면서도 실질적인 조언을 제공합니다."""

        user_prompt = f"""다음 고민에 대해 따뜻하고 공감적인 답변을 300-500자로 작성해주세요:

"{question}" """

        try:
            response = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            return response.content[0].text.strip()

        except Exception as e:
            print(f"[ERROR] Claude API 호출 오류: {e}")
            raise


def test_generator():
    """생성기 테스트 함수"""
    print("=== 답변 생성 테스트 ===\n")

    try:
        generator = AnswerGenerator()

        # 테스트 질문
        question = "최근 친구와 사소한 일로 다퉜는데, 먼저 연락하기가 어색해요."

        # 참고 답변 (실제로는 matcher에서 가져옴)
        reference = [
            ({
                "id": "TEST",
                "category": "대인관계",
                "title": "친구 관계 회복",
                "content": "친구와의 다툼은 누구에게나 있는 일입니다. 먼저 연락하는 것이 어색하더라도, 관계가 소중하다면 용기를 내보세요."
            }, 0.85)
        ]

        print(f"질문: {question}\n")
        print("답변 생성 중...")

        answer = generator.generate_answer(question, reference)

        print("\n생성된 답변:")
        print("-" * 50)
        print(answer)
        print("-" * 50)

    except Exception as e:
        print(f"[ERROR] 테스트 실패: {e}")


if __name__ == "__main__":
    test_generator()
