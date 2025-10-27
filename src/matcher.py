"""
답변 매칭 모듈
질문과 가장 유사한 답변을 데이터베이스에서 찾는 기능
"""

import json
from pathlib import Path
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config import SAMPLE_ANSWERS_PATH, SIMILARITY_THRESHOLD, TOP_K_MATCHES


class AnswerMatcher:
    """답변 매칭 클래스"""

    def __init__(self, answers_path: Path = SAMPLE_ANSWERS_PATH):
        """
        초기화

        Args:
            answers_path: 답변 데이터베이스 JSON 파일 경로
        """
        self.answers_path = answers_path
        self.answers = []
        self.vectorizer = TfidfVectorizer(
            analyzer='char',  # 한국어는 문자 단위가 효과적
            ngram_range=(2, 3)  # 2-3글자 조합
        )
        self.load_answers()
        self.prepare_vectorizer()

    def load_answers(self):
        """답변 데이터베이스 로드"""
        try:
            with open(self.answers_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.answers = data.get('answers', [])
            print(f"[OK] {len(self.answers)}개의 답변을 로드했습니다.")
        except FileNotFoundError:
            print(f"[ERROR] 답변 파일을 찾을 수 없습니다: {self.answers_path}")
            raise
        except json.JSONDecodeError:
            print(f"[ERROR] JSON 파싱 오류: {self.answers_path}")
            raise

    def prepare_vectorizer(self):
        """답변 데이터로 벡터라이저 학습"""
        # 모든 답변의 키워드, 제목, 내용을 결합
        corpus = []
        for answer in self.answers:
            text = ' '.join([
                ' '.join(answer.get('keywords', [])),
                answer.get('title', ''),
                answer.get('content', '')
            ])
            corpus.append(text)

        # 벡터라이저 학습
        self.answer_vectors = self.vectorizer.fit_transform(corpus)
        print(f"[OK] 벡터라이저 학습 완료")

    def find_best_matches(self, question: str, top_k: int = TOP_K_MATCHES) -> List[Tuple[Dict, float]]:
        """
        질문과 가장 유사한 답변 찾기

        Args:
            question: 사용자 질문
            top_k: 상위 몇 개를 반환할지

        Returns:
            (답변, 유사도 점수) 튜플의 리스트
        """
        # 질문 벡터화
        question_vector = self.vectorizer.transform([question])

        # 코사인 유사도 계산
        similarities = cosine_similarity(question_vector, self.answer_vectors)[0]

        # 상위 k개 인덱스 추출
        top_indices = similarities.argsort()[-top_k:][::-1]

        # 결과 구성
        results = []
        for idx in top_indices:
            score = similarities[idx]
            if score >= SIMILARITY_THRESHOLD:
                results.append((self.answers[idx], float(score)))

        return results

    def get_match_summary(self, matches: List[Tuple[Dict, float]]) -> str:
        """
        매칭 결과 요약

        Args:
            matches: 매칭된 답변 리스트

        Returns:
            요약 문자열
        """
        if not matches:
            return "[X] 유사한 답변을 찾지 못했습니다."

        summary = f"[OK] {len(matches)}개의 유사한 답변을 찾았습니다:\n"
        for i, (answer, score) in enumerate(matches, 1):
            summary += f"\n{i}. [{answer['category']}] {answer['title']}"
            summary += f" (유사도: {score:.2%})"

        return summary


def test_matcher():
    """매처 테스트 함수"""
    print("=== 답변 매칭 테스트 ===\n")

    matcher = AnswerMatcher()

    test_questions = [
        "남자친구와 헤어져서 너무 힘들어요",
        "진로를 어떻게 정해야 할지 모르겠어요",
        "매일 걱정이 많고 불안해요",
        "친구를 사귀고 싶은데 방법을 모르겠어요"
    ]

    for question in test_questions:
        print(f"\n질문: {question}")
        matches = matcher.find_best_matches(question)
        print(matcher.get_match_summary(matches))

        if matches:
            best_match, score = matches[0]
            print(f"\n가장 유사한 답변 미리보기:")
            print(f"{best_match['content'][:100]}...")


if __name__ == "__main__":
    test_matcher()
