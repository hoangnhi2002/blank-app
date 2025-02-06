
import streamlit as st
import requests
from bs4 import BeautifulSoup 
 

# Hàm lấy danh sách URL các chương từ trang chính

def fetch_chapter_urls(main_url):
    try:
        response = requests.get(main_url)
        if response.status_code != 200:
            st.error("Không thể truy cập trang chính.")
            return []
        soup = BeautifulSoup(response.content, 'html.parser')
        # Lấy các liên kết chương
        chapter_links = soup.select('div.list-chapters div.episode-title a')
        urls = [link['href'] for link in chapter_links]
        return urls[::-1]  # Lưu từ chương nhỏ đến lớn
    except Exception as e:
        st.error(f"Lỗi khi tải danh sách chương: {e}")
        return []
    
    
# Hàm lấy nội dung của một chương
def fetch_chapter_content(chapter_url):
    try:
        response = requests.get(chapter_url)
        if response.status_code != 200:
            st.warning(f"Không thể truy cập chương: {chapter_url}")
            return None
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.select_one('div#chapter-content-render')  # Cập nhật selector nếu cần
        if not content:
            st.warning(f"Không tìm thấy nội dung trong: {chapter_url}")
            return None
        return content.get_text(separator='\n')
    except Exception as e:
            st.error(f"Lỗi khi tải nội dung chương: {e}")
            return None
# Ứng dụng Streamlit
def main():
    st.title("Ứng dụng Tải Truyện Tự Động")
     # Nhập liên kết trang chính
    main_url = st.text_input("Nhập liên kết trang chính của truyện:", "")
             
    if st.button("Tải nội dung truyện"):
        if not main_url:
            st.error("Vui lòng nhập liên kết trang chính.")
        else:
            st.info("Đang tải danh sách chương...")
            chapter_urls = fetch_chapter_urls(main_url)
            if chapter_urls:
                st.success(f"Đã tìm thấy {len(chapter_urls)} chương.")
                # Tải nội dung từng chương
                all_content = []
                for index, url in enumerate(chapter_urls, start=1):
                    st.info(f"Đang tải chương {index}...")
                    content = fetch_chapter_content(url)
                    if content:
                        # Lọc bỏ các dòng không mong muốn
                        lines = content.splitlines()
                        filtered_lines = [
                            line.strip() for line in lines
                            if line.strip() and not any(
                                unwanted in line for unwanted in ["-Hết-", "[Truyện được đăng tải duy nhất tại MonkeyD.com.vn -"]
                            )
                        ]
                        all_content.append("\n".join(filtered_lines))

                # Hiển thị nội dung
                st.subheader("Nội dung truyện:")
                for index, chapter_content in enumerate(all_content, start=1):
                    st.markdown(f"### Chương {index}")
                    st.text(chapter_content)
                # Nút tải xuống
                all_content_text = "\n\n".join(all_content)
                st.download_button(
                    label="Tải xuống nội dung",
                    data=all_content_text,
                    file_name="truyen.txt",
                    mime="text/plain"
                )
            else:
                st.warning("Không tìm thấy chương nào.")
if __name__ == "__main__":
        main()
