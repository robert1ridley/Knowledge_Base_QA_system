# Knowledge Base QA System
本系统是一个基于知识库问答系统，可以回答关于《三国演义》的问题。

## 系统的依赖性
- Python版本：3.5.1

## 设置环境指南
- 下载项目：`git clone https://github.com/robert1ridley/Knowledge_Base_QA_system.git`
- 打开一个终端窗口
- 输入`cd Knowledge_Base_QA_system`
- 生成一个python3虚拟环境: 输入`python3 -m venv venv`
- 启动虚拟环境：输入`source venv/bin/activate`
- 下载项目的依赖性：输入`pip install -r requirements.txt`

## 系统使用指南
系统有以下5个阶段，需要顺序的完成：
1. 生成关于《三国演义》的知识库：输入`python generate_knowledge_base.py`，执行后，一个文件叫`three_kingdoms.rdf`将在`data/`文件夹里保存下来。
2. 抽取《三国演义》的关键词：输入`python keyword_generator.py`，执行后，一个文件叫`keywords.txt`将在`data/`文件夹里保存下来。
3. 为了训练神经网络，生成意图的训练数据：输入`python generate_intent_training_data.py`，执行后，一个文件叫`training.txt`将在`data/`文件夹里保存下来。
4. 训练分类意图的神经网络：输入`python intent_classifier.py`，执行后，一个文件叫`vocab.p`将在`data/`文件夹里保存下来，训练好的模型和权重（`model.h5`和`model.json`）将在`pretrained_models/`保存下来。
5. 启动整个问答系统：确保上面的阶段都已完成，输入`python handle_input.py`，在终端窗口里输入关于《三国演义》的问题，等到系统输出答案。
