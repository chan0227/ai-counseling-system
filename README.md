# AI 고민상담 자동 답변 시스템 MVP

실시간 고민 상담 질문에 대해 AI 기반 답변을 자동 생성하는 시스템의 MVP(Minimum Viable Product)입니다.

## 주요 기능

- 📝 질문 입력 및 분석
- 🔍 키워드 기반 답변 매칭
- 🤖 Claude API를 활용한 맞춤형 답변 생성
- 🎙️ TTS(Text-to-Speech)를 통한 음성 답변 생성
- 💾 답변 및 오디오 파일 저장

## 프로젝트 구조

```
ai-counseling-mvp/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── data/
│   └── sample_answers.json    # 샘플 답변 데이터베이스
├── src/
│   ├── __init__.py
│   ├── config.py              # 설정 관리
│   ├── matcher.py             # 답변 매칭 로직
│   ├── generator.py           # Claude API 답변 생성
│   ├── tts.py                 # TTS 음성 변환
│   └── main.py                # 메인 실행 파일
├── output/                    # 생성된 답변 저장 폴더
└── tests/
    └── test_basic.py
```

## 설치 방법

### 1. 필수 요구사항
- Python 3.10 이상
- Claude API 키 (Anthropic)

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 API 키를 입력합니다.

```bash
cp .env.example .env
# .env 파일을 열어 CLAUDE_API_KEY를 입력
```

## 사용 방법

### CLI 실행
```bash
python src/main.py
```

질문을 입력하면:
1. 유사한 답변을 데이터베이스에서 검색
2. Claude API로 맞춤형 답변 생성
3. TTS로 음성 변환
4. 텍스트 및 오디오 파일로 저장

### 출력 결과
- `output/answer_[timestamp].txt` - 생성된 답변 텍스트
- `output/answer_[timestamp].mp3` - 음성 파일

## 기술 스택

- **언어**: Python 3.10+
- **LLM**: Claude API (Anthropic)
- **TTS**: gTTS (Google Text-to-Speech)
- **기타**: python-dotenv, requests

## 개발 계획

### ✅ Phase 1: MVP (현재)
- 기본 질문-답변 매칭
- Claude API 답변 생성
- 기본 TTS

### 📋 Phase 2: 고도화
- 벡터 임베딩 기반 의미론적 검색
- 감정 분석 추가
- 음성 클로닝 (Voice Cloning)
- 웹 인터페이스

### 🚀 Phase 3: 프로덕션
- 실제 고민상담 사이트 연동
- 모니터링 대시보드
- 성능 최적화

## 배포 방법

### 🌐 온라인 배포 (권장)

**Streamlit Cloud** (무료, 가장 간단):
1. GitHub에 레포지토리 업로드
2. https://share.streamlit.io/ 에서 배포
3. Secrets에 API 키 설정
4. 상세 가이드: `DEPLOY.md` 참고

**Render** (무료 티어 제공):
1. https://render.com 에서 Web Service 생성
2. GitHub 레포지토리 연결
3. Start Command: `streamlit run app.py`
4. Environment에 API 키 설정

### 📦 이 ZIP 파일 사용법

1. ZIP 압축 해제
2. 터미널에서 프로젝트 폴더로 이동
3. `pip install -r requirements.txt`
4. `.env.example`을 복사하여 `.env` 생성 후 API 키 입력
5. `streamlit run app.py`

## 라이선스

MIT License

## 문의

프로젝트 관련 문의: GitHub Issues
