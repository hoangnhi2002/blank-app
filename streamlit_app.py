import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

def get_full_story(start_url):
    """Tự động lấy tất cả các chương của truyện từ Wattpad"""
    all_content = []
    current_url = start_url
    chapter_count = 1  # Đếm số chương

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    while current_url:
        response = requests.get(current_url, headers=headers)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        # Lấy tiêu đề chương
        title_tag = soup.find('h1', class_='sr-only')
        title = title_tag.text.strip() if title_tag else f"Chapter {chapter_count}"

        # Lấy nội dung chương
        story_divs = soup.find_all('p')
        content = '\n'.join([p.text for p in story_divs])

        # Lưu nội dung chương vào danh sách
        all_content.append(f"{title}\n\n{content}\n\n{'='*50}\n")

        # Tìm link chương tiếp theo
        next_chapter_tag = soup.select_one("#story-part-navigation a")
        next_chapter_url = next_chapter_tag['href'] if next_chapter_tag else None
        if next_chapter_url and not next_chapter_url.startswith("http"):
            next_chapter_url = "https://www.wattpad.com" + next_chapter_url  # Thêm domain nếu thiếu

        # Cập nhật URL chương tiếp theo hoặc dừng vòng lặp nếu không có chương nữa
        current_url = next_chapter_url
        chapter_count += 1
        time.sleep(1)  # Tránh bị Wattpad chặn do gửi request quá nhanh

    # Gộp tất cả nội dung vào một file
    full_story = "\n".join(all_content)
    return full_story

# Giao diện Streamlit
st.title("📖 Wattpad Full Story Downloader")

# Nhập URL chương đầu tiên của truyện Wattpad
story_url = st.text_input("🔗 Nhập URL chương đầu tiên của truyện Wattpad:")

if story_url:
    if st.button("📥 Tải Toàn Bộ Truyện"):
        with st.spinner("⏳ Đang tải toàn bộ truyện... Vui lòng đợi!"):
            full_story = get_full_story(story_url)

        if full_story:
            st.success("✅ Hoàn tất! Truyện đã được tải thành công.")
            st.text_area("📖 Nội dung truyện:", full_story[:2000], height=400)  # Hiển thị 2000 ký tự đầu tiên để xem trước

            # Lưu vào file TXT
            filename = "Full_Story.txt"
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(full_story)

            # Nút tải file TXT
            with open(filename, 'rb') as file:
                st.download_button(
                    label="⬇️ Tải về toàn bộ truyện (.txt)",
                    data=file,
                    file_name=filename,
                    mime='text/plain'
                )
        else:
            st.error("❌ Không thể tải truyện. Vui lòng kiểm tra lại URL.")
