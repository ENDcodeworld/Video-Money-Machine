"""
视频自动制作工具
将脚本转换为视频文件
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
import subprocess


class VideoMaker:
    """视频制作器"""
    
    def __init__(self, output_dir: str = './output'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 素材目录
        self.assets_dir = Path('./assets')
        self.assets_dir.mkdir(exist_ok=True)
        
        # 子目录
        (self.assets_dir / 'images').mkdir(exist_ok=True)
        (self.assets_dir / 'videos').mkdir(exist_ok=True)
        (self.assets_dir / 'audio').mkdir(exist_ok=True)
        (self.assets_dir / 'music').mkdir(exist_ok=True)
    
    def create_video_from_script(self, script: Dict, style: str = 'simple') -> str:
        """
        根据脚本创建视频
        
        Args:
            script: 视频脚本字典
            style: 视频风格 (simple/dynamic/cinematic)
            
        Returns:
            输出视频文件路径
        """
        print(f"🎬 正在制作视频: {script['title'][:30]}...")
        
        # 这里应该调用FFmpeg进行视频合成
        # 由于环境限制，这里生成制作指令文件
        
        output_file = self.output_dir / f"{script['title'][:20]}_{datetime.now().strftime('%H%M%S')}.mp4"
        
        # 生成制作指令
        instructions = self._generate_ffmpeg_command(script, output_file)
        
        # 保存指令文件
        cmd_file = self.output_dir / f"{output_file.stem}_command.txt"
        with open(cmd_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"  ✓ 制作指令已生成: {cmd_file}")
        print(f"  📁 预期输出: {output_file}")
        
        return str(output_file)
    
    def _generate_ffmpeg_command(self, script: Dict, output_file: Path) -> str:
        """生成FFmpeg命令"""
        cmd_parts = []
        
        # FFmpeg基础命令
        cmd_parts.append("ffmpeg -y")
        
        # 输入素材（图片/视频片段）
        # 这里应该根据脚本场景选择合适的素材
        for i, scene in enumerate(script['scenes']):
            # 假设每个场景对应一个图片或视频
            input_file = f"assets/images/scene_{i % 5}.jpg"  # 循环使用素材
            cmd_parts.append(f"-loop 1 -t {scene['duration']} -i {input_file}")
        
        # 音频输入
        cmd_parts.append("-i assets/music/background.mp3")
        
        # 复杂的filtergraph（简化版）
        filter_complex = self._build_filter_complex(script)
        cmd_parts.append(f"-filter_complex \"{filter_complex}\"")
        
        # 输出设置
        cmd_parts.append("-c:v libx264 -pix_fmt yuv420p")
        cmd_parts.append("-c:a aac -b:a 192k")
        cmd_parts.append(f"-shortest {output_file}")
        
        return " \\\n  ".join(cmd_parts)
    
    def _build_filter_complex(self, script: Dict) -> str:
        """构建FFmpeg filter complex"""
        filters = []
        
        # 为每个输入添加缩放和文字
        for i, scene in enumerate(script['scenes']):
            # 缩放滤镜
            filters.append(f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1[v{i}]")
        
        # 连接所有视频
        concat_input = "".join([f"[v{i}]" for i in range(len(script['scenes']))])
        filters.append(f"{concat_input}concat=n={len(script['scenes'])}:v=1:a=0[outv]")
        
        # 音频处理
        filters.append("[audio_input]volume=0.3[bgm]")
        
        return ";".join(filters)
    
    def batch_create_videos(self, scripts: List[Dict]) -> List[str]:
        """批量制作视频"""
        output_files = []
        
        print(f"\n🎬 开始批量制作 {len(scripts)} 个视频...")
        print("=" * 60)
        
        for i, script in enumerate(scripts, 1):
            print(f"\n[{i}/{len(scripts)}]")
            try:
                output_file = self.create_video_from_script(script)
                output_files.append(output_file)
            except Exception as e:
                print(f"  ❌ 制作失败: {e}")
        
        print("\n" + "=" * 60)
        print(f"✅ 批量制作完成！成功 {len(output_files)}/{len(scripts)}")
        
        return output_files
    
    def create_video_guide(self) -> str:
        """创建视频制作指南"""
        guide = """
# 视频制作指南

## 前置要求

1. 安装FFmpeg
   ```bash
   # Ubuntu/Debian
   sudo apt-get install ffmpeg
   
   # MacOS
   brew install ffmpeg
   
   # Windows
   # 下载：https://ffmpeg.org/download.html
   ```

2. 准备素材
   - 将图片放入 `assets/images/` 目录
   - 将背景音乐放入 `assets/music/` 目录
   - 建议图片尺寸：1080x1920 (9:16竖屏)

## 制作视频

### 方法一：使用生成的命令文件

```bash
# 进入项目目录
cd Video-Money-Machine

# 查看生成的命令
cat output/xxx_command.txt

# 复制命令并执行
# （注意：需要提前准备好素材文件）
```

### 方法二：使用Python自动制作

```python
from video_maker import VideoMaker

maker = VideoMaker()

# 制作单个视频
video_path = maker.create_video_from_script(script)

# 批量制作
video_paths = maker.batch_create_videos(scripts)
```

## 素材推荐

### 免费图片素材网站
- Unsplash: https://unsplash.com
- Pexels: https://pexels.com
- Pixabay: https://pixabay.com

### 免费音乐素材网站
- YouTube Audio Library
- Free Music Archive
- Bensound

## 视频规格建议

- **分辨率**: 1080x1920 (9:16竖屏)
- **帧率**: 30fps
- **编码**: H.264
- **音频**: AAC, 192kbps
- **时长**: 30-120秒

