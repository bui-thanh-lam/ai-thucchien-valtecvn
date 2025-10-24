import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# --- Thiết lập Font ---
# Dòng này sẽ thiết lập font 'Lato' cho tất cả các thành phần văn bản trong biểu đồ.
# LƯU Ý: Bạn cần đảm bảo font 'Lato' đã được cài đặt trên máy tính của mình.
plt.rcParams['font.family'] = 'Lato'


# --- Dữ liệu tài chính ---
# Dữ liệu được trích xuất từ phân tích của bạn, làm tròn để trình bày
# Đơn vị: Nghìn tỷ VND cho 3 chỉ số đầu, % cho 2 chỉ số sau
data = {
    'Indicator': [
        'Tổng tài sản\n(Nghìn tỷ VND)',
        'Tiền gửi khách hàng\n(Nghìn tỷ VND)',
        'Lợi nhuận trước thuế\n(Nghìn tỷ VND)',
        'Tỷ lệ CASA\n(%)',
        'Tỷ lệ an toàn vốn (CAR)\n(%)'
    ],
    'value_2024': [908.3, 496.0, 15.6, 39.2, 14.5],
    'value_2025': [1037.6, 589.1, 15.1, 41.1, 15.0]
}
df = pd.DataFrame(data)

# --- Tùy chỉnh chung cho biểu đồ ---
sns.set_style("whitegrid")
colors = ['#BDBDBD', '#D32F2F'] # Màu xám cho năm cũ, màu đỏ cho năm mới nổi bật
bar_width = 0.6

def plot_single_chart(ax, indicator_data):
    """Hàm trợ giúp để vẽ một biểu đồ cột cho một chỉ số."""
    indicator = indicator_data['Indicator']
    val_2024 = indicator_data['value_2024']
    val_2025 = indicator_data['value_2025']

    # Vẽ các cột
    bars = ax.bar(['6T 2024', '6T 2025'], [val_2024, val_2025], color=colors, width=bar_width)

    # Thêm tiêu đề cho từng biểu đồ con
    ax.set_title(indicator, fontsize=16, weight='bold', pad=20)
    
    # Tinh chỉnh giao diện
    ax.tick_params(axis='x', labelsize=14, length=0)
    ax.grid(False, axis='x')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('lightgray')
    ax.get_yaxis().set_ticks([])

    # Hiển thị giá trị trên đỉnh mỗi cột
    for bar in bars:
        yval = bar.get_height()
        unit = '%' if '%' in indicator else ''
        label = f'{yval:,.1f}{unit}'
        # Điều chỉnh vị trí của nhãn giá trị
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + yval*0.02, label, 
                va='bottom', ha='center', fontsize=14, weight='bold', color=bar.get_facecolor())
    
    # Tăng giới hạn trục Y để có khoảng trống cho nhãn
    ax.set_ylim(0, ax.get_ylim()[1] * 1.15)


# --- Vẽ và lưu Hàng 1 ---
fig1, axes1 = plt.subplots(1, 2, figsize=(18, 6))
plot_single_chart(axes1[0], df.iloc[0])
plot_single_chart(axes1[1], df.iloc[1])

# Tiêu đề chính được làm nổi bật
# fig1.suptitle('So sánh các chỉ số tài chính nổi bật\n6 tháng đầu năm 2025 vs 2024', 
#               fontsize=28, weight='bold', y=1.0)
fig1.tight_layout(rect=[0, 0, 1, 0.9])
plt.savefig('chart_row_1.png', bbox_inches='tight')
plt.close(fig1)
print("Đã lưu 'chart_row_1.png'")


# --- Vẽ và lưu Hàng 2 ---
fig2, axes2 = plt.subplots(1, 2, figsize=(18, 6))
plot_single_chart(axes2[0], df.iloc[2])
plot_single_chart(axes2[1], df.iloc[3])
fig2.tight_layout()
plt.savefig('chart_row_2.png', bbox_inches='tight')
plt.close(fig2)
print("Đã lưu 'chart_row_2.png'")


# --- Vẽ và lưu Hàng 3 (biểu đồ đơn rộng hơn) ---
fig3 = plt.figure(figsize=(18, 6))
# Tạo một trục (axes) duy nhất chiếm 50% chiều rộng và được căn giữa
ax3 = fig3.add_axes([0.25, 0.1, 0.5, 0.8]) 
plot_single_chart(ax3, df.iloc[4])
plt.savefig('chart_row_3.png', bbox_inches='tight')
plt.close(fig3)
print("Đã lưu 'chart_row_3.png'")