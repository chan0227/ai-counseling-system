# 사용 가이드

AI 고민상담 자동 답변 시스템 MVP의 상세 사용 가이드입니다.

## 목차
- [빠른 시작](#빠른-시작)
- [설치 방법](#설치-방법)
- [사용 방법](#사용-방법)
- [모듈별 상세 설명](#모듈별-상세-설명)
- [문제 해결](#문제-해결)

## 빠른 시작

### 1. 필수 요구사항
```bash
# Python 버전 확인 (3.10 이상 필요)
python --version

# pip 업그레이드
python -m pip install --upgrade pip
```

### 2. 패키지 설치
```bash
# 프로젝트 디렉토리로 이동
cd ai-counseling-mvp

# 필수 패키지 설치
pip install -r requirements.txt
```

### 3. 환경 변수 설정
```bash
# .env 파일 생성 (Windows)
copy .env.example .env

# .env 파일 생성 (Mac/Linux)
cp .env.example .env
```

`.env` 파일을 편집하여 Claude API 키 입력:
```
CLAUDE_API_KEY=your_actual_api_key_here
```

**Claude API 키 발급 방법:**
1. https://console.anthropic.com/ 접속
2. 계정 생성/로그인
3. API Keys 메뉴에서 새 키 생성
4. 생성된 키를 `.env` 파일에 입력

### 4. 테스트 실행
```bash
# 기본 테스트
python tests/test_basic.py

# 매칭 모듈 테스트
python src/matcher.py

# TTS 모듈 테스트
python src/tts.py
```

### 5. 시스템 실행
```bash
# 대화형 모드
python src/main.py

# 명령행 인자로 질문 전달
python src/main.py "친구와 다퉜는데 어떻게 화해해야 할까요?"
```

## 설치 방법

### Python 가상 환경 사용 (권장)

**Windows:**
```bash
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화
venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
# 가상 환경 생성
python3 -m venv venv

# 가상 환경 활성화
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 필수 패키지 설명

- **anthropic**: Claude API 클라이언트
- **python-dotenv**: 환경 변수 관리
- **gTTS**: Google Text-to-Speech
- **scikit-learn**: 텍스트 유사도 계산
- **colorama**: 콘솔 색상 출력 (선택사항)

## 사용 방법

### 대화형 모드 (권장)

```bash
python src/main.py
```

실행 화면:
```
============================================================
AI 고민상담 자동 답변 시스템 MVP
============================================================

시스템 초기화 중...

✓ 10개의 답변을 로드했습니다.
✓ 벡터라이저 학습 완료
✓ Claude API 클라이언트 초기화 완료
✓ TTS 모듈 초기화 완료

✓ 시스템 초기화 완료!

대화형 모드를 시작합니다.
종료하려면 'quit' 또는 'exit'를 입력하세요.

고민을 입력해주세요:
>
```

### 명령행 모드

특정 질문에 대한 답변만 빠르게 생성:

```bash
python src/main.py "최근 진로에 대해 고민이 많아요"
```

### 출력 파일 확인

생성된 답변은 `output/` 디렉토리에 저장됩니다:

```
output/
├── answer_20250127_143052.txt    # 텍스트 답변
└── answer_20250127_143052.mp3    # 음성 답변
```

## 모듈별 상세 설명

### 1. config.py - 설정 관리

프로젝트 전반의 설정을 관리합니다.

**주요 설정 변경 방법:**

`.env` 파일 편집:
```env
# Claude API 모델 변경
CLAUDE_MODEL=claude-sonnet-4-5-20250929

# 답변 길이 조절 (토큰 수)
MAX_TOKENS=2000

# 창의성 조절 (0.0 ~ 1.0)
TEMPERATURE=0.7
```

`src/config.py` 파일에서 추가 설정:
```python
# 유사도 임계값 (낮을수록 더 많은 답변 매칭)
SIMILARITY_THRESHOLD = 0.3

# 참고할 답변 개수
TOP_K_MATCHES = 3

# TTS 언어
TTS_LANGUAGE = "ko"
```

### 2. matcher.py - 답변 매칭

질문과 유사한 답변을 찾는 모듈입니다.

**단독 테스트:**
```bash
python src/matcher.py
```

**동작 원리:**
1. 질문과 답변을 문자 단위 벡터로 변환 (TF-IDF)
2. 코사인 유사도로 유사한 답변 검색
3. 임계값 이상의 답변만 반환

### 3. generator.py - 답변 생성

Claude API로 맞춤형 답변을 생성합니다.

**단독 테스트:**
```bash
python src/generator.py
```

**프롬프트 커스터마이징:**

`src/generator.py` 파일의 `system_prompt` 수정:
```python
system_prompt = """당신은 공감 능력이 뛰어난 전문 고민 상담사입니다.
[여기에 원하는 성격/스타일 추가]
"""
```

### 4. tts.py - 음성 변환

텍스트 답변을 음성으로 변환합니다.

**단독 테스트:**
```bash
python src/tts.py
```

**TTS 설정 변경:**

느린 속도로 읽기:
```python
# src/config.py
TTS_SLOW = True
```

다른 언어 사용:
```python
# src/config.py
TTS_LANGUAGE = "en"  # 영어
```

### 5. main.py - 메인 시스템

전체 시스템을 통합 실행합니다.

**TTS 비활성화하고 실행:**

코드 수정:
```python
# main.py 실행 시 대화형 모드에서 'n' 입력
음성 답변을 생성할까요? (y/n, 기본: y)
> n
```

## 샘플 답변 데이터베이스 관리

### 새 답변 추가

`data/sample_answers.json` 파일 편집:

```json
{
  "answers": [
    {
      "id": "A011",
      "category": "새로운 카테고리",
      "keywords": ["키워드1", "키워드2", "키워드3"],
      "title": "답변 제목",
      "content": "답변 내용...",
      "key_points": ["핵심1", "핵심2"]
    }
  ]
}
```

### 카테고리

현재 지원하는 카테고리:
- 연애
- 진로
- 가족
- 대인관계
- 학업
- 자존감
- 스트레스
- 직장
- 불안

필요시 새 카테고리 추가 가능

## 문제 해결

### Q1: "CLAUDE_API_KEY가 설정되지 않았습니다" 오류

**해결 방법:**
1. `.env` 파일이 프로젝트 루트에 있는지 확인
2. 파일 내용이 정확한지 확인:
   ```
   CLAUDE_API_KEY=sk-ant-...
   ```
3. API 키에 공백이나 따옴표가 없는지 확인

### Q2: "ModuleNotFoundError" 오류

**해결 방법:**
```bash
# 패키지 재설치
pip install -r requirements.txt

# 특정 패키지만 설치
pip install anthropic
```

### Q3: TTS 생성 실패

**해결 방법:**
1. 인터넷 연결 확인 (gTTS는 온라인 필요)
2. 방화벽 설정 확인
3. 텍스트가 너무 길지 않은지 확인

### Q4: 유사 답변을 찾지 못함

**해결 방법:**
1. `src/config.py`에서 `SIMILARITY_THRESHOLD` 값 낮추기:
   ```python
   SIMILARITY_THRESHOLD = 0.2  # 0.3 → 0.2
   ```
2. 답변 데이터베이스에 더 다양한 키워드 추가

### Q5: Claude API 호출 오류

**가능한 원인:**
- API 키 만료 또는 잔액 부족
- 네트워크 연결 문제
- API 사용 한도 초과

**해결 방법:**
1. Anthropic 콘솔에서 API 키 상태 확인
2. 잔액 및 사용량 확인
3. 네트워크 연결 확인

## 고급 사용

### 배치 처리

여러 질문을 한 번에 처리:

```python
# batch_process.py (새로 만들기)
from src.main import CounselingSystem

questions = [
    "친구와 다퉜어요",
    "진로가 고민돼요",
    "공부 의욕이 안 생겨요"
]

system = CounselingSystem()

for question in questions:
    print(f"\n처리 중: {question}")
    system.process_question(question, enable_tts=False)
```

### 웹 API 서버로 확장

Flask를 사용한 간단한 API 서버:

```python
# api_server.py (새로 만들기)
from flask import Flask, request, jsonify
from src.main import CounselingSystem

app = Flask(__name__)
system = CounselingSystem()

@app.route('/answer', methods=['POST'])
def get_answer():
    data = request.json
    question = data.get('question')
    answer = system.process_question(question, enable_tts=False)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(port=5000)
```

## 추가 리소스

- [Claude API 문서](https://docs.anthropic.com/)
- [gTTS 문서](https://gtts.readthedocs.io/)
- [scikit-learn 문서](https://scikit-learn.org/)

## 지원

문제가 계속되면:
1. GitHub Issues에 문의
2. 이메일 문의: [연락처]
