import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import matplotlib.dates as mdates
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def read_spx500_data(filename):
    """读取标普500数据"""
    try:
        # 读取Excel文件
        df = pd.read_excel(filename)
        
        # 由于列名是日期和价格，我们需要重新整理数据
        # 第一列是日期，第二列是价格
        df.columns = ['Date', 'Close']
        
        # 确保日期列是datetime类型
        df['Date'] = pd.to_datetime(df['Date'])
        
        # 按日期排序
        df = df.sort_values('Date').reset_index(drop=True)
        
        # 删除任何包含NaN的行
        df = df.dropna()
        
        print(f"数据范围: {df['Date'].min()} 到 {df['Date'].max()}")
        print(f"总数据点数: {len(df)}")
        
        return df
        
    except Exception as e:
        print(f"读取数据时出错: {e}")
        return None

def calculate_4year_ma(df):
    """计算4年均线（约1460个交易日）"""
    # 4年大约有1460个交易日（365*4*0.6，考虑到周末和节假日）
    df['MA_4Y'] = df['Close'].rolling(window=1460, min_periods=1).mean()
    return df

def create_visualization(df):
    """创建可视化图表"""
    # 创建图形和子图
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 14))
    
    # 计算16年9个月的时间段
    start_date = df['Date'].min()
    period_days = 16 * 365.25 + 9 * 30.44  # 16年9个月的天数
    periods = []
    current_date = start_date
    
    while current_date < df['Date'].max():
        end_date = current_date + pd.Timedelta(days=period_days)
        if end_date > df['Date'].max():
            end_date = df['Date'].max()
        periods.append((current_date, end_date))
        current_date = end_date
    
    print(f"共划分了 {len(periods)} 个时间段")
    
    # 上图：收盘价和4年均线
    ax1.plot(df['Date'], df['Close'], label='标普500收盘价', linewidth=0.8, alpha=0.8, color='blue')
    ax1.plot(df['Date'], df['MA_4Y'], label='4年均线', linewidth=2, color='red')
    
    # 添加时间段分割线和标注
    colors = ['lightgray', 'lightblue', 'lightgreen', 'lightyellow', 'lightpink', 'lightcyan']
    for i, (start, end) in enumerate(periods):
        color = colors[i % len(colors)]
        ax1.axvspan(start, end, alpha=0.2, color=color)
        
        # 添加时间段标注
        mid_date = start + (end - start) / 2
        period_label = f"第{i+1}期\n{start.strftime('%Y-%m')} 至 {end.strftime('%Y-%m')}"
        ax1.text(mid_date, ax1.get_ylim()[1] * 0.9, period_label, 
                ha='center', va='top', fontsize=8, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.7))
        
        # 添加明显的垂直分割线（从1930年开始，每16年9个月一条）
        ax1.axvline(x=start, color='red', linestyle='-', alpha=0.8, linewidth=2.5, zorder=5)
        ax1.text(start, ax1.get_ylim()[1] * 0.98, start.strftime('%Y-%m-%d'), 
                ha='left', va='top', fontsize=7, rotation=0, 
                bbox=dict(boxstyle="round,pad=0.2", facecolor='white', edgecolor='red', alpha=0.8))
    
    ax1.set_title('标普500历史收盘价与4年均线 (按16年9个月划分)', fontsize=16, fontweight='bold')
    ax1.set_ylabel('价格', fontsize=12)
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # 设置x轴格式
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax1.xaxis.set_major_locator(mdates.YearLocator(5))  # 每5年显示一个刻度
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    # 下图：对数价格（更好地显示长期趋势）
    ax2.semilogy(df['Date'], df['Close'], label='标普500收盘价(对数)', linewidth=0.8, alpha=0.8, color='blue')
    ax2.semilogy(df['Date'], df['MA_4Y'], label='4年均线(对数)', linewidth=2, color='red')
    
    # 添加时间段分割线和标注（对数图）
    for i, (start, end) in enumerate(periods):
        color = colors[i % len(colors)]
        ax2.axvspan(start, end, alpha=0.2, color=color)
        
        # 添加时间段标注
        mid_date = start + (end - start) / 2
        period_label = f"第{i+1}期\n{start.strftime('%Y-%m')} 至 {end.strftime('%Y-%m')}"
        ax2.text(mid_date, ax2.get_ylim()[1] * 0.7, period_label, 
                ha='center', va='top', fontsize=8, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.7))
        
        # 添加明显的垂直分割线（从1930年开始，每16年9个月一条）
        ax2.axvline(x=start, color='red', linestyle='-', alpha=0.8, linewidth=2.5, zorder=5)
        ax2.text(start, ax2.get_ylim()[1] * 0.95, start.strftime('%Y-%m-%d'), 
                ha='left', va='top', fontsize=7, rotation=0, 
                bbox=dict(boxstyle="round,pad=0.2", facecolor='white', edgecolor='red', alpha=0.8))
    
    ax2.set_title('标普500历史收盘价与4年均线 (对数坐标，按16年9个月划分)', fontsize=16, fontweight='bold')
    ax2.set_xlabel('年份', fontsize=12)
    ax2.set_ylabel('价格 (对数)', fontsize=12)
    ax2.legend(fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # 设置x轴格式
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax2.xaxis.set_major_locator(mdates.YearLocator(5))
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    
    # 调整布局
    plt.tight_layout()
    
    # 确保 output 文件夹存在
    os.makedirs('output', exist_ok=True)
    
    # 保存图表
    output_path = os.path.join('output', 'spx500_4year_ma_periods.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"图表已保存为 {output_path}")
    
    # 显示图表
    plt.show()
    
    return fig, periods

def print_statistics(df):
    """打印统计信息"""
    print("\n=== 标普500数据统计 ===")
    print(f"数据开始日期: {df['Date'].min().strftime('%Y-%m-%d')}")
    print(f"数据结束日期: {df['Date'].max().strftime('%Y-%m-%d')}")
    print(f"总交易日数: {len(df)}")
    print(f"最高收盘价: ${df['Close'].max():.2f}")
    print(f"最低收盘价: ${df['Close'].min():.2f}")
    print(f"当前收盘价: ${df['Close'].iloc[-1]:.2f}")
    print(f"当前4年均线: ${df['MA_4Y'].iloc[-1]:.2f}")
    
    # 计算年化收益率
    years = (df['Date'].max() - df['Date'].min()).days / 365.25
    total_return = (df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1
    annual_return = (1 + total_return) ** (1/years) - 1
    print(f"总收益率: {total_return:.2%}")
    print(f"年化收益率: {annual_return:.2%}")

def main():
    """主函数"""
    print("正在读取标普500数据...")
    
    # 确保 input 文件夹存在
    os.makedirs('input', exist_ok=True)
    
    # 读取数据
    input_path = os.path.join('input', 'spx500_1930td.xlsx')
    df = read_spx500_data(input_path)
    
    if df is not None:
        # 计算4年均线
        df = calculate_4year_ma(df)
        
        # 打印统计信息
        print_statistics(df)
        
        # 创建可视化
        print("\n正在生成可视化图表...")
        fig, periods = create_visualization(df)
        
        # 打印时间段信息
        print("\n=== 时间段划分详情 ===")
        for i, (start, end) in enumerate(periods):
            duration = end - start
            years = duration.days / 365.25
            print(f"第{i+1}期: {start.strftime('%Y-%m-%d')} 至 {end.strftime('%Y-%m-%d')} (约{years:.1f}年)")
        
        # 确保 output 文件夹存在
        os.makedirs('output', exist_ok=True)
        
        # 保存处理后的数据
        output_path = os.path.join('output', 'spx500_processed.csv')
        df.to_csv(output_path, index=False)
        print(f"处理后的数据已保存为 {output_path}")
        
    else:
        print("无法读取数据文件")

if __name__ == "__main__":
    main()
