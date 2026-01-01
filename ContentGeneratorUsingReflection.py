"""
Content Generator with Reflection (Modular App)
GitHub: https://github.com/AnubhavKarki/ContentGeneratorUsingReflection
"""

import os
from typing import List, Sequence
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langgraph.graph import END, MessageGraph
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import textwrap
from datetime import datetime


class ContentGenerator:
    def __init__(self, max_iterations: int = 5):
        """Initialize Content Generator with Reflection Graph."""
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        self.max_iterations = max_iterations
        self.graph = self._build_graph()
        self.trace_history = []  # Store generation traces

    def _build_graph(self):
        """Build reflection graph."""
        # Generation prompt
        generation_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a Twitter (X) expert assigned to craft outstanding Contents.
Generate the most engaging and impactful Content possible based on the user's request.
If the user provides feedback, refine and enhance your previous attempts accordingly for maximum engagement.""",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        # Reflection prompt
        reflection_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a Twitter influencer known for your engaging content and sharp insights.
Review and critique the user's Content.
Provide constructive feedback, focusing on enhancing its depth, style, and overall impact.
Offer specific suggestions to make the Content more compelling and engaging for their audience.""",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        generate_chain = generation_prompt | self.llm
        reflect_chain = reflection_prompt | self.llm

        def generation_node(state: Sequence[BaseMessage]):
            return generate_chain.invoke({"messages": state})

        def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
            cls_map = {"ai": HumanMessage, "human": AIMessage}
            translated = [messages[0]] + [
                cls_map[msg.type](content=msg.content) for msg in messages[1:]
            ]
            res = reflect_chain.invoke({"messages": translated})
            return [HumanMessage(content=res.content)]

        builder = MessageGraph()
        builder.add_node("generate", generation_node)
        builder.add_node("reflect", reflection_node)
        builder.set_entry_point("generate")

        def should_continue(state):
            if len(state) >= self.max_iterations * 2:
                return END
            if state[-1].type == "human":
                return "generate"
            return "reflect"

        builder.add_conditional_edges(
            "generate", should_continue, {"reflect": "reflect", END: END}
        )
        builder.add_edge("reflect", "generate")

        return builder.compile()

    def generate_Content_with_trace(self, topic: str):
        """Generate Content with full trace capture."""
        self.trace_history = []  # Reset trace

        inputs = HumanMessage(content=f"Generate a Content about {topic}")
        response = self.graph.invoke(inputs)

        # Extract trace from full response
        trace_steps = []
        for i, msg in enumerate(response):
            if isinstance(msg, AIMessage):
                step_type = "generate" if i % 2 == 0 else "reflect"
                trace_steps.append(
                    {
                        "step": len(trace_steps) + 1,
                        "type": step_type,
                        "content": msg.content,
                    }
                )

        final_Content = (
            trace_steps[-1]["content"] if trace_steps else "No Content generated."
        )
        self.trace_history = trace_steps
        return final_Content

    def visualize_graph(self):
        """Display matplotlib graph visualization."""
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect("equal")

        # Generate node
        generate_box = patches.FancyBboxPatch(
            (2, 6),
            3,
            2,
            boxstyle="round,pad=0.1",
            facecolor="#4CAF50",
            edgecolor="white",
            linewidth=2,
        )
        ax.add_patch(generate_box)
        ax.text(
            3.5,
            7,
            "GENERATE\nContent",
            ha="center",
            va="center",
            fontsize=14,
            fontweight="bold",
            color="white",
        )

        # Reflect node
        reflect_box = patches.FancyBboxPatch(
            (6, 6),
            3,
            2,
            boxstyle="round,pad=0.1",
            facecolor="#2196F3",
            edgecolor="white",
            linewidth=2,
        )
        ax.add_patch(reflect_box)
        ax.text(
            7.5,
            7,
            "REFLECT\nFeedback",
            ha="center",
            va="center",
            fontsize=14,
            fontweight="bold",
            color="white",
        )

        # END node
        end_box = patches.FancyBboxPatch(
            (4, 2),
            2,
            1.5,
            boxstyle="round,pad=0.1",
            facecolor="#FF9800",
            edgecolor="white",
            linewidth=2,
        )
        ax.add_patch(end_box)
        ax.text(
            5,
            2.75,
            "FINAL\nContent",
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
            color="white",
        )

        # Arrows
        ax.annotate(
            "",
            xy=(5, 6),
            xytext=(3.5, 6),
            arrowprops=dict(arrowstyle="->", lw=2, color="#4CAF50"),
        )
        ax.annotate(
            "",
            xy=(8, 6),
            xytext=(6.5, 6),
            arrowprops=dict(arrowstyle="->", lw=2, color="#2196F3"),
        )
        ax.annotate(
            "",
            xy=(5, 4.5),
            xytext=(5.5, 4),
            arrowprops=dict(arrowstyle="->", lw=2, color="#FF9800"),
        )
        ax.annotate(
            "",
            xy=(6, 4.5),
            xytext=(4.5, 4),
            arrowprops=dict(arrowstyle="->", lw=2, color="#FF9800"),
        )

        ax.set_title(
            "Content Generator Reflection Graph", fontsize=20, fontweight="bold", pad=20
        )
        ax.axis("off")
        plt.tight_layout()
        plt.show()

    def print_beautiful_Content(self, Content: str):
        """Print Content with beautiful formatting."""
        print("\n" + "=" * 60)
        print("FINAL Content".center(60))
        print("=" * 60)
        wrapped_Content = textwrap.fill(Content, width=55)
        print(wrapped_Content)
        print("=" * 60)
        print("Ready to post? Type 'new <topic>', 'save', 'trace', or 'help'")

    def save_Content_to_file(self, Content: str):
        """Save current Content to timestamped file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Content_{timestamp}.txt"
        with open(filename, "w") as f:
            f.write(
                f"Content generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            f.write("-" * 50 + "\n")
            f.write(Content)
        print(f"Content saved to {filename}")

    def show_trace(self):
        """Show beautiful trace of refinement process."""
        if not self.trace_history:
            print("\nNo trace available. Generate a Content first!")
            return

        print("\n" + "=" * 80)
        print("REFLECTION TRACE".center(80))
        print("=" * 80)

        for step in self.trace_history:
            step_num = f"Step {step['step']}"
            step_type = f"({step['type'].upper()})"
            content = textwrap.fill(step["content"], width=70)

            print(f"\n{step_num:<8} {step_type:<12}")
            print("-" * 80)
            print(content)
            print()

        print("=" * 80)
        print("Final Content ready! Use 'save' to export.")

    def show_help(self):
        """Show help menu."""
        print("\n" + "COMMANDS HELP".center(60, "="))
        print("\nChat Commands:")
        print("  new <topic>     - Generate new Content")
        print("  feedback <text> - Refine current Content")
        print("  save            - Save Content to file")
        print("  trace           - Show full refinement trace")
        print("\nVisual Commands:")
        print("  visualize       - Show graph diagram")
        print("  help            - Show this help")
        print("\nExit:")
        print("  quit, exit, q   - Exit chat")
        print("\n" + "=" * 60)

    def interactive_cli(self):
        """Interactive chat shell interface."""
        print("Content Generator with Reflection - Interactive Chat")
        print("Type 'help' for commands")
        print("-" * 60)

        current_Content = ""

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if user_input.lower() in ["quit", "exit", "q"]:
                    print("\nAgent: Goodbye! Happy Contenting!")
                    break

                if user_input.lower() == "help":
                    self.show_help()
                    continue

                if user_input.lower() == "visualize":
                    print("\nAgent: Showing reflection graph visualization:")
                    self.visualize_graph()
                    continue

                if user_input.lower() == "save":
                    if current_Content:
                        self.save_Content_to_file(current_Content)
                    else:
                        print("\nAgent: No Content to save. Generate one first!")
                    continue

                if user_input.lower() == "trace":
                    self.show_trace()
                    continue

                # Generate Content for new topic
                if user_input.lower().startswith("new ") or not current_Content:
                    topic = user_input.replace("new ", "").strip()
                    print(
                        f"\nAgent: Generating Content about '{topic}' with reflection..."
                    )
                    current_Content = self.generate_Content_with_trace(topic)
                    self.print_beautiful_Content(current_Content)

                # Handle feedback/refinement
                elif user_input.lower().startswith("feedback "):
                    feedback = user_input.replace("feedback ", "").strip()
                    print("\nAgent: Refining Content based on your feedback...")
                    current_Content = self.generate_Content_with_trace(
                        f"Refine this Content based on: " + feedback
                    )
                    self.print_beautiful_Content(current_Content)

                else:
                    print(
                        "\nAgent: Try 'new <topic>', 'feedback <suggestion>', 'save', 'trace', 'visualize', or 'help'"
                    )

            except KeyboardInterrupt:
                print("\n\nAgent: Goodbye! Happy Contenting!")
                break
            except Exception as e:
                print(f"\nAgent: Something went wrong: {e}")


# Usage Examples
def main():
    # Initialize (reads OPENAI_API_KEY from environment)
    generator = ContentGenerator(max_iterations=3)

    # Start interactive chat
    generator.interactive_cli()


if __name__ == "__main__":
    main()