## 发布建议

### 最佳发布时间
- 早上 7:30-8:30
- 中午 12:00-13:00
- 傍晚 17:30-19:00
- 晚上 21:00-23:00

### 平台选择
1. **抖音** - 流量最大，变现方式多
2. **快手** - 下沉市场，带货效果好
3. **YouTube Shorts** - 国际平台，美元收益
4. **B站** - 年轻用户，知识内容受欢迎
5. **视频号** - 微信生态，私域转化好

## 变现方式

1. **平台分成** - 播放量收益
2. **带货佣金** - 商品橱窗
3. **广告接单** - 星图/蒲公英
4. **知识付费** - 课程/社群
5. **直播打赏** - 粉丝经济

---

💡 提示：没有素材也没关系！
可以使用以下替代方案：
1. AI生成图片 (Midjourney/Stable Diffusion)
2. 录屏 + 文字
3. 纯文字动画视频
4. 混剪素材 (注意版权)
"""
        
        guide_file = self.output_dir / 'VIDEO_GUIDE.md'
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide)
        
        return str(guide_file)


class PlatformPublisher:
    """平台发布工具"""
    
    def __init__(self):
        self.platforms = {
            'douyin': '抖音',
            'kuaishou': '快手',
            'youtube': 'YouTube',
            'bilibili': 'B站',
            'weixin': '视频号'
        }
    
    def generate_publish_guide(self, video_file: str, script: Dict) -> Dict:
        """生成各平台发布指南"""
        guides = {}
        
        for platform_id, platform_name in self.platforms.items():
            guide = self._adapt_for_platform(video_file, script, platform_id)
            guides[platform_id] = guide
        
        return guides
    
    def _adapt_for_platform(self, video_file: str, script: Dict, platform: str) -> Dict:
        """适配不同平台"""
        
        base_info = {
            'video_file': video_file,
            'title': script['title'],
            'description': '',
            'tags': script['tags'],
            'cover_time': 1.0,  # 封面时间点
        }
        
        if platform == 'douyin':
            base_info.update({
                'title': f"#{script['topic']} {script['title']}",
                'description': f"{script['title']}\\n\\n{script['scenes'][-1]['text']}\\n\\n#{script['category']} #{script['topic']} #热门 #推荐",
                'tags': script['tags'][:5],
                'privacy': 'public',
                'allow_download': True,
                'allow_duet': True
            })
        
        elif platform == 'kuaishou':
            base_info.update({
                'description': f"{script['title']}\\n\\n{script['scenes'][-1]['text']}",
                'location': '热门地点',
                'visibility': 'public'
            })
        
        elif platform == 'youtube':
            base_info.update({
                'title': script['title'] + ' | Shorts',
                'description': f"{script['title']}\\n\\n{chr(10).join([s['text'] for s in script['scenes']])}\\n\\n#Shorts {' '.join(['#' + t for t in script['tags']])}",
                'category': 'Entertainment',
                'privacy': 'public',
                'made_for_kids': False
            })
        
        elif platform == 'bilibili':
            base_info.update({
                'title': script['title'],
                'description': f"{script['title']}\\n\\n{script['scenes'][-1]['text']}\\n\\n点赞关注，持续更新！",
                'tags': script['tags'][:10],
                'copyright': 1,  # 原创
                'tid': 174  # 生活-其他
            })
        
        elif platform == 'weixin':
            base_info.update({
                'description': script['title'],
                'visibility': 'public'
            })
        
        return base_info
    
    def export_publish_scripts(self, guides: Dict, output_dir: str):
        """导出发布脚本"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        for platform, guide in guides.items():
            file_path = output_path / f"publish_{platform}.txt"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {self.platforms.get(platform, platform)} 发布指南\\n\\n")
                f.write(f"视频文件: {guide['video_file']}\\n")
                f.write(f"标题: {guide['title']}\\n\\n")
                f.write(f"描述:\\n{guide['description']}\\n\\n")
                f.write(f"标签: {', '.join(guide['tags'])}\\n")
            
            print(f"  ✓ 已导出: {file_path}")


if __name__ == '__main__':
    from datetime import datetime
    
    print("=" * 60)
    print("🎬 视频制作工具测试")
    print("=" * 60)
    
    # 创建制作器
    maker = VideoMaker()
    
    # 创建制作指南
    print("\n📖 生成视频制作指南...")
    guide_file = maker.create_video_guide()
    print(f"  ✓ 指南已生成: {guide_file}")
    
    # 测试生成发布指南
    print("\n📤 测试发布指南生成...")
    
    test_script = {
        'title': '测试视频标题',
        'topic': '测试主题',
        'category': 'knowledge',
        'scenes': [
            {'type': 'hook', 'text': '开场钩子', 'duration': 4},
            {'type': 'body', 'text': '正文内容', 'duration': 10},
            {'type': 'cta', 'text': '引导关注', 'duration': 4}
        ],
        'tags': ['测试', '知识', '热门']
    }
    
    publisher = PlatformPublisher()
    guides = publisher.generate_publish_guide('output/test_video.mp4', test_script)
    
    print("\n各平台发布信息:")
    for platform, guide in guides.items():
        print(f"  {platform}: {guide['title'][:30]}...")
    
    # 导出发布脚本
    print("\n💾 导出发布脚本...")
    publisher.export_publish_scripts(guides, './output/publish_guides')
    
    print("\n" + "=" * 60)
    print("✅ 视频制作工具测试完成！")
    print("=" * 60)
    print("\n📋 下一步:")
    print("  1. 安装FFmpeg")
    print("  2. 准备素材文件")
    print("  3. 运行制作命令")
    print("  4. 上传到各平台")
