# UNO-project

[toc]

## 小组成员

+ *Jiangze Yan*, *Thomas Young*, *Matthew Dwyer*, *Ting-Chun Chen*, *Rebecca Sarah Wallis Downham*

## 关于项目

+ 项目完成了所要求的**UNO**游戏的全部规则，并按要求额外添加了每回合开始时选择一张手牌进行换牌的步骤
+ 项目中的素材均为合理获得：
  + 卡片与图标均是团队成员自己设计
  + 部分按钮来自开源图库->[阿里巴巴矢量图库](https://www.iconfont.cn/)

### 游玩方法：

+ 运行 `Start.py` 文件可以开启游戏，进入主菜单
+ 主菜单可以开始游戏或者查看游戏规则
+ 选择开始游戏后，首先通过点击数字 1，2，3 三种卡牌确定玩家想要对抗的人数，确定好人数可以进行难度选择
+ 人数与难度确认后，玩家可以开始游戏，每轮开始前需要进行换牌操作
+ 游戏结束后，会生成得分板，玩家可以选择重新开始或退出

### 项目特点:

+ 支持玩家与`1`至`3`名机器人玩家进行游戏，玩家可进行选择。会根据选择的机器人玩家数量合理的进行游戏界面的布局
+ 支持游戏难度选择：
  + `低难度`：机器人玩家将会更少的为难玩家
  + `中等难度`：机器人会根据自己的手牌正常的出牌（标准难度）
  + `高难度`：机器人会根据场上的情况（比如，自己的上一个玩家的和下一个玩家的手牌数量）进行判断，在合适的时机使用功能牌，能够更有效的限制其他玩家赢得游戏的成功率
+ 玩家或者机器人的操作都会以提示信息展示出来
  + 每轮游戏中，玩家或者机器人玩家进行操作后，都会在左下角提示每次的操作信息。
  + 具有功能的卡牌会提示卡牌的功能效果

+ 当场上有玩家只剩下一张牌时，会在该玩家旁标注白色的 `UNO` 字样
+ 玩家游玩体验性：
  + 通过将玩家名字和选牌区域变成白色来区分是哪个玩家的回合
  + 在UI设计过程中，为提高用户游玩的体验性，采用了更好的展示效果。通过一些细节表现，使得机器人的行为看起来更像是真正的玩家

### 新增规则:

+ 当玩家手牌仅剩一张时，可以选择直接打出或者交换手牌。因为在实际测试中，当玩家只剩一张手牌时，如果只能进行交换，往往会加大游戏的难度，会给玩家的游戏体验造成不好的影响。
+ 现当一位玩家胜利后，剩下的玩家之一可能存在只剩下一张数字牌0的情况，此时这名玩家和胜利者都是零分。为避免出现这种情况的发生，将数字牌的得分整体 +1

## 技术特点

### 项目结构设计

在该**UNO**项目中，为了能够使得团队合作更加有效，采用了分模块的设计，每个模块中都有着自己的功能，各个模块都服务于主程序，而各个模块都只是提供出接口，在模块之间的调用的过程中也避免了循环依赖的情况，使得项目结构看起来更加清晰。还有一些为提高代码效率所进行的封装，例如：

+ `UtilForUNO.py` 文件中用`Util class`将对卡片的所有操作的方式进行了封装
+ `UIRendererForUNO.py` 文件封装了`pygame` 的图形渲染，为主程序提供UNO界面的可视化的方法
+ `AIPlayer.py` 文件封装了机器人玩家的出牌逻辑，根据不同的`difficulty_level` 相应的切换出牌的逻辑

除了以上的模块，为了管理参数字符串，还创建了一个`EnumForUNO.py` 文件，将一些需要做比较和判断的字符串参数放到该文件中统一管理

### 详细的日志

+ 玩家和机器人的每次操作和牌桌的状态都会打印在控制台中
+ 通过观察日志，组员能够很快的定位bug的位置，并及时处理

# UNO-project

## Group Members

+ *Jiangze Yan*, *Thomas Young*, *Matthew Dwyer*, *Ting-Chun Chen*, *Rebecca Wallis Downham*

## About The Project
+ This is an implementation of the UNO game
+ The project meets all the requirements mentioned in the description file, including the new rule of swapping a card every turn
+ images included in the project are fair use:
  + UNO cards and icons are designed by group members
  + Some buttons are referenced from [Iconfont.com](https://www.iconfont.cn/)

### Usage:

+ Start a game with the main menu by running `Start.py` file
+ User can select **START** to start a new game or **RULES** to read the rules
+ When the game starts, select the blue UNO card for the number of players and the **EASY**, **MEDIUM** or **HARD** button for the difficulty, or select **RESET** to choose again
+ After finishing with settings, the UNO game starts
+ User should **swap a card** (place one card at the bottom of the discard pile and take the top card from the draw pile) in the beginning of every turn
+ When the game ends, user can check their score on the scoring board and select **Play Again** to start another UNO game or **Quit** to leave the game

### Features:

+ Number of Player Options:
  + User can choose `1`, `2` or `3` AI players to play with, a suitable layout would be set up according to the number of AI players
+ Difficulty Options:
  + `EASY`: AI players will choose the colour for wild card based on the rest of the cards in the draw pile and on the players' hand, and the AI won't play the draw4 card on the user
  + `MEDIUM`: AI players will choose the colour with the conditions mentioned above but play the draw4 card normally (Default)
  + `HARD`: AI players will play functional cards at the right time according to the number of cards of the other players, which effectively reduces the chance for other players to win
+ Activities Of Players Were Shown As Log Messages:
  + Every decision made by user or AI players will be shown as log messages on the bottom-left 
  + When a function card is played, its function and effect will be shown as well
+ A player will be labelled with a white `UNO` next to their name when there's one card left in their hand
+ Adjustment For Better Player Experience:
  + Switch player's name and display border to white as an indicator of whose turn
  + Add some animation and interactive effects to optimise player experience
  + Adjust some details (e.g. time delay) to make AI players act more human

### Additional Game Rules:

+ **User can choose to swap a card or play it directly when there's only one card left in their hand (i.e. they have UNO).**
  During our practical testing, there's a high chance for the user to lose the game if their only allowed to swap the last card instead of playing it, which results in bad UX.
+ A player might get 0 points if only number-0 card is left in their hand, however he shouldn't get the same points as the winner.
  to avoid this, we **set the points of number card +1 than it shows on the card** (i.e. 1 point for number-0 card, 2 points for number-1 card, etc.)

## Development Feature

### Structure and Module

We use modular design to improve teamwork effectiveness.
Every module focuses on one aspect of functionality, provides only output method and serves for main function.
Program is designed to avoid circular dependencies between modules and make it easy-to-read.
We encapsulate some functional concepts as packages to improve program efficiency including:

+ The operations on the cards were encapsulated in the `Util class` in `UtilForUNO.py` file
+ Methods related to `pygame` rendering were encapsulated in the `UIRendererForUNO.py` file as the visualisation method used by main function
+ The decision-making strategies were encapsulated in the `AIPlayer.py` file for AI players to make decisions according to different `difficulty_level`

Besides the modules above, we create the `EnumForUNO.py` file to store string variables, making it convenient to manage the comparison of strings

### Detailed Log Messages

+ All of the user's and the AI players' actions as well as the status of the deck are printed on the control panel in real-time
+ Developers can promptly find bugs and deal with them by checking the log messages
