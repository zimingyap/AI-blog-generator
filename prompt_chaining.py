"""
Prompt Chaining Implementation for Blog Post Generation

This module implements a prompt chaining pattern for generating blog posts using OpenAI's GPT models.
The process is broken down into multiple steps (chains) where each step's output feeds into the next,
allowing for better control and validation at each stage.

Workflow:
1. Topic Generation -> 2. Outline Creation -> 3. Content Writing -> 4. Content Polishing

Each step includes validation gates to ensure quality control throughout the process.

Requirements:
    - openai>=1.0.0
    - python-dotenv
    - Python 3.7+
"""

from dotenv import load_dotenv
load_dotenv()

import openai
import os
import time
from typing import List, Dict, Optional, Union

class PromptChaining:
    """
    A class that implements prompt chaining for automated blog post generation.
    
    This class breaks down the blog post creation process into multiple steps,
    with each step building upon the output of the previous one. Quality gates
    are implemented between steps to ensure output meets minimum standards.
    
    Attributes:
        client (openai.OpenAI): OpenAI client instance for making API calls
    """

    def __init__(self, api_key: str):
        """
        Initialize the PromptChaining instance with OpenAI API credentials.
        
        Args:
            api_key (str): OpenAI API key for authentication
        """
        self.client = openai.OpenAI(api_key=api_key)

    def generate_llm_response(self, prompt: str) -> str:
        """
        Generate a response from the LLM using the provided prompt.
        
        Args:
            prompt (str): The input prompt for the LLM
            
        Returns:
            str: The generated response text
            
        Raises:
            Exception: If there's an error in API communication
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return ""

    def generate_blog_topics(self, domain: str, target_audience: str) -> List[str]:
        """
        Step 1: Generate potential blog topics based on domain and audience.
        
        Args:
            domain (str): The subject area for the blog post
            target_audience (str): The intended audience for the content
            
        Returns:
            List[str]: A list of generated blog topics
            
        Raises:
            ValueError: If fewer than 3 valid topics are generated
        """
        prompt = f"""Generate 5 engaging blog post topics for {target_audience} 
        in the {domain} domain. Each topic should be unique and interesting."""
        
        response = self.generate_llm_response(prompt)
        topics = [topic.strip() for topic in response.split('\n') if topic.strip()]
        
        # Gate: Check if we have enough topics
        if len(topics) < 3:
            raise ValueError("Not enough topics generated. Please try again.")
            
        return topics

    def create_outline(self, topic: str) -> Dict[str, List[str]]:
        """
        Step 2: Create a structured outline for the chosen topic.
        
        Args:
            topic (str): The selected blog post topic
            
        Returns:
            Dict[str, List[str]]: A dictionary where keys are section headings
                                 and values are lists of bullet points
                                 
        Raises:
            ValueError: If the outline has fewer than 3 sections
        """
        prompt = f"""Create a detailed outline for a blog post about '{topic}'.
        Include main sections and key points for each section."""
        
        response = self.generate_llm_response(prompt)
        
        # Parse the outline into a structured format
        sections: Dict[str, List[str]] = {}
        current_section: Optional[str] = None
        
        for line in response.split('\n'):
            if line.strip():
                if not line.startswith('  '):
                    current_section = line.strip()
                    sections[current_section] = []
                else:
                    sections[current_section].append(line.strip())
        
        # Gate: Check if outline has enough sections
        if len(sections) < 3:
            raise ValueError("Outline is too short. Please generate a more detailed outline.")
            
        return sections

    def write_content(self, outline: Dict[str, List[str]]) -> str:
        """
        Step 3: Generate the actual content based on the outline.
        
        Args:
            outline (Dict[str, List[str]]): The structured outline with sections
                                          and bullet points
                                          
        Returns:
            str: The generated blog post content
            
        Raises:
            ValueError: If the generated content is less than 300 words
        """
        content = []
        
        for section, points in outline.items():
            prompt = f"""Write a detailed section for a blog post covering the following points: {', '.join(points)}. 
            Do not include the section title in your response."""
            
            section_content = self.generate_llm_response(prompt)
            content.append(f"\n{section}\n{section_content}")
        
        final_content = "\n".join(content)
        
        # Gate: Check if content meets minimum length
        if len(final_content.split()) < 300:
            raise ValueError("Content is too short. Please generate more detailed content.")
            
        return final_content

    def edit_and_polish(self, content: str) -> str:
        """
        Step 4: Polish and improve the generated content.
        
        This step focuses on improving clarity, fixing grammatical issues,
        and enhancing the overall flow of the content.
        
        Args:
            content (str): The initial blog post content
            
        Returns:
            str: The polished and improved content
            
        Raises:
            ValueError: If no meaningful edits were made to the content
        """
        prompt = f"""Please edit and polish the following blog post content. 
        Improve clarity, fix any grammatical issues, and enhance the overall flow:
        
        {content}"""
        
        final_content = self.generate_llm_response(prompt)
        
        # Gate: Check if content was actually modified
        if final_content.strip() == content.strip():
            raise ValueError("No meaningful edits were made. Please try editing again.")
            
        return final_content

def main():
    """
    Main function to demonstrate the prompt chaining workflow.
    
    This function shows the complete process of generating a blog post,
    from topic selection to final polishing, with error handling.
    """
    api_key = os.getenv("OPEN_AI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables")
        
    blog_writer = PromptChaining(api_key)
    
    try:
        # Step 1: Generate topics
        topics = blog_writer.generate_blog_topics(
            domain="artificial intelligence",
            target_audience="business professionals"
        )
        print("Generated Topics:", topics)
        
        # Let's use the first topic
        chosen_topic = topics[0]
        
        # Step 2: Create outline
        outline = blog_writer.create_outline(chosen_topic)
        print("\nOutline:", outline)
        
        # Step 3: Write content
        content = blog_writer.write_content(outline)
        print("\nInitial Content:", content)
        
        # Step 4: Polish and finalize
        final_content = blog_writer.edit_and_polish(content)
        print("\nFinal Content:", final_content)
        
    except ValueError as e:
        print(f"Error in blog generation process: {e}")
        
if __name__ == "__main__":
    main() 