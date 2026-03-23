#!/usr/bin/env python3
"""
短视频赚钱机器 - 一键运行
自动生成短视频内容，制作视频，规划发布
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from video_engine import VideoContentGenerator, VideoProductionPlanner
from video_maker import VideoMaker, PlatformPublisher


def print_banner():
    """打印启动画面"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║           🎬 短视频赚钱机器 🎬                          ║
    ║     Video Money Machine v1.0                           ║
    ║                                                          ║
    ║     自动生成脚本 → 制作视频 → 多平台分发              ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    parser = argparse.ArgumentParser(description='短视频赚钱机器 - 自动化短视频生产系统')
    parser.add_argument('-n', '--count', type=int, default=5,
                       help='生成视频数量 (默认: 5)')
    parser.add_argument('--make-video', action='store_true',
                       help='生成视频制作命令')
    parser.add_argument('--plan', action='store_true',
                       help='生成发布计划')
    parser.add_argument('-o', '--output', type=str, default='./output',
                       help='输出目录 (默认: ./output)')
    parser.add_argument('--views', type=int, default=5000,
                       help='预估单视频播放量 (默认: 5000)')
    
    args = parser.parse_args()
    
    # 打印启动画面
    print_banner()
    
    # 创建输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    # 初始化组件
    print("\n🔧 正在初始化短视频赚钱机器...")
    generator = VideoContentGenerator()
    planner = VideoProductionPlanner()
    maker = VideoMaker(output_dir)
    
    # 1. 批量生成脚本
    print(f"\n🎯 正在生成 {args.count} 个视频脚本...")
    print("=" * 60)
    
    scripts = generator.batch_generate_scripts(args.count)
    
    # 保存脚本
    scripts_file = output_dir / 'video_scripts.json'
    with open(scripts_file, 'w', encoding='utf-8') as f:
        json.dump(scripts, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 脚本已保存: {scripts_file}")
    
    # 2. 生成视频制作命令（可选）
    if args.make_video:
        print("\n" + "=" * 60)
        print("🎬 正在生成视频制作命令...")
        print("=" * 60)
        
        video_commands_dir = output_dir / 'video_commands'
        video_commands_dir.mkdir(exist_ok=True)
        
        for i, script in enumerate(scripts, 1):
            print(f"\n[{i}/{len(scripts)}] {script['title'][:30]}...")
            try:
                output_file = maker.create_video_from_script(script)
            except Exception as e:
                print(f"  ⚠️ 跳过: {e}")
        
        # 生成视频制作指南
        guide_file = maker.create_video_guide()
        print(f"\n📖 视频制作指南: {guide_file}")
    
    # 3. 生成发布计划（可选）
    if args.plan:
        print("\n" + "=" * 60)
        print("📅 正在生成发布计划...")
        print("=" * 60)
        
        # 一周计划
        weekly_plan = planner.create_weekly_plan(videos_per_day=args.count)
        
        plan_file = output_dir / 'publish_plan.json'
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(weekly_plan, f, ensure_ascii=False, indent=2)
        
        print(f"\n📅 一周发布计划:")
        for day_plan in weekly_plan[:3]:  # 只显示前3天
            print(f"\n  {day_plan['date']} ({day_plan['weekday']}):")
            for item in day_plan['schedule'][:3]:  # 每天前3个
                print(f"    {item['time']} - {item['category']}")
        
        print(f"\n💾 完整计划已保存: {plan_file}")
        
        # 生成发布指南
        print("\n📤 正在生成各平台发布指南...")
        publisher = PlatformPublisher()
        
        for i, script in enumerate(scripts[:3], 1):  # 只处理前3个
            print(f"\n  视频 {i}: {script['title'][:30]}...")
            guides = publisher.generate_publish_guide(f"video_{i}.mp4", script)
            
            publish_dir = output_dir / f'publish_guide_{i}'
            publisher.export_publish_scripts(guides, publish_dir)
    
    # 4. 收益预估
    print("\n" + "=" * 60)
    print("💰 收益预估")
    print("=" * 60)
    
    revenue = generator.estimate_revenue(args.count, args.views)
    
    print(f"\n📊 生成视频数: {revenue['video_count']}")
    print(f"📊 预估总播放: {revenue['total_views']:,}")
    print(f"💰 预估总收益: ¥{revenue['total_revenue']}")
    print(f"💰 单视频收益: ¥{revenue['per_video']}")
    
    print("\n📈 各平台收益分布:")
    for platform, amount in revenue['breakdown'].items():
        percentage = (amount / revenue['total_revenue']) * 100 if revenue['total_revenue'] > 0 else 0
        print(f"  {platform:12s}: ¥{amount:8.2f} ({percentage:5.1f}%)")
    
    # 月度预测
    monthly_revenue = revenue['total_revenue'] * 30
    print(f"\n🚀 如果每天发布 {args.count} 个视频:")
    print(f"   预估月收益: ¥{monthly_revenue:.2f}")
    print(f"   预估年收益: ¥{monthly_revenue * 12:.2f}")
    
    # 完成提示
    print("\n" + "=" * 60)
    print("🎉 运行完成！")
    print("=" * 60)
    
    print(f"\n📁 所有文件已保存到: {output_dir.absolute()}")
    
    print("\n📋 下一步行动:")
    print("  1. 查看生成的脚本: video_scripts.json")
    if args.make_video:
        print("  2. 按照 video_commands 目录的命令制作视频")
        print("  3. 查看 VIDEO_GUIDE.md 了解制作流程")
    if args.plan:
        print("  4. 按照 publish_plan.json 的计划发布视频")
        print("  5. 使用各平台的 publish_guide 发布")
    
    print("\n💡 赚钱提示:")
    print("  • 每天坚持发布，量变引起质变")
    print("  • 关注数据，优化内容方向")
    print("  • 多平台分发，最大化收益")
    print("  • 与粉丝互动，提高粘性")
    
    print("\n" + "=" * 60)
    print("🚀 开始你的短视频赚钱之旅吧！")
    print("=" * 60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断运行")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
