# -*- coding: utf-8 -*-
from modelscope.pipelines import pipeline

t2t_generator = pipeline("text2text-generation", "/Users/jinmu/.cache/modelscope/hub/damo/nlp_mt5_zero-shot-augment_chinese-base", model_revision="v1.0.0")

# print(t2t_generator("文本分类。\n候选标签：故事,房产,娱乐,文化,游戏,国际,股票,科技,军事,教育。\n文本内容：他们的故事平静而闪光，一代人奠定沉默的基石，让中国走向繁荣。"))
# {'text': '文化'}

# print(t2t_generator("抽取关键词：\n在分析无线Mesh网路由协议所面临挑战的基础上,结合无线Mesh网络的性能要求,以优化链路状态路由(OLSR)协议为原型,采用跨层设计理论,提出了一种基于链路状态良好程度的路由协议LR-OLSR.该协议引入了认知无线网络中的环境感知推理思想,通过时节点负载、链路投递率和链路可用性等信息进行感知,并以此为依据对链路质量进行推理,获得网络中源节点和目的节点对之间各路径状态良好程度的评价,将其作为路由选择的依据,实现对路由的优化选择,提高网络的吞吐量,达到负载均衡.通过与OLSR及其典型改进协议P-OLSR、SC-OLSR的对比仿真结果表明,LR-OLSB能够提高网络中分组的递交率,降低平均端到端时延,在一定程度上达到负载均衡."))
# # {'text': '无线Mesh网,路由协议,环境感知推理'}
#
# print(t2t_generator("为以下的文本生成标题：\n在分析无线Mesh网路由协议所面临挑战的基础上,结合无线Mesh网络的性能要求,以优化链路状态路由(OLSR)协议为原型,采用跨层设计理论,提出了一种基于链路状态良好程度的路由协议LR-OLSR.该协议引入了认知无线网络中的环境感知推理思想,通过时节点负载、链路投递率和链路可用性等信息进行感知,并以此为依据对链路质量进行推理,获得网络中源节点和目的节点对之间各路径状态良好程度的评价,将其作为路由选择的依据,实现对路由的优化选择,提高网络的吞吐量,达到负载均衡.通过与OLSR及其典型改进协议P-OLSR、SC-OLSR的对比仿真结果表明,LR-OLSB能够提高网络中分组的递交率,降低平均端到端时延,在一定程度上达到负载均衡."))
# # {'text': '基于链路状态良好程度的无线Mesh网路由协议'}
#
# print(t2t_generator("为下面的文章生成摘要：\n据统计，今年三季度大中华区共发生58宗IPO交易，融资总额为60亿美元，交易宗数和融资额分别占全球的35%和25%。报告显示，三季度融资额最高的三大证券交易所分别为东京证券交易所、深圳证券交易所和马来西亚证券交易所"))
# # {'text': '大中华区IPO融资额超60亿美元'}
#
# print(t2t_generator("评价对象抽取：颐和园还是挺不错的，作为皇家园林，有山有水，亭台楼阁，古色古香，见证着历史的变迁。"))
# # {'text': '颐和园'}
#
# print(t2t_generator("翻译成英文：如果日本沉没，中国会接收日本难民吗？"))
# # {'text': 'will China accept Japanese refugees if Japan sinks?'}
#
# print(t2t_generator("情感分析：外观漂亮，性能不错，屏幕很好。"))
# # {'text': '积极'}
#
# print(t2t_generator("根据给定的段落和答案生成对应的问题。\n段落：跑步后不能马上进食，运动与进食的时间要间隔30分钟以上。看你跑步的量有多大。不管怎么样，跑完步后要慢走一段时间，将呼吸心跳体温调整至正常状态才可进行正常饮食。血液在四肢还没有回流到内脏，不利于消化，加重肠胃的负担。如果口渴可以喝一点少量的水。洗澡的话看你运动量。如果跑步很剧烈，停下来以后，需要让身体恢复正常之后，再洗澡，能达到放松解乏的目的，建议15-20分钟后再洗澡；如果跑步不是很剧烈，只是慢跑，回来之后可以马上洗澡。 \n 答案：30分钟以上"))
# # {'text': '跑步后多久进食'}

print(t2t_generator("为以下的文本生成标题: \n想要收听更多付费精品节目请加微信1716143665你好 我是刘超欢迎来到去谈Linux操作系统的课堂今天是入学的第一课但是呢我们今天不打算直接进入主题我为你准备了12道小题邀请你先来做个小测验你可不要小看这些题目它们都是我精心设计反复筛选出来的可以说是覆盖了Linux操作系统中最重要最核心的知识点我估计你看着它也不会陌生甚至你正在从事相关的工作但是你对你所做的事情真的了解吗有了解到什么样的程度呢这两个问题非常非常关键我们平时所谓说我要成长就是要知道自己目前在哪里并且清楚将来要去哪里然后通过学习和行动到达自己的目的地希望这道题目能帮你明确在哪里和去哪里的问题然后我们整个课程的学习帮你解决怎么去的问题所以一方面我希望你可以通过这套题目对自己之前的学习做一个检测查缺不漏另外一方面我希望你可以把这套题目作为手边的一个常用资料每隔一段时间都回过头来检测一下所谓走得太远不要忘记自己当初为什么而出发接下来跟你聊一聊我希望你怎样去做这套题题目一共12套都是多项选择题你可以安排15分钟到30分钟的时间静下心来认真读题杆和每一个选项不仅仅选出你认为正确的答案更重要的是对于每一道题目都去想想这道题背后的知识点到底是什么如果有可能你可以用笔写下来12道题目结束以后你可以看看自己是不是可以勾露出一个知识体系同时如果你在哪里有困惑拿不准不太确信千万不要放过这些地方赶紧记下来带着这些问题去学习你才能够做到事半功倍最后这道题目我不会现在就给答案原因我想你也很清楚了我们把这道题目当成一个工具知己而知目标在后面的学习过程中我会带你一起解开每一道题目的面纱好了现在你可以把你的答案思考疑问都写在留言区记录下来这样在之后的学习过程中你就可以对照这些内容有争论性的去攻克做完之后呢你也可以把这份测试题分享给你的朋友和他一起学习进步祝你每道题都有收获。"))