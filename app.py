#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞花令Web应用 - 集成外部API版本
Author: AI Assistant
"""

from flask import Flask, render_template, request, jsonify, session
import re
import random
import requests
import json
import time

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'feihualing_secret_key_2024'

class FeiHuaLingWeb:
    def __init__(self):
        # 外部API配置
        self.apis = {
            'saintic': {
                'base_url': 'https://hub.saintic.com/openservice/sentence',
                'search_endpoint': '/all.json',
                'available': True
            },
            'freeapi': {
                'base_url': 'https://www.51biu.cn/api',
                'search_endpoint': '/poetry',
                'available': True
            }
        }
        
        # 备用本地诗句库（当API不可用时使用）
        self.fallback_poems = {
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
                "落红不是无情物，化作春泥更护花",
                "人面不知何处去，桃花依旧笑春风",
                "忽如一夜春风来，千树万树梨花开",
                "花谢花飞花满天，红消香断有谁怜",
                "梨花院落溶溶月，柳絮池塘淡淡风",
                "感时花溅泪，恨别鸟惊心"
            ],
            "月": [
                "床前明月光，疑是地上霜",
                "举头望明月，低头思故乡",
                "海上生明月，天涯共此时",
                "明月几时有，把酒问青天",
                "月上柳梢头，人约黄昏后",
                "月落乌啼霜满天，江枫渔火对愁眠",
                "今夜月明人尽望，不知秋思落谁家",
                "月下飞天镜，云生结海楼"
            ],
            "水": [
                "问君能有几多愁，恰似一江春水向东流",
                "山重水复疑无路，柳暗花明又一村",
                "桃花潭水深千尺，不及汪伦送我情",
                "水光潋滟晴方好，山色空蒙雨亦奇",
                "黄河之水天上来，奔流到海不复回",
                "抽刀断水水更流，举杯消愁愁更愁",
                "落花有意流水无情",
                "一水护田将绿绕，两山排闼送青来"
            ],
            "雪": [
                "窗含西岭千秋雪，门泊东吴万里船",
                "北国风光，千里冰封，万里雪飘",
                "雪似梅花，梅花似雪，似和不似都奇绝",
                "柴门闻犬吠，风雪夜归人",
                "孤舟蓑笠翁，独钓寒江雪",
                "梅须逊雪三分白，雪却输梅一段香",
                "燕山雪花大如席，片片吹落轩辕台",
                "欲渡黄河冰塞川，将登太行雪满山"
            ],
            "山": [
                "山重水复疑无路，柳暗花明又一村",
                "会当凌绝顶，一览众山小",
                "青山不老，绿水长流",
                "仁者乐山，智者乐水",
                "山不在高，有仙则名",
                "两岸青山相对出，孤帆一片日边来",
                "横看成岭侧成峰，远近高低各不同",
                "白日依山尽，黄河入海流"
            ],
            "风": [
                "春风又绿江南岸，明月何时照我还",
                "忽如一夜春风来，千树万树梨花开",
                "春风得意马蹄疾，一日看尽长安花",
                "随风潜入夜，润物细无声",
                "风急天高猿啸哀，渚清沙白鸟飞回",
                "长风破浪会有时，直挂云帆济沧海",
                "风萧萧兮易水寒，壮士一去兮不复还",
                "东风不与周郎便，铜雀春深锁二乔"
            ],
            "雨": [
                "夜来风雨声，花落知多少",
                "好雨知时节，当春乃发生",
                "清明时节雨纷纷，路上行人欲断魂",
                "空山新雨后，天气晚来秋",
                "黄梅时节家家雨，青草池塘处处蛙",
                "山河破碎风飘絮，身世浮沉雨打萍",
                "君问归期未有期，巴山夜雨涨秋池",
                "七八个星天外，两三点雨山前"
            ],
            "江": [
                "孤帆远影碧空尽，唯见长江天际流",
                "大江东去，浪淘尽，千古风流人物",
                "江山如此多娇，引无数英雄竞折腰",
                "星垂平野阔，月涌大江流",
                "无边落木萧萧下，不尽长江滚滚来",
                "江南好，风景旧曾谙",
                "日出江花红胜火，春来江水绿如蓝",
                "一江春水向东流"
            ],
            "秋": [
                "自古逢秋悲寂寥，我言秋日胜春朝",
                "停车坐爱枫林晚，霜叶红于二月花",
                "秋风萧瑟，洪波涌起",
                "秋水共长天一色，落霞与孤鹜齐飞",
                "君问归期未有期，巴山夜雨涨秋池",
                "银烛秋光冷画屏，轻罗小扇扑流萤",
                "无边落木萧萧下，不尽长江滚滚来",
                "秋风起兮白云飞，草木黄落兮雁南归"
            ]
        }

    def is_valid_poem(self, text):
        """判断是否为诗词 - 增强版验证"""
        clean_text = re.sub(r'[，。！？；：、""''（）《》\s]', '', text)
        
        # 基本长度检查
        if len(clean_text) < 4 or len(clean_text) > 30:
            return False
        
        # 现代词汇过滤
        modern_words = ['电脑', '手机', '汽车', '飞机', '网络', '互联网', '微信', 'QQ', 
                       '淘宝', '支付宝', '股票', '房价', '996', '内卷', '躺平', '打工', 
                       '上班', '下班', '加班', '电视', '空调', '冰箱', '高铁', '地铁',
                       '公交', '快递', '外卖', '直播', '短视频', '抖音', '朋友圈']
        for word in modern_words:
            if word in text:
                return False
        
        # 纯数字/字母过滤
        if re.match(r'^[0-9a-zA-Z]+$', clean_text):
            return False
        
        # 新增：重复字符检查
        # 检查是否有过多重复的单个字符
        for char in set(clean_text):
            char_count = clean_text.count(char)
            # 如果单个字符出现次数超过总长度的50%，很可能不是诗词
            if char_count > len(clean_text) * 0.5:
                return False
            # 如果单个字符连续出现超过2次，很可能不是诗词
            if char + char + char in clean_text:
                return False
        
        # 新增：检查是否有异常的重复模式
        # 像"花花几花花"这样的重复模式
        if len(clean_text) <= 6:
            # 对于短文本，检查是否有明显的重复模式
            if len(set(clean_text)) < len(clean_text) * 0.6:  # 去重后字符数太少
                return False
        
        # 新增：检查明显的无意义组合
        meaningless_patterns = [
            r'(.)\1{2,}',  # 同一字符连续出现3次以上
            r'^(.)\1+$',   # 整个文本只有重复的单个字符
            r'^(.{1,2})\1+$',  # 短序列的重复（如"花花几花花"中的"花花"重复）
        ]
        
        for pattern in meaningless_patterns:
            if re.search(pattern, clean_text):
                return False
        
        return True

    def contains_target_char(self, text, target_char):
        """检查是否包含目标字符"""
        return target_char in text

    def clean_poem_text(self, text):
        """清理诗句文本用于比较"""
        return re.sub(r'[，。！？；：、""''（）《》\s]', '', text)

    def search_poems_from_api(self, target_char, used_poems, max_attempts=5):
        """从API搜索包含目标字符的诗句（优化版）"""
        found_poems = []
        
        # 1. 优先尝试 freeapi，因为它支持搜索，效率更高
        try:
            if self.apis['freeapi']['available']:
                poems = self._search_freeapi(target_char, used_poems)
                if poems:
                    found_poems.extend(poems)
        except Exception as e:
            print(f"API freeapi 调用失败: {e}")

        # 2. 如果 freeapi 没找到足够诗句，再尝试 saintic 作为补充
        if len(found_poems) < 3:
            try:
                if self.apis['saintic']['available']:
                    poems = self._search_saintic_api(target_char, used_poems)
                    if poems:
                        found_poems.extend(poems)
            except Exception as e:
                print(f"API saintic 调用失败: {e}")
        
        return found_poems

    def _search_freeapi(self, target_char, used_poems):
        """搜索freeapi"""
        try:
            url = f"{self.apis['freeapi']['base_url']}{self.apis['freeapi']['search_endpoint']}"
            params = {
                'content': target_char,
                'size': 10,
                'page': 1
            }
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200 and data.get('data'):
                    poems = []
                    for item in data['data']:
                        content = item.get('content', '').strip()
                        if content and self.contains_target_char(content, target_char):
                            # 提取诗句（取第一句或第二句）
                            lines = [line.strip() for line in content.split('\n') if line.strip()]
                            for line in lines:
                                if (self.contains_target_char(line, target_char) and 
                                    self.is_valid_poem(line) and
                                    self.clean_poem_text(line) not in used_poems):
                                    poems.append(line)
                                    if len(poems) >= 5:
                                        break
                            if len(poems) >= 5:
                                break
                    return poems
        except Exception as e:
            print(f"Freeapi搜索失败: {e}")
        return []

    def _search_saintic_api(self, target_char, used_poems):
        """搜索SaintIC古诗词API"""
        try:
            poems = []
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # 尝试多次获取随机诗句，提高命中概率
            for attempt in range(15):  # 尝试15次获取随机诗句
                url = f"{self.apis['saintic']['base_url']}{self.apis['saintic']['search_endpoint']}"
                response = requests.get(url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and data.get('data'):
                        poem_text = data['data'].get('text', '').strip()
                        if (poem_text and 
                            self.contains_target_char(poem_text, target_char) and 
                            self.is_valid_poem(poem_text) and
                            self.clean_poem_text(poem_text) not in used_poems):
                            poems.append(poem_text)
                            print(f"✅ SaintIC API找到包含'{target_char}'的诗句: {poem_text}")
                            if len(poems) >= 3:
                                return poems
                
                time.sleep(0.1)  # 避免请求过快
                
        except Exception as e:
            print(f"SaintIC API搜索失败: {e}")
        return poems

    def get_ai_response(self, target_char, used_poems):
        """AI回复诗句 - 优先从API搜索，备用本地诗句"""
        # 首先尝试从API搜索
        api_poems = self.search_poems_from_api(target_char, used_poems)
        
        if api_poems:
            # 随机选择一首API找到的诗句
            available_poems = [poem for poem in api_poems 
                             if self.clean_poem_text(poem) not in used_poems]
            if available_poems:
                return random.choice(available_poems)
        
        # API搜索失败，使用备用本地诗句库
        if target_char in self.fallback_poems:
            available_poems = []
            for poem in self.fallback_poems[target_char]:
                clean_poem = self.clean_poem_text(poem)
                if clean_poem not in used_poems:
                    available_poems.append(poem)
            
            if available_poems:
                return random.choice(available_poems)
        
        # 尝试从所有诗句中寻找包含目标字符的
        for char, poems in self.fallback_poems.items():
            for poem in poems:
                if (self.contains_target_char(poem, target_char) and 
                    self.clean_poem_text(poem) not in used_poems):
                    return poem
        
        # 都没有找到，返回None表示AI认输
        return None

# 创建游戏实例
game = FeiHuaLingWeb()

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    """开始游戏"""
    data = request.json
    target_char = data.get('target_char', '').strip()
    
    # 验证输入
    if len(target_char) != 1 or not ('\u4e00' <= target_char <= '\u9fff'):
        return jsonify({'success': False, 'message': '请输入一个有效的汉字！'})
    
    # 初始化游戏状态
    session['target_char'] = target_char
    session['used_poems'] = []
    session['round_count'] = 0
    session['game_history'] = []
    
    return jsonify({
        'success': True, 
        'target_char': target_char,
        'message': f'游戏开始！飞花令关键字是：{target_char}（AI将通过网络搜索诗词与你对战）'
    })

@app.route('/submit_poem', methods=['POST'])
def submit_poem():
    """提交用户诗句"""
    data = request.json
    user_poem = data.get('poem', '').strip()
    target_char = session.get('target_char')
    used_poems = session.get('used_poems', [])
    
    if not target_char:
        return jsonify({'success': False, 'message': '游戏尚未开始！'})
    
    # 验证诗句
    if not game.is_valid_poem(user_poem):
        return jsonify({'success': False, 'message': '这不像是诗词，请输入真正的诗句！'})
    
    if not game.contains_target_char(user_poem, target_char):
        return jsonify({'success': False, 'message': f'诗句中没有包含"{target_char}"字，请重新输入！'})
    
    clean_user_poem = game.clean_poem_text(user_poem)
    if clean_user_poem in used_poems:
        return jsonify({'success': False, 'message': '这句诗词之前已经说过了，请换一句！'})
    
    # 用户诗句有效，添加到已使用列表
    used_poems.append(clean_user_poem)
    session['used_poems'] = used_poems
    session['round_count'] = session.get('round_count', 0) + 1
    
    # 记录游戏历史
    game_history = session.get('game_history', [])
    game_history.append({
        'round': session['round_count'],
        'user_poem': user_poem,
        'ai_poem': None
    })
    
    # AI回复 - 通过网络API搜索
    ai_poem = game.get_ai_response(target_char, used_poems)
    
    if ai_poem:
        # AI找到了诗句
        clean_ai_poem = game.clean_poem_text(ai_poem)
        used_poems.append(clean_ai_poem)
        session['used_poems'] = used_poems
        
        game_history[-1]['ai_poem'] = ai_poem
        session['game_history'] = game_history
        
        return jsonify({
            'success': True,
            'user_poem': user_poem,
            'ai_poem': ai_poem,
            'round': session['round_count'],
            'game_continues': True,
            'message': '✨ AI通过网络搜索找到了诗句！'
        })
    else:
        # AI认输
        session['game_history'] = game_history
        return jsonify({
            'success': True,
            'user_poem': user_poem,
            'ai_poem': None,
            'round': session['round_count'],
            'game_continues': False,
            'message': f'🎊 AI在网络上也找不到更多含有"{target_char}"字的诗句了，你赢了！'
        })

@app.route('/end_game', methods=['POST'])
def end_game():
    """结束游戏"""
    round_count = session.get('round_count', 0)
    target_char = session.get('target_char', '')
    
    # 清除游戏状态
    session.pop('target_char', None)
    session.pop('used_poems', None)
    session.pop('round_count', None)
    session.pop('game_history', None)
    
    return jsonify({
        'success': True,
        'message': f'游戏结束！共进行了 {round_count} 回合，关键字是"{target_char}"'
    })

@app.route('/api_status', methods=['GET'])
def api_status():
    """检查API状态"""
    status = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for api_name, api_config in game.apis.items():
        try:
            if api_name == 'saintic':
                response = requests.get(f"{api_config['base_url']}/all.json", headers=headers, timeout=3)
                status[api_name] = response.status_code == 200
            elif api_name == 'freeapi':
                response = requests.get(f"{api_config['base_url']}/poetry?size=1", timeout=3)
                status[api_name] = response.status_code == 200
        except:
            status[api_name] = False
    
    return jsonify({'api_status': status})

if __name__ == '__main__':
    # 启动时检查API状态
    print("正在检查诗词API状态...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for api_name, api_config in game.apis.items():
        try:
            if api_name == 'saintic':
                response = requests.get(f"{api_config['base_url']}/all.json", headers=headers, timeout=5)
                if response.status_code == 200:
                    print(f"✅ {api_name} API 可用")
                else:
                    print(f"❌ {api_name} API 不可用")
                    game.apis[api_name]['available'] = False
            elif api_name == 'freeapi':
                response = requests.get(f"{api_config['base_url']}/poetry?size=1", timeout=5)
                if response.status_code == 200:
                    print(f"✅ {api_name} API 可用")
                else:
                    print(f"❌ {api_name} API 不可用")
                    game.apis[api_name]['available'] = False
        except Exception as e:
            print(f"❌ {api_name} API 连接失败: {e}")
            game.apis[api_name]['available'] = False
    
    print("飞花令Web应用启动中...")
    app.run(debug=True, host='0.0.0.0', port=5000) 