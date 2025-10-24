import csv
import re
from bs4 import BeautifulSoup

def sanitize_filename(filename):
    """
    Làm sạch một chuỗi để nó trở thành một tên tệp hợp lệ.
    """
    # Loại bỏ các ký tự không hợp lệ
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    # Thay thế khoảng trắng bằng dấu gạch dưới
    filename = filename.replace(' ', '_')
    # Giới hạn độ dài tên tệp để tránh lỗi hệ thống
    return filename[:100]

# Đường dẫn đến tệp HTML của bạn
html_file_path = 'Highlights _ Techcombank.html'

try:
    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'lxml')

    # Tìm tất cả các thẻ <table> trong tệp HTML
    tables = soup.find_all('table')

    if not tables:
        print("Không tìm thấy bảng nào trong tệp HTML.")
    else:
        print(f"Tìm thấy {len(tables)} bảng. Bắt đầu trích xuất...")

        # Lặp qua từng bảng và lưu thành một tệp CSV riêng
        for i, table in enumerate(tables):
            if len(table.find_all('tr')) < 2:
                print(f"Bỏ qua bảng {i+1} vì có vẻ là bảng layout.")
                continue

            # Tìm tiêu đề cho bảng
            title_text = f'table_{i+1}' # Tên mặc định
            
            # Thử tìm tiêu đề bằng cách tìm thẻ heading (h2, h3, h4) ngay trước bảng
            # hoặc trong thẻ cha của bảng.
            parent = table.find_parent()
            if parent:
                # Tìm thẻ heading gần nhất phía trước bảng trong cùng thẻ cha
                prev_sibling = table.find_previous_sibling(['h2', 'h3', 'h4', 'p'])
                if prev_sibling:
                    title_text = prev_sibling.get_text(strip=True)
                else:
                    # Nếu không tìm thấy, thử tìm trong thẻ cha
                    heading_in_parent = parent.find(['h2', 'h3', 'h4', 'p'])
                    if heading_in_parent:
                        title_text = heading_in_parent.get_text(strip=True)

            # Làm sạch tên tệp
            safe_filename = sanitize_filename(title_text)
            csv_file_name = f'{safe_filename}.csv'

            with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                
                rows = table.find_all('tr')
                
                for row in rows:
                    cols = [ele.get_text(strip=True) for ele in row.find_all(['th', 'td'])]
                    csv_writer.writerow(cols)
            
            print(f"Đã trích xuất thành công bảng vào '{csv_file_name}'")

    print("\nHoàn tất quá trình trích xuất.")

except FileNotFoundError:
    print(f"Lỗi: Không tìm thấy tệp '{html_file_path}'. Vui lòng kiểm tra lại đường dẫn.")
except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")