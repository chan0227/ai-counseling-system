"""
기본 기능 테스트
"""

import sys
from pathlib import Path

# src 디렉토리를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import json
from config import SAMPLE_ANSWERS_PATH


def test_data_loading():
    """데이터 로딩 테스트"""
    print("=== 데이터 로딩 테스트 ===")

    try:
        with open(SAMPLE_ANSWERS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

        answers = data.get('answers', [])
        print(f"[OK] {len(answers)}개의 답변 데이터 로드 성공")

        # 첫 번째 답변 확인
        if answers:
            first = answers[0]
            print(f"  첫 번째 답변: [{first['category']}] {first['title']}")

        return True

    except Exception as e:
        print(f"[FAIL] 데이터 로딩 실패: {e}")
        return False


def test_matcher():
    """매칭 모듈 테스트"""
    print("\n=== 매칭 모듈 테스트 ===")

    try:
        from matcher import AnswerMatcher

        matcher = AnswerMatcher()
        question = "친구와 다퉜어요"
        matches = matcher.find_best_matches(question, top_k=3)

        print(f"[OK] 매칭 테스트 성공")
        print(f"  질문: {question}")
        print(f"  매칭된 답변 수: {len(matches)}")

        for i, (answer, score) in enumerate(matches, 1):
            print(f"  {i}. {answer['title']} ({score:.1%})")

        return True

    except Exception as e:
        print(f"[FAIL] 매칭 테스트 실패: {e}")
        return False


def test_config():
    """설정 테스트"""
    print("\n=== 설정 테스트 ===")

    try:
        from config import validate_config, CLAUDE_API_KEY

        if not CLAUDE_API_KEY or CLAUDE_API_KEY == "your_api_key_here":
            print("! Claude API 키가 설정되지 않았습니다.")
            print("  .env 파일을 생성하고 API 키를 입력하세요.")
            return False

        validate_config()
        print("[OK] 설정 검증 성공")
        return True

    except Exception as e:
        print(f"[FAIL] 설정 테스트 실패: {e}")
        return False


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 60)
    print("AI 고민상담 시스템 - 기본 테스트")
    print("=" * 60 + "\n")

    results = []

    # 각 테스트 실행
    results.append(("데이터 로딩", test_data_loading()))
    results.append(("설정 검증", test_config()))
    results.append(("매칭 모듈", test_matcher()))

    # 결과 요약
    print("\n" + "=" * 60)
    print("테스트 결과 요약")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status}: {name}")

    print(f"\n총 {passed}/{total} 테스트 통과")

    if passed == total:
        print("\n모든 테스트를 통과했습니다!")
    else:
        print("\n일부 테스트가 실패했습니다. 위 내용을 확인하세요.")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
