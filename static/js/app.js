// 飞花令游戏JavaScript逻辑
class FeiHuaLingGame {
    constructor() {
        this.currentState = 'start'; // start, playing, ended
        this.currentRound = 0;
        this.targetChar = '';
        
        this.initElements();
        this.bindEvents();
    }

    // 初始化DOM元素引用
    initElements() {
        // 面板
        this.startPanel = document.getElementById('start-panel');
        this.gamePanel = document.getElementById('game-panel');
        this.endPanel = document.getElementById('end-panel');
        
        // 开始游戏相关
        this.targetCharInput = document.getElementById('target-char');
        this.startBtn = document.getElementById('start-btn');
        this.charButtons = document.querySelectorAll('.char-btn');
        
        // 游戏进行相关
        this.currentCharDisplay = document.getElementById('current-char');
        this.roundNumberDisplay = document.getElementById('round-number');
        this.chatArea = document.getElementById('chat-area');
        this.poemInput = document.getElementById('poem-input');
        this.submitBtn = document.getElementById('submit-btn');
        this.endGameBtn = document.getElementById('end-game-btn');
        this.newGameBtn = document.getElementById('new-game-btn');
        
        // 结束游戏相关
        this.resultTitle = document.getElementById('result-title');
        this.resultMessage = document.getElementById('result-message');
        this.totalRoundsDisplay = document.getElementById('total-rounds');
        this.finalCharDisplay = document.getElementById('final-char');
        this.restartBtn = document.getElementById('restart-btn');
        
        // 提示和加载
        this.toast = document.getElementById('toast');
        this.toastMessage = document.getElementById('toast-message');
        this.loading = document.getElementById('loading');
    }

