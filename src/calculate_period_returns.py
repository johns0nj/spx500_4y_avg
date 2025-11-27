import pandas as pd
import numpy as np
import os

def calculate_period_returns():
    """计算各个时期的年化收益率"""
    # 确保 output 文件夹存在
    os.makedirs('output', exist_ok=True)
    
    # 读取处理后的数据
    input_path = os.path.join('output', 'spx500_processed.csv')
    df = pd.read_csv(input_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
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
    
    print("=" * 80)
    print("标普500各时期年化收益率分析")
    print("=" * 80)
    print(f"\n数据范围: {df['Date'].min().strftime('%Y-%m-%d')} 至 {df['Date'].max().strftime('%Y-%m-%d')}")
    print(f"共划分 {len(periods)} 个时期，每期约16年9个月\n")
    
    # 计算每个时期的收益率
    results = []
    for i, (start, end) in enumerate(periods):
        # 获取时期内的数据
        period_data = df[(df['Date'] >= start) & (df['Date'] <= end)]
        
        if len(period_data) < 2:
            continue
        
        # 获取起始和结束价格
        start_price = period_data['Close'].iloc[0]
        end_price = period_data['Close'].iloc[-1]
        
        # 计算总收益率
        total_return = (end_price / start_price - 1)
        
        # 计算实际年数
        actual_years = (period_data['Date'].iloc[-1] - period_data['Date'].iloc[0]).days / 365.25
        
        # 计算年化收益率
        if actual_years > 0:
            annual_return = (1 + total_return) ** (1/actual_years) - 1
        else:
            annual_return = 0
        
        results.append({
            '期数': i + 1,
            '起始日期': start.strftime('%Y-%m-%d'),
            '结束日期': end.strftime('%Y-%m-%d'),
            '起始价格': start_price,
            '结束价格': end_price,
            '总收益率': total_return,
            '实际年数': actual_years,
            '年化收益率': annual_return
        })
        
        # 打印详细信息
        print(f"第{i+1}期:")
        print(f"  时间范围: {start.strftime('%Y-%m-%d')} 至 {end.strftime('%Y-%m-%d')}")
        print(f"  实际年数: {actual_years:.2f}年")
        print(f"  起始价格: ${start_price:.2f}")
        print(f"  结束价格: ${end_price:.2f}")
        print(f"  总收益率: {total_return:+.2%}")
        print(f"  年化收益率: {annual_return:+.2%}")
        print()
    
    # 创建结果DataFrame
    results_df = pd.DataFrame(results)
    
    # 保存结果
    output_path = os.path.join('output', 'period_returns_analysis.csv')
    results_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print("=" * 80)
    print(f"详细结果已保存至 {output_path}")
    print("=" * 80)
    
    # 重点显示第2期和第4期
    print("\n" + "=" * 80)
    print("重点关注：第2期和第4期的年化收益率")
    print("=" * 80)
    
    if len(results) >= 2:
        period_2 = results[1]  # 索引1对应第2期
        print(f"\n【第2期】")
        print(f"  时间范围: {period_2['起始日期']} 至 {period_2['结束日期']}")
        print(f"  实际年数: {period_2['实际年数']:.2f}年")
        print(f"  起始价格: ${period_2['起始价格']:.2f}")
        print(f"  结束价格: ${period_2['结束价格']:.2f}")
        print(f"  总收益率: {period_2['总收益率']:+.2%}")
        print(f"  年化收益率: {period_2['年化收益率']:+.2%}")
    
    if len(results) >= 4:
        period_4 = results[3]  # 索引3对应第4期
        print(f"\n【第4期】")
        print(f"  时间范围: {period_4['起始日期']} 至 {period_4['结束日期']}")
        print(f"  实际年数: {period_4['实际年数']:.2f}年")
        print(f"  起始价格: ${period_4['起始价格']:.2f}")
        print(f"  结束价格: ${period_4['结束价格']:.2f}")
        print(f"  总收益率: {period_4['总收益率']:+.2%}")
        print(f"  年化收益率: {period_4['年化收益率']:+.2%}")
    
    print("\n" + "=" * 80)
    
    return results_df

if __name__ == "__main__":
    calculate_period_returns()


