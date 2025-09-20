#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞花令小程序
Author: AI Assistant
"""

import re
import random

class FeiHuaLing:
    def __init__(self):
        self.used_poems = set()  # 存储已使用的诗句
        self.target_char = ""    # 目标字符
        self.round_count = 0     # 回合数
        
        # 一些经典诗句示例，用于AI回复
        self.poem_database = {
            "春": [
                "春眠不觉晓，处处闻啼鸟",
                "春风又绿江南岸，明月何时照我还",
                "春色满园关不住，一枝红杏出墙来",
                "春花秋月何时了，往事知多少",
                "春蚕到死丝方尽，蜡炬成灰泪始干",
                "春江潮水连海平，海上明月共潮生",
                "春宵一刻值千金，花有清香月有阴",
                "春风得意马蹄疾，一日看尽长安花"
            ],
            "花": [
                "花间一壶酒，独酌无相亲",
                "花开堪折直须折，莫待无花空折枝",
                "花落知多少，夜来风雨声",
                "落红不是无情物，化作春泥更护花",
                "人面不知何处去，桃花依旧笑春风",
                "花谢花飞花满天，红消香断有谁怜",
                "梨花院落溶溶月，柳絮池塘淡淡风",
                "忽如一夜春风来，千树万树梨花开"
            ],
            "月": [
                "床前明月光，疑是地上霜",
                "月上柳梢头，人约黄昏后",
                "举头望明月，低头思故乡",
                "月落乌啼霜满天，江枫渔火对愁眠",
                "月黑雁飞高，单于夜遁逃",
                "今夜月明人尽望，不知秋思落谁家",
                "月儿弯弯照九州，几家欢乐几家愁",
                "海上生明月，天涯共此时"
            ],
            "水": [
                "问君能有几多愁，恰似一江春水向东流",
                "山重水复疑无路，柳暗花明又一村",
                "抽刀断水水更流，举杯消愁愁更愁",
                "落花有意流水无情",
                "青山不老，绿水长流",
                "仁者乐山，智者乐水",
                "水光潋滟晴方好，山色空蒙雨亦奇",
                "一水护田将绿绕，两山排闼送青来"
            ],
            "山": [
                "山重水复疑无路，柳暗花明又一村",
                "会当凌绝顶，一览众山小",
                "青山不老，绿水长流",
                "仁者乐山，智者乐水",
                "山不在高，有仙则名",
                "青山隐隐水迢迢，秋尽江南草未凋",
                "两岸青山相对出，孤帆一片日边来",
                "横看成岭侧成峰，远近高低各不同"
            ]
        }

    def is_valid_poem(self, text):
        """
        简单判断是否为诗词
        基本规则：
        1. 长度在4-20字之间
        2. 包含常见诗词标点或无标点
        3. 不包含明显的现代词汇
        """
        # 去除标点符号
        clean_text = re.sub(r'[，。！？；：、""''（）《》\s]', '', text)
        
        # 长度检查
        if len(clean_text) < 4 or len(clean_text) > 20:
            return False
        
        # 检查是否包含明显的现代词汇（简单检查）
        modern_words = ['电脑', '手机', '汽车', '飞机', '网络', '互联网', '微信', 'QQ', 
                       '淘宝', '支付宝', '股票', '房价', '996', '内卷', '躺平']
        for word in modern_words:
            if word in text:
                return False
        
        # 检查是否全是数字或字母
        if re.match(r'^[0-9a-zA-Z]+$', clean_text):
            return False
            
        return True

    def contains_target_char(self, text, target_char):
        """检查文本是否包含目标字符"""
        return target_char in text

    def is_duplicate(self, text):
        """检查是否为重复的诗句"""
        # 去除标点符号进行比较
        clean_text = re.sub(r'[，。！？；：、""''（）《》\s]', '', text)
        return clean_text in self.used_poems

    def add_used_poem(self, text):
        """添加已使用的诗句"""
        clean_text = re.sub(r'[，。！？；：、""''（）《》\s]', '', text)
        self.used_poems.add(clean_text)

    def get_ai_response(self):
        """AI回复一句诗"""
        if self.target_char in self.poem_database:
            available_poems = [poem for poem in self.poem_database[self.target_char] 
                             if not self.is_duplicate(poem)]
            if available_poems:
                return random.choice(available_poems)
        
        # 如果没有预设的诗句，返回一个通用回复
        return f"抱歉，我想不出更多含有'{self.target_char}'字的诗句了"

    def print_welcome(self):
        """打印欢迎信息"""
        print("=" * 50)
        print("🌸 欢迎来到飞花令小游戏 🌸")
        print("=" * 50)
        print("游戏规则：")
        print("1. 请先输入一个汉字作为飞花令的关键字")
        print("2. 轮流说出包含该字的诗句")
        print("3. 不能重复之前说过的诗句")
        print("4. 输入的必须是真正的诗词")
        print("5. 输入'结束'或'认输'可以退出游戏")
        print("=" * 50)

    def start_game(self):
        """开始游戏"""
        self.print_welcome()
        
        # 获取目标字符
        while True:
            self.target_char = input("\n请输入飞花令的关键字（一个汉字）：").strip()
            if len(self.target_char) == 1 and '\u4e00' <= self.target_char <= '\u9fff':
                break
            print("请输入一个有效的汉字！")
        
        print(f"\n🎯 本轮飞花令关键字：'{self.target_char}'")
        print("游戏开始！请你先来一句含有该字的诗词：")
        
        while True:
            self.round_count += 1
            print(f"\n--- 第 {self.round_count} 回合 ---")
            
            # 用户回合
            user_input = input(f"👤 你的诗句（含'{self.target_char}'字）：").strip()
            
            # 检查是否要结束游戏
            if user_input in ['结束', '认输', '退出', 'quit', 'exit']:
                print(f"\n🎊 游戏结束！共进行了 {self.round_count-1} 回合")
                print("感谢参与飞花令游戏！")
                break
            
            # 验证用户输入
            if not self.is_valid_poem(user_input):
                print("❌ 这不像是诗词，请重新输入一句真正的诗词！")
                self.round_count -= 1
                continue
            
            if not self.contains_target_char(user_input, self.target_char):
                print(f"❌ 你的诗句中没有包含'{self.target_char}'字，请重新输入！")
                self.round_count -= 1
                continue
            
            if self.is_duplicate(user_input):
                print("❌ 这句诗词之前已经说过了，请换一句！")
                self.round_count -= 1
                continue
            
            # 用户输入有效，记录下来
            self.add_used_poem(user_input)
            print(f"✅ 很好！'{user_input}'")
            
            # AI回合
            ai_poem = self.get_ai_response()
            if "抱歉" in ai_poem:
                print(f"\n🤖 {ai_poem}")
                print("🎊 你赢了！我想不出更多诗句了！")
                break
            else:
                print(f"\n🤖 我的诗句：{ai_poem}")
                self.add_used_poem(ai_poem)

def main():
    """主函数"""
    game = FeiHuaLing()
    
    try:
        game.start_game()
    except KeyboardInterrupt:
        print("\n\n游戏被中断，再见！")
    except Exception as e:
        print(f"\n游戏出现错误：{e}")
        print("请重新启动游戏")

if __name__ == "__main__":
    main()