    // 绑定事件监听器
    bindEvents() {
        // 开始游戏
        this.startBtn.addEventListener('click', () => this.startGame());
        this.targetCharInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.startGame();
        });
        
        // 快速选择字符
        this.charButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const char = e.target.dataset.char;
                this.targetCharInput.value = char;
                this.startGame();
            });
        });
        
        // 游戏进行中
        this.submitBtn.addEventListener('click', () => this.submitPoem());
        this.poemInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.submitPoem();
        });
        
        // 游戏控制
        this.endGameBtn.addEventListener('click', () => this.endGame());
        this.newGameBtn.addEventListener('click', () => this.resetToStart());
        this.restartBtn.addEventListener('click', () => this.resetToStart());
    }

    // 显示提示消息
    showToast(message, type = 'info') {
        this.toastMessage.textContent = message;
        this.toast.className = `toast ${type}`;
        this.toast.classList.remove('hidden');
        
        setTimeout(() => {
            this.toast.classList.add('hidden');
        }, 3000);
    }

    // 显示/隐藏加载动画
    showLoading(show = true) {
        if (show) {
            this.loading.classList.remove('hidden');
        } else {
            this.loading.classList.add('hidden');
        }
    }

    // 切换面板显示
    switchPanel(panelName) {
        this.startPanel.classList.add('hidden');
        this.gamePanel.classList.add('hidden');
        this.endPanel.classList.add('hidden');
        
        switch(panelName) {
            case 'start':
                this.startPanel.classList.remove('hidden');
                break;
            case 'game':
                this.gamePanel.classList.remove('hidden');
                break;
            case 'end':
                this.endPanel.classList.remove('hidden');
                break;
        }
    }

    // 开始游戏
    async startGame() {
        const targetChar = this.targetCharInput.value.trim();
        
        if (!targetChar) {
            this.showToast('请输入一个汉字作为关键字！', 'error');
            return;
        }
        
        if (targetChar.length !== 1) {
            this.showToast('请输入一个汉字！', 'error');
            return;
        }

        // 验证是否为汉字
        if (!/[\u4e00-\u9fff]/.test(targetChar)) {
            this.showToast('请输入一个有效的汉字！', 'error');
            return;
        }

        this.showLoading(true);

        try {
            const response = await fetch('/start_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ target_char: targetChar })
            });

            const data = await response.json();

            if (data.success) {
                this.targetChar = data.target_char;
                this.currentRound = 0;
                this.currentState = 'playing';
                
                // 更新UI
                this.currentCharDisplay.textContent = this.targetChar;
                this.roundNumberDisplay.textContent = '1';
                this.chatArea.innerHTML = '';
                this.poemInput.value = '';
                
                this.switchPanel('game');
                this.showToast(data.message, 'success');
                this.poemInput.focus();
            } else {
                this.showToast(data.message, 'error');
            }
        } catch (error) {
            console.error('开始游戏失败:', error);
            this.showToast('网络错误，请重试！', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    // 提交诗句
    async submitPoem() {
        const poem = this.poemInput.value.trim();
        
        if (!poem) {
            this.showToast('请输入诗句！', 'error');
            return;
        }

        this.showLoading(true);
        this.submitBtn.disabled = true;

        try {
            const response = await fetch('/submit_poem', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ poem: poem })
            });

            const data = await response.json();

            if (data.success) {
                // 显示用户诗句
                this.addMessage(data.user_poem, 'user', data.round);
                this.poemInput.value = '';
                
                if (data.game_continues && data.ai_poem) {
                    // AI回复
                    setTimeout(() => {
                        this.addMessage(data.ai_poem, 'ai', data.round);
                        this.currentRound = data.round;
                        this.roundNumberDisplay.textContent = data.round + 1;
                    }, 1000);
                } else {
                    // 游戏结束，用户获胜
                    setTimeout(() => {
                        this.endGameWithResult('win', data.message, data.round);
                    }, 1000);
                }
            } else {
                this.showToast(data.message, 'error');
            }
        } catch (error) {
            console.error('提交诗句失败:', error);
            this.showToast('网络错误，请重试！', 'error');
        } finally {
            this.showLoading(false);
            this.submitBtn.disabled = false;
            this.poemInput.focus();
        }
    }

    // 添加消息到聊天区域
    addMessage(text, sender, round) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'message-bubble';
        bubbleDiv.textContent = text;
        
        const infoDiv = document.createElement('div');
        infoDiv.className = 'message-info';
        
        if (sender === 'user') {
            infoDiv.textContent = `第${round}回合 - 你`;
        } else {
            infoDiv.textContent = `第${round}回合 - AI`;
        }
        
        messageDiv.appendChild(bubbleDiv);
        messageDiv.appendChild(infoDiv);
        
        this.chatArea.appendChild(messageDiv);
        
        // 滚动到底部
        this.chatArea.scrollTop = this.chatArea.scrollHeight;
    }

    // 结束游戏
    async endGame() {
        if (confirm('确定要认输结束游戏吗？')) {
            this.showLoading(true);

            try {
                const response = await fetch('/end_game', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                const data = await response.json();
                
                if (data.success) {
                    this.endGameWithResult('lose', data.message, this.currentRound);
                }
            } catch (error) {
                console.error('结束游戏失败:', error);
                this.showToast('网络错误！', 'error');
            } finally {
                this.showLoading(false);
            }
        }
    }

    // 显示游戏结果
    endGameWithResult(result, message, rounds) {
        this.currentState = 'ended';
        
        if (result === 'win') {
            this.resultTitle.textContent = '🎊 恭喜获胜！ 🎊';
            this.resultMessage.textContent = message || '恭喜你赢得了这局飞花令！';
        } else {
            this.resultTitle.textContent = '😊 游戏结束 😊';
            this.resultMessage.textContent = message || '感谢参与，再接再厉！';
        }
        
        this.totalRoundsDisplay.textContent = rounds || this.currentRound;
        this.finalCharDisplay.textContent = this.targetChar;
        
        setTimeout(() => {
            this.switchPanel('end');
        }, 1500);
    }

    // 重置到开始状态
    resetToStart() {
        this.currentState = 'start';
        this.currentRound = 0;
        this.targetChar = '';
        this.targetCharInput.value = '';
        this.chatArea.innerHTML = '';
        this.poemInput.value = '';
        
        this.switchPanel('start');
        this.targetCharInput.focus();
    }

    // 添加一些随机特效
    addRandomEffects() {
        // 为页面添加一些动态效果
        setInterval(() => {
            if (Math.random() < 0.1) { // 10% 概率
                this.createFloatingPoetry();
            }
        }, 5000);
    }

    // 创建飘浮诗句效果
    createFloatingPoetry() {
        const poems = [
            '春风又绿江南岸', '花开堪折直须折', '月上柳梢头',
            '山重水复疑无路', '落红不是无情物', '海上生明月'
        ];
        
        const poem = poems[Math.floor(Math.random() * poems.length)];
        const floatingText = document.createElement('div');
        
        floatingText.textContent = poem;
        floatingText.style.cssText = `
            position: fixed;
            top: ${Math.random() * 50 + 10}%;
            left: ${Math.random() * 80 + 10}%;
            color: rgba(255,255,255,0.6);
            font-size: 0.9rem;
            pointer-events: none;
            z-index: 2;
            animation: fadeFloat 4s ease-out forwards;
        `;
        
        // 添加CSS动画
        if (!document.getElementById('floating-animation')) {
            const style = document.createElement('style');
            style.id = 'floating-animation';
            style.textContent = `
                @keyframes fadeFloat {
                    0% { opacity: 0; transform: translateY(0px); }
                    50% { opacity: 1; transform: translateY(-20px); }
                    100% { opacity: 0; transform: translateY(-40px); }
                }
            `;
            document.head.appendChild(style);
        }
        
        document.body.appendChild(floatingText);
        
        setTimeout(() => {
            if (floatingText.parentNode) {
                floatingText.parentNode.removeChild(floatingText);
            }
        }, 4000);
    }
}

// 页面加载完成后初始化游戏
document.addEventListener('DOMContentLoaded', () => {
    const game = new FeiHuaLingGame();
    
    // 添加一些随机特效
    game.addRandomEffects();
    
    // 让第一个输入框获得焦点
    setTimeout(() => {
        document.getElementById('target-char').focus();
    }, 500);
    
    console.log('🌸 飞花令游戏已加载完成！');
});