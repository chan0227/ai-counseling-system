"""
AI 고민상담 자동 답변 시스템 - 웹 인터페이스
Streamlit 기반 웹 UI
"""

import streamlit as st
import sys
import os
from pathlib import Path
from datetime import datetime
import base64

# Streamlit Secrets를 환경 변수로 설정 (config.py 로드 전에 실행)
if hasattr(st, 'secrets'):
    try:
        os.environ['CLAUDE_API_KEY'] = st.secrets["CLAUDE_API_KEY"]
        if "CLAUDE_MODEL" in st.secrets:
            os.environ['CLAUDE_MODEL'] = st.secrets["CLAUDE_MODEL"]
        if "MAX_TOKENS" in st.secrets:
            os.environ['MAX_TOKENS'] = st.secrets["MAX_TOKENS"]
        if "TEMPERATURE" in st.secrets:
            os.environ['TEMPERATURE'] = st.secrets["TEMPERATURE"]
    except (KeyError, FileNotFoundError):
        pass

# src 디렉토리를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import validate_config
from matcher import AnswerMatcher
from generator import AnswerGenerator
from tts import TextToSpeech
from main import remove_emojis


# 페이지 설정
st.set_page_config(
    page_title="AI 고민상담 시스템",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .category-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin: 0.25rem;
        border-radius: 1rem;
        background-color: #e3f2fd;
        color: #1976d2;
        font-size: 0.875rem;
    }
    .answer-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .reference-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stTextArea textarea {
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def init_system():
    """시스템 초기화 (캐싱)"""
    try:
        validate_config()
        matcher = AnswerMatcher()
        generator = AnswerGenerator()
        tts = TextToSpeech()
        return matcher, generator, tts, None
    except Exception as e:
        return None, None, None, str(e)


def get_audio_player(audio_path: Path):
    """오디오 플레이어 HTML 생성"""
    try:
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
        <audio controls style="width: 100%;">
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        </audio>
        """
        return audio_html
    except Exception as e:
        return f"<p>오디오 로드 실패: {e}</p>"


def main():
    # 헤더
    st.markdown('<div class="main-header">💬 AI 고민상담 자동 답변 시스템</div>', unsafe_allow_html=True)

    # 시스템 초기화
    matcher, generator, tts, error = init_system()

    if error:
        st.error(f"시스템 초기화 오류: {error}")
        st.info("1. .env 파일에 CLAUDE_API_KEY가 설정되어 있는지 확인하세요.\n2. 터미널에서 `python src/config.py`를 실행하여 설정을 확인하세요.")
        return

    # 사이드바
    with st.sidebar:
        st.header("📌 시스템 정보")
        st.success("✓ 시스템 준비 완료")

        st.markdown("---")
        st.subheader("🗂️ 지원 카테고리")
        categories = ["연애", "진로", "가족", "대인관계", "학업", "자존감", "스트레스", "직장", "불안"]
        for cat in categories:
            st.markdown(f'<span class="category-badge">{cat}</span>', unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("⚙️ 설정")
        enable_tts = st.checkbox("음성 답변 생성", value=True)
        show_references = st.checkbox("참고 답변 표시", value=True)

        st.markdown("---")
        st.info("""
        **사용 방법:**
        1. 고민을 입력창에 작성
        2. '답변 생성' 버튼 클릭
        3. AI가 생성한 답변 확인
        4. 음성 답변 듣기 (선택)
        """)

    # 메인 컨텐츠
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("💭 고민을 입력해주세요")
        question = st.text_area(
            label="고민 내용",
            placeholder="예: 친구와 다퉜는데 어떻게 화해해야 할까요?",
            height=150,
            label_visibility="collapsed"
        )

        # 예시 질문 버튼
        st.caption("예시 질문:")
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if st.button("💔 이별 고민"):
                question = "남자친구와 헤어져서 너무 힘들어요"
                st.rerun()
        with col_btn2:
            if st.button("🎓 진로 고민"):
                question = "진로를 어떻게 정해야 할지 모르겠어요"
                st.rerun()
        with col_btn3:
            if st.button("😰 불안 고민"):
                question = "매일 걱정이 많고 불안해요"
                st.rerun()

        generate_button = st.button("🚀 답변 생성", type="primary", use_container_width=True)

    with col2:
        st.subheader("📊 통계")
        st.metric("답변 데이터베이스", f"{len(matcher.answers)}개")
        st.metric("카테고리", f"{len(categories)}개")

        if 'answer_count' not in st.session_state:
            st.session_state.answer_count = 0
        st.metric("생성된 답변", f"{st.session_state.answer_count}개")

    # 답변 생성
    if generate_button and question.strip():
        with st.spinner("답변을 생성하고 있습니다..."):
            try:
                # 1. 유사 답변 검색
                st.info("🔍 유사한 답변을 검색 중...")
                matches = matcher.find_best_matches(question, top_k=3)

                # 2. 답변 생성
                st.info("🤖 AI 답변 생성 중...")
                if matches:
                    answer_text = generator.generate_answer(question, matches)
                else:
                    answer_text = generator.generate_simple_answer(question)

                # 이모지 제거
                clean_answer = remove_emojis(answer_text)

                # 3. 답변 표시
                st.markdown("---")
                st.subheader("✨ 생성된 답변")
                st.markdown(f'<div class="answer-box">{answer_text}</div>', unsafe_allow_html=True)

                # 참고 답변 표시
                if show_references and matches:
                    st.markdown("---")
                    st.subheader("📚 참고한 유사 답변")
                    for i, (answer, score) in enumerate(matches, 1):
                        with st.expander(f"{i}. [{answer['category']}] {answer['title']} (유사도: {score:.0%})"):
                            st.write(answer['content'])

                # 4. TTS 생성
                if enable_tts:
                    st.markdown("---")
                    st.subheader("🎙️ 음성 답변")
                    with st.spinner("음성을 생성하고 있습니다..."):
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        audio_path = tts.generate_answer_audio(answer_text, f"answer_{timestamp}")

                        # 오디오 플레이어
                        audio_html = get_audio_player(audio_path)
                        st.markdown(audio_html, unsafe_allow_html=True)

                        # 다운로드 버튼
                        with open(audio_path, "rb") as f:
                            st.download_button(
                                label="📥 음성 파일 다운로드",
                                data=f,
                                file_name=f"answer_{timestamp}.mp3",
                                mime="audio/mp3"
                            )

                # 통계 업데이트
                st.session_state.answer_count += 1

                st.success("✓ 답변 생성 완료!")

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
                st.exception(e)

    elif generate_button and not question.strip():
        st.warning("고민 내용을 입력해주세요.")

    # 푸터
    st.markdown("---")
    st.caption("AI 고민상담 자동 답변 시스템 MVP v0.1.0 | Powered by Claude API & Streamlit")


if __name__ == "__main__":
    main()
