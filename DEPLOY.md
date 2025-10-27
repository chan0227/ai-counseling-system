# 배포 가이드

AI 고민상담 자동 답변 시스템을 온라인에 배포하는 방법입니다.

## 목차
- [Streamlit Cloud 배포 (추천)](#streamlit-cloud-배포-추천)
- [Heroku 배포](#heroku-배포)
- [Docker 배포](#docker-배포)
- [기타 배포 옵션](#기타-배포-옵션)

---

## Streamlit Cloud 배포 (추천)

**장점**: 무료, 간단, Streamlit에 최적화
**단점**: Public 레포지토리 필요, 리소스 제한

### 1. GitHub 레포지토리 생성

#### 1-1. Git 초기화
```bash
cd ai-counseling-mvp
git init
git add .
git commit -m "Initial commit: AI Counseling MVP"
```

#### 1-2. GitHub에서 새 레포지토리 생성
1. https://github.com/new 접속
2. 레포지토리 이름 입력 (예: `ai-counseling-system`)
3. **Public** 선택 (Streamlit Cloud 무료 플랜 필수)
4. "Create repository" 클릭

#### 1-3. 로컬 레포지토리를 GitHub에 푸시
```bash
git remote add origin https://github.com/your-username/ai-counseling-system.git
git branch -M main
git push -u origin main
```

### 2. Streamlit Cloud 설정

#### 2-1. Streamlit Cloud 계정 생성
1. https://share.streamlit.io/ 접속
2. "Sign up" 클릭
3. GitHub 계정으로 로그인

#### 2-2. 앱 배포
1. "New app" 버튼 클릭
2. 레포지토리 선택: `your-username/ai-counseling-system`
3. Branch: `main`
4. Main file path: `app.py`
5. "Deploy!" 클릭

### 3. Secrets 설정 (중요!)

배포 후 API 키를 설정해야 합니다:

1. Streamlit Cloud 대시보드에서 앱 선택
2. ⚙️ "Settings" 클릭
3. "Secrets" 탭 선택
4. 다음 내용 입력:

```toml
CLAUDE_API_KEY = "sk-ant-api03-your-actual-api-key-here"
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"
MAX_TOKENS = "2000"
TEMPERATURE = "0.7"
```

5. "Save" 클릭
6. 앱이 자동으로 재시작됩니다

### 4. 완료!

앱이 배포되면 다음과 같은 URL을 받게 됩니다:
```
https://your-app-name.streamlit.app
```

이 URL을 공유하면 누구나 접속할 수 있습니다!

---

## Heroku 배포

### 1. 필수 파일 생성

#### Procfile
```bash
web: sh setup.sh && streamlit run app.py
```

#### setup.sh
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

### 2. Heroku CLI 설치 및 배포

```bash
# Heroku CLI 설치 (https://devcenter.heroku.com/articles/heroku-cli)

# Heroku 로그인
heroku login

# 새 앱 생성
heroku create ai-counseling-system

# Config Vars 설정 (API 키)
heroku config:set CLAUDE_API_KEY="your-api-key-here"

# 배포
git push heroku main

# 앱 열기
heroku open
```

---

## Docker 배포

### 1. Dockerfile 생성

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 복사
COPY . .

# 포트 노출
EXPOSE 8501

# 실행
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. .dockerignore 생성

```
.env
.git
.gitignore
__pycache__
*.pyc
output/
venv/
.streamlit/secrets.toml
```

### 3. Docker 이미지 빌드 및 실행

```bash
# 이미지 빌드
docker build -t ai-counseling-system .

# 컨테이너 실행
docker run -p 8501:8501 \
  -e CLAUDE_API_KEY="your-api-key-here" \
  ai-counseling-system

# 접속: http://localhost:8501
```

### 4. Docker Hub에 푸시 (선택사항)

```bash
# Docker Hub 로그인
docker login

# 태그 지정
docker tag ai-counseling-system your-username/ai-counseling-system:latest

# 푸시
docker push your-username/ai-counseling-system:latest
```

---

## 기타 배포 옵션

### AWS EC2
1. EC2 인스턴스 생성 (Ubuntu)
2. Docker 설치 또는 Python 환경 설정
3. 위의 Docker 방법 또는 직접 실행

### Google Cloud Run
1. 프로젝트 생성
2. Docker 이미지 빌드
3. Google Container Registry에 푸시
4. Cloud Run에 배포

### Azure App Service
1. Azure App Service 생성
2. GitHub Actions를 통한 자동 배포 설정
3. 환경 변수에 API 키 설정

---

## 보안 주의사항

### ⚠️ 절대 하지 말 것
- `.env` 파일을 Git에 커밋하지 마세요
- API 키를 코드에 하드코딩하지 마세요
- 공개 레포지토리에 secrets를 푸시하지 마세요

### ✅ 권장사항
- `.gitignore`에 `.env`와 `.streamlit/secrets.toml` 포함
- 환경 변수 또는 Secrets 관리 도구 사용
- API 키는 별도의 안전한 곳에 백업
- 정기적으로 API 키 로테이션

---

## 트러블슈팅

### Streamlit Cloud에서 "Module not found" 에러
- `requirements.txt`에 모든 패키지가 포함되어 있는지 확인
- 로컬에서 `pip freeze > requirements.txt` 실행

### API 키 오류
- Streamlit Cloud의 Secrets 설정 확인
- Secrets 형식이 올바른지 확인 (TOML 형식)
- 앱 재시작: Settings → Reboot app

### 앱이 느리거나 타임아웃
- Streamlit Cloud 무료 플랜은 리소스 제한이 있습니다
- 유료 플랜 고려 또는 다른 호스팅 서비스 사용

### 음성 파일 생성 실패
- gTTS는 인터넷 연결이 필요합니다
- 방화벽 또는 네트워크 설정 확인

---

## 비용 안내

### Streamlit Cloud
- **무료**: Public 앱 1개, 제한된 리소스
- **Pro**: $20/월, Private 앱 지원, 더 많은 리소스

### Heroku
- **무료 (Eco Dyno)**: $5/월, 1000시간
- **Basic**: $7/월
- **Standard**: $25/월

### AWS/GCP/Azure
- 사용량에 따라 다름
- 프리 티어 활용 가능
- 일반적으로 월 $10-50

---

## 추가 리소스

- [Streamlit Cloud 문서](https://docs.streamlit.io/streamlit-community-cloud)
- [Heroku Python 배포](https://devcenter.heroku.com/articles/getting-started-with-python)
- [Docker 공식 문서](https://docs.docker.com/)

---

## 문의

배포 과정에서 문제가 발생하면 GitHub Issues에 문의해주세요.
