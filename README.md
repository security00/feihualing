# 🌸 飞花令 - 中国传统诗词游戏 Web版

一个基于Flask开发的飞花令在线游戏，让您与AI进行诗词对战，体验中国传统文化的魅力。

## ✨ 功能特点

- 🎮 **在线对战** - 与AI进行实时诗词对战
- 🌐 **智能搜索** - AI通过网络API搜索真实的古诗词
- 📚 **丰富诗库** - 内置春、花、月、水、山、风、雨、江、秋等常见字的诗句库
- ✅ **智能验证** - 自动验证诗句有效性，过滤现代词汇
- 🎨 **精美界面** - 现代化的响应式Web界面设计
- 💾 **游戏记录** - 自动保存游戏历史记录

## 🎯 游戏规则

1. 输入一个汉字作为飞花令的关键字（如"花"、"月"、"春"等）
2. 玩家和AI轮流说出包含该字的诗句
3. 不能重复已经说过的诗句
4. 输入的必须是真正的古诗词
5. 谁先想不出新的诗句就输了

## 🚀 快速开始

### 环境要求

- Python 3.7+
- pip包管理器

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/feihualing-game.git
cd feihualing-game
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动应用**
```bash
python app.py
```

4. **访问游戏**
打开浏览器访问：http://localhost:5000

## 📁 项目结构

```
feihualing-game/
├── app.py              # Flask主应用
├── feihualing.py       # 命令行版本
├── requirements.txt    # 项目依赖
├── README.md          # 项目说明
├── templates/         # HTML模板
│   └── index.html    # 游戏主页面
└── static/           # 静态资源
    ├── css/
    │   └── style.css # 样式文件
    └── js/
        └── app.js    # 前端JavaScript
```

## 🎮 使用方法

### Web版本
1. 启动Flask应用后，在浏览器中打开 http://localhost:5000
2. 输入一个汉字作为关键字
3. 点击"开始游戏"
4. 在输入框中输入包含关键字的诗句
5. 点击"提交"或按回车键发送
6. AI会自动回复相应的诗句
7. 继续游戏直到一方无法继续

### 命令行版本
```bash
python feihualing.py
```

## 🔧 配置说明

### API配置
应用使用以下免费诗词API：
- SaintIC古诗词API
- 其他备用API

如果API不可用，系统会自动切换到本地诗句库。

### 本地诗句库
内置了以下常用字的诗句：
- 春、花、月、水、山
- 风、雨、江、秋、雪

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 如何贡献
1. Fork本项目
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 感谢所有古诗词API提供者
- 感谢Flask框架
- 感谢所有贡献者

## 📮 联系方式

如有问题或建议，请提交Issue或联系项目维护者。

---

**享受飞花令的乐趣，传承中华诗词文化！** 🌸📜
