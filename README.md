# ContentGenerator

**AI-powered tweet generator with reflection loops that iteratively improves content quality**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-latest-orange)](https://www.langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-latest-purple)](https://langchain-ai.github.io/langgraph/)

## Features

- **Interactive Chat Interface** - Real-time conversation with `You:` / `Agent:` prompts
- **Reflection Loops** - AI self-critiques and refines tweets through multiple iterations
- **Beautiful Trace Viewer** - See every step of the refinement process
- **One-Click Save** - Export tweets to timestamped `.txt` files
- **Live Graph Visualization** - Matplotlib diagram of the reflection workflow
- **Smart Commands** - `new`, `feedback`, `save`, `trace`, `visualize`, `help`

## How Reflection Works

The generator uses **LangGraph's stateful graph** with two nodes:

```
GENERATE → REFLECT → GENERATE → REFLECT → FINAL TWEET
  ↓           ↓           ↓           ↓
AI creates   AI critiques  AI improves AI finalizes
```

1. **Generate Node**: Creates initial tweet using GPT-4o-mini
2. **Reflect Node**: AI acts as Twitter expert, critiques the draft
3. **Loop**: Continues until max iterations or optimal tweet achieved
4. **Trace**: Full history preserved for inspection

## Tech Stack

| Component | Purpose |
|-----------|---------|
| **LangGraph** | Stateful reflection graph orchestration |
| **LangChain** | Message handling & prompt templates |
| **LangChain-OpenAI** | GPT-4o-mini integration |
| **OpenAI** | LLM inference |
| **Matplotlib** | Graph visualization |
| **Textwrap** | Beautiful tweet formatting |

## Installation

```bash
# Clone the repo
git clone https://github.com/AnubhavKarki/ContentGenerator.git
cd ContentGenerator

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
# or on Windows: set OPENAI_API_KEY=your-api-key-here
```

**requirements.txt contents:**
```
openai
langchain
langchain-openai
langchain-community
langgraph
matplotlib
```

## Quick Start

```bash
python main.py
```

```
Tweet Generator with Reflection - Interactive Chat
Type 'help' for commands
--------------------------------------------------

You: new AI ethics
Agent: Generating tweet about 'AI ethics' with reflection...

============================================================
FINAL TWEET
============================================================
AI ethics debate: Are we creating digital gods without
moral compasses? Time for programmers to play philosopher. 🤖⚖️
============================================================
Ready to post? Type 'new <topic>', 'save', 'trace', or 'help'

You: feedback make it shorter and punchier
You: trace
You: save
```

## Commands

| Command | Action |
|---------|--------|
| `new <topic>` | Generate fresh tweet |
| `feedback <text>` | Refine with specific feedback |
| `save` | Export to `tweet_YYYYMMDD_HHMMSS.txt` |
| `trace` | Show full refinement steps |
| `visualize` | Display workflow graph |
| `help` | Show this menu |
| `quit/q/exit` | Exit |

## Example Output

**tweet_20241201_143022.txt:**
```
Tweet generated on 2024-12-01 14:30:22
--------------------------------------------------
AI ethics: We're building digital gods without moral compasses.
```

## 🔍 Trace Example

```
REFLECTION TRACE
================================================================================

Step 1     (GENERATE) 
--------------------------------------------------------------------------------
Long explanation about AI ethics and responsibility...

Step 2     (REFLECT)  
--------------------------------------------------------------------------------
Good content but too wordy for Twitter. Needs punchier delivery...

Step 3     (GENERATE)
--------------------------------------------------------------------------------
AI ethics: Digital gods without moral compasses. Time to code conscience.
```

## Graph Visualization

```
[GENERATE Tweet] → [REFLECT Feedback] → [FINAL TWEET]
     ↓                    ↓                 ↑
   GPT-4o-mini        Twitter Expert     Optimized Output
```

## Contributing

1. Fork the repo
2. Create feature branch (`git checkout -b feature/reflection-v2`)
3. Commit changes (`git commit -m 'Add new reflection node'`)
4. Push (`git push origin feature/reflection-v2`)
5. Open Pull Request

## License

MIT License - see [LICENSE](LICENSE) file.

## Acknowledgments

Built with ❤️ using [LangChain](https://langchain.com) & [LangGraph](https://langchain-ai.github.io/langgraph/)

---

**Made by [Anubhav Karki](https://github.com/AnubhavKarki)**  
⭐ Star if you found useful!
