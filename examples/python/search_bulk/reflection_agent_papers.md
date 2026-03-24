# 反思相关的 Agent 顶会论文

## 核心经典论文 (高引用)

### 1. Chain of Thought Prompting (NeurIPS 2022) - 16541 引用
- **标题**: Chain of Thought Prompting Elicits Reasoning in Large Language Models
- **作者**: Jason Wei et al.
- **会议**: Neural Information Processing Systems (NeurIPS) 2022
- **链接**: https://www.semanticscholar.org/paper/1b6e810ce0afd0dd093f789d2b2742d047e316d5
- **简介**: 提出了 Chain-of-Thought (CoT) 推理方法，通过逐步推理来增强 LLM 的推理能力

### 2. ReAct (ICLR 2022) - 6480 引用
- **标题**: ReAct: Synergizing Reasoning and Acting in Language Models
- **作者**: Shunyu Yao et al.
- **会议**: International Conference on Learning Representations (ICLR) 2022
- **链接**: https://www.semanticscholar.org/paper/99832586d55f540f603637e458a292406a0ed75d
- **简介**: 将推理(Reasoning)与行动(Acting)结合，是 Agent 推理的奠基性工作

### 3. Self-Consistency (ICLR 2022) - 6158 引用
- **标题**: Self-Consistency Improves Chain of Thought Reasoning in Language Models
- **作者**: Xuezhi Wang et al.
- **会议**: International Conference on Learning Representations (ICLR) 2022
- **链接**: https://www.semanticscholar.org/paper/5f19ae1135a9500940978104ec15a5b8751bc7d2
- **简介**: 通过采样多条推理路径并投票来提高推理准确性

### 4. Tree of Thoughts (NeurIPS 2023) - 3570 引用
- **标题**: Tree of Thoughts: Deliberate Problem Solving with Large Language Models
- **作者**: Shunyu Yao et al.
- **会议**: Neural Information Processing Systems (NeurIPS) 2023
- **链接**: https://www.semanticscholar.org/paper/2f3822eb380b5e753a6d579f31dfc3ec4c4a0820
- **简介**: 将思维扩展为树形结构，支持搜索和回溯

### 5. Self-Refine (NeurIPS 2023) - 3012 引用
- **标题**: Self-Refine: Iterative Refinement with Self-Feedback
- **作者**: Aman Madaan et al.
- **会议**: Neural Information Processing Systems (NeurIPS) 2023
- **链接**: https://www.semanticscholar.org/paper/3aaf6a2cbad5850ad81ab5c163599cb3d523436f
- **简介**: 通过自我反馈进行迭代优化

### 6. Reflexion (NeurIPS 2023) - 2828 引用 ⭐
- **标题**: Reflexion: Language Agents with Verbal Reinforcement Learning
- **作者**: Noah Shinn et al.
- **会议**: Neural Information Processing Systems (NeurIPS) 2023
- **链接**: https://www.semanticscholar.org/paper/0671fd553dd670a4e820553a974bc48040ba0819
- **简介**: **最核心的反思 Agent 论文**，通过语言反馈实现自我反思和学习

---

## 其他重要论文

### 7. Multiagent Debate (ICML 2023) - 1386 引用
- **标题**: Improving Factuality and Reasoning in Language Models through Multiagent Debate
- **作者**: Yilun Du et al.
- **会议**: International Conference on Machine Learning (ICML) 2023
- **简介**: 通过多 Agent 辩论来提高推理能力

### 8. STaR (2022) - 781 引用
- **标题**: STaR: Bootstrapping Reasoning With Reasoning
- **作者**: E. Zelikman et al.
- **简介**: 通过自我生成推理链进行自举学习

### 9. Large Language Models Can Self-Improve (EMNLP 2022) - 810 引用
- **标题**: Large Language Models Can Self-Improve
- **作者**: Jiaxin Huang et al.
- **会议**: Conference on Empirical Methods in Natural Language Processing (EMNLP) 2022
- **简介**: 模型通过自我生成数据进行自我改进

### 10. Least-to-Most Prompting (ICLR 2022) - 1603 引用
- **标题**: Least-to-Most Prompting Enables Complex Reasoning in Large Language Models
- **作者**: Denny Zhou et al.
- **会议**: International Conference on Learning Representations (ICLR) 2022
- **简介**: 将复杂问题分解为简单子问题

---

## 2024-2025 年新论文

1. **Efficient Reasoning for Large Reasoning Language Models via Certainty-Guided Reflection Suppression** (AAAI 2025)
   - 通过确定性引导的反思抑制来提高推理效率

2. **Re2LLM: Reflective Reinforcement Large Language Model** (AAAI 2024)
   - 反思强化学习 LLM 用于会话推荐

3. **InEx: Hallucination Mitigation via Introspection and Cross-Modal Multi-Agent Collaboration** (AAAI 2025)
   - 通过内省和多 Agent 协作减少幻觉

4. **MAPS: Multi-Agent Personality Shaping for Collaborative Reasoning** (AAAI 2025)
   - 多 Agent 个性塑造用于协作推理

---

## 总结

**核心三篇**（建议优先阅读）：
1. **Reflexion** (NeurIPS 2023) - 反思 Agent 的奠基性工作
2. **ReAct** (ICLR 2022) - Agent 推理与行动结合
3. **Self-Refine** (NeurIPS 2023) - 自我反思迭代优化

**推理基础**：
- Chain of Thought Prompting (NeurIPS 2022)
- Self-Consistency (ICLR 2022)
- Tree of Thoughts (NeurIPS 2023)
