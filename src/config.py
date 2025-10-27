"""
설정 관리 모듈
환경 변수 로드 및 프로젝트 설정 관리
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 프로젝트 루트 디렉토리
PROJECT_ROOT = Path(__file__).parent.parent

# .env 파일 로드
load_dotenv(PROJECT_ROOT / ".env")

# Streamlit secrets 지원
try:
    import streamlit as st
    if hasattr(st, 'secrets'):
        # Streamlit Cloud 환경
        CLAUDE_API_KEY = st.secrets.get("CLAUDE_API_KEY", os.getenv("CLAUDE_API_KEY"))
        CLAUDE_MODEL = st.secrets.get("CLAUDE_MODEL", os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929"))
        MAX_TOKENS = int(st.secrets.get("MAX_TOKENS", os.getenv("MAX_TOKENS", "2000")))
        TEMPERATURE = float(st.secrets.get("TEMPERATURE", os.getenv("TEMPERATURE", "0.7")))
    else:
        # 로컬 환경
        CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
        CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")
        MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
        TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
except ImportError:
    # Streamlit이 없는 환경 (CLI 모드)
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
    CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# 파일 경로
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
SAMPLE_ANSWERS_PATH = DATA_DIR / "sample_answers.json"

# 출력 디렉토리 생성
OUTPUT_DIR.mkdir(exist_ok=True)

# 답변 생성 설정
SIMILARITY_THRESHOLD = 0.3  # 유사도 임계값 (0.0 ~ 1.0)
TOP_K_MATCHES = 3  # 상위 몇 개의 유사 답변을 참고할지

# TTS 설정
TTS_LANGUAGE = "ko"  # 한국어
TTS_SLOW = False  # 속도 (False = 정상 속도)


def validate_config():
    """설정 유효성 검사"""
    if not CLAUDE_API_KEY or CLAUDE_API_KEY == "your_api_key_here":
        raise ValueError(
            "CLAUDE_API_KEY가 설정되지 않았습니다. "
            ".env 파일을 확인해주세요."
        )

    if not DATA_DIR.exists():
        raise FileNotFoundError(f"데이터 디렉토리가 없습니다: {DATA_DIR}")

    return True


if __name__ == "__main__":
    # 설정 테스트
    try:
        validate_config()
        print("[OK] 설정이 올바르게 구성되었습니다.")
        print(f"  - Claude Model: {CLAUDE_MODEL}")
        print(f"  - Data Directory: {DATA_DIR}")
        print(f"  - Output Directory: {OUTPUT_DIR}")
    except Exception as e:
        print(f"[ERROR] 설정 오류: {e}")
