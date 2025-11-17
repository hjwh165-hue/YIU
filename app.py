import streamlit as st
import re
import requests

# 🔒 API 키는 streamlit secrets에서 가져오기
API_KEY = st.secrets["YOUTUBE_API_KEY"]

st.title("🎬 유튜브 썸네일 추출기")
st.write("유튜브 영상 URL을 입력하면 자동으로 썸네일 이미지를 가져와요!")

url = st.text_input("유튜브 영상 URL을 입력하세요")

def extract_video_id(youtube_url):
    """
    다양한 형태의 유튜브 URL에서 video ID 추출
    """
    patterns = [
        r"v=([^&]+)",
        r"youtu\.be/([^?]+)",
        r"youtube\.com/embed/([^?]+)",
    ]
    for p in patterns:
        match = re.search(p, youtube_url)
        if match:
            return match.group(1)
    return None

if url:
    video_id = extract_video_id(url)

    if not video_id:
        st.error("유효한 유튜브 URL이 아니에요 😥")
    else:
        # 썸네일 URL 생성
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        # ▶ 유튜브 API로 영상 존재 여부 확인
        api_check_url = (
            "https://www.googleapis.com/youtube/v3/videos"
            f"?id={video_id}&key={API_KEY}&part=snippet"
        )
        response = requests.get(api_check_url).json()

        if "items" not in response or len(response["items"]) == 0:
            st.error("영상이 존재하지 않아요! URL을 다시 확인해 주세요.")
        else:
            st.success("썸네일을 성공적으로 가져왔어요!")
            st.image(thumbnail_url, caption="유튜브 썸네일")

            # 다운로드 버튼
            img_data = requests.get(thumbnail_url).content
            st.download_button(
                label="📥 썸네일 다운로드",
                data=img_data,
                file_name=f"{video_id}.jpg",
                mime="image/jpeg"
            )
