import os
import openai
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from datetime import datetime
import random

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
console = Console()

class StoryGenerator:
    def __init__(self):
        self.story_history = []
        self.story_arcs = {
            "hero's_journey": {
                "name": "Hero's Journey",
                "stages": [
                    {
                        "name": "Ordinary World",
                        "description": "Introduce the character in their normal, everyday life",
                        "emotional_tone": "comfortable, familiar",
                        "age_adaptations": {
                            "5-6": "Show simple daily routine (playing, eating, sleeping)",
                            "7-8": "Include family, friends, and favorite activities",
                            "9-10": "Add personality traits and small challenges"
                        }
                    },
                    {
                        "name": "Call to Adventure",
                        "description": "Something happens that starts the adventure",
                        "emotional_tone": "exciting, curious",
                        "age_adaptations": {
                            "5-6": "Simple discovery (lost toy, new friend)",
                            "7-8": "Invitation to help someone or explore somewhere",
                            "9-10": "Mystery to solve or challenge to accept"
                        }
                    },
                    {
                        "name": "Journey Begins",
                        "description": "Character starts their adventure",
                        "emotional_tone": "determined, hopeful",
                        "age_adaptations": {
                            "5-6": "Taking first steps with excitement",
                            "7-8": "Planning and preparing for the journey",
                            "9-10": "Showing courage despite uncertainty"
                        }
                    },
                    {
                        "name": "Challenges and Helpers",
                        "description": "Character faces obstacles but also finds help",
                        "emotional_tone": "challenging but hopeful",
                        "age_adaptations": {
                            "5-6": "Simple problems with friendly helpers",
                            "7-8": "Puzzles to solve with teammates",
                            "9-10": "Complex challenges requiring multiple attempts"
                        }
                    },
                    {
                        "name": "Victory and Learning",
                        "description": "Character succeeds and learns important lesson",
                        "emotional_tone": "triumphant, wise",
                        "age_adaptations": {
                            "5-6": "Simple success with clear lesson",
                            "7-8": "Achievement through perseverance",
                            "9-10": "Complex victory showing character growth"
                        }
                    },
                    {
                        "name": "Return Home",
                        "description": "Character returns changed and shares wisdom",
                        "emotional_tone": "satisfied, peaceful",
                        "age_adaptations": {
                            "5-6": "Happy return with simple sharing",
                            "7-8": "Sharing adventure with family/friends",
                            "9-10": "Reflection on growth and change"
                        }
                    }
                ],
                "description": "A transformative journey where the hero overcomes challenges and returns changed",
                "themes": ["courage", "growth", "adventure", "friendship", "perseverance"]
            },
            "friendship": {
                "name": "Friendship Story",
                "stages": [
                    {
                        "name": "Loneliness or New Situation",
                        "description": "Character needs a friend or meets someone new",
                        "emotional_tone": "hopeful, open",
                        "age_adaptations": {
                            "5-6": "Want to play with someone new",
                            "7-8": "Starting school or moving to new place",
                            "9-10": "Complex social situation requiring friendship"
                        }
                    },
                    {
                        "name": "First Connection",
                        "description": "Characters begin to interact",
                        "emotional_tone": "tentative, curious",
                        "age_adaptations": {
                            "5-6": "Simple sharing or playing together",
                            "7-8": "Discovering common interests",
                            "9-10": "Meaningful conversation or shared experience"
                        }
                    },
                    {
                        "name": "Friendship Challenge",
                        "description": "Misunderstanding or conflict arises between friends",
                        "emotional_tone": "sad but hopeful",
                        "age_adaptations": {
                            "5-6": "Simple disagreement about what to play",
                            "7-8": "Misunderstanding about intentions",
                            "9-10": "Complex conflict requiring empathy"
                        }
                    },
                    {
                        "name": "Understanding and Forgiveness",
                        "description": "Characters work through their differences",
                        "emotional_tone": "understanding, caring",
                        "age_adaptations": {
                            "5-6": "Simple apology and making up",
                            "7-8": "Talking through the problem together",
                            "9-10": "Deep understanding and compromise"
                        }
                    },
                    {
                        "name": "Stronger Friendship",
                        "description": "Friendship is stronger after working through challenges",
                        "emotional_tone": "warm, secure",
                        "age_adaptations": {
                            "5-6": "Playing happily together again",
                            "7-8": "Celebrating their friendship",
                            "9-10": "Deeper bond and mutual support"
                        }
                    }
                ],
                "description": "A story about the power of friendship and overcoming obstacles together",
                "themes": ["friendship", "empathy", "communication", "forgiveness", "social skills"]
            }
        }
        
    def call_model(self, prompt: str, max_tokens=3000, temperature=0.7) -> str:
        """Call the OpenAI API with the given prompt."""
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                stream=False,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return resp.choices[0].message["content"]
        except Exception as e:
            console.print(f"[red]Error calling OpenAI API: {str(e)}[/red]")
            return ""

    def select_story_arc(self, user_input: str) -> str:
        """Select the most appropriate story arc based on the user input."""
        prompt = f"""Based on this story request: "{user_input}", which story arc would be most appropriate? Choose from:
1. Hero's Journey - for adventure and transformation stories
2. Friendship - for stories about relationships and teamwork

Respond with just the name of the arc (hero's_journey or friendship)."""
        
        arc_choice = self.call_model(prompt, temperature=0.3).strip().lower()
        return arc_choice if arc_choice in self.story_arcs else "hero's_journey"  # default to hero's journey
        
    def generate_story_prompt(self, user_input: str) -> str:
        """Generate a prompt for story creation."""
        selected_arc = self.select_story_arc(user_input)
        arc_info = self.story_arcs[selected_arc]
        
        # Determine age category based on story complexity
        age_category = "7-8"  # default to middle range
        
        story_structure = "\n".join([
            f"\n{stage['name']}:\n"
            f"Purpose: {stage['description']}\n"
            f"Emotional Tone: {stage['emotional_tone']}\n"
            f"Age-Appropriate Approach: {stage['age_adaptations'][age_category]}"
            for stage in arc_info['stages']
        ])
        
        return f"""Create a rich, detailed, and engaging bedtime story (for ages 5-10) based on the following request: "{user_input}"

Story Arc: {arc_info['name']}
Description: {arc_info['description']}
Themes: {', '.join(arc_info['themes'])}

Story Structure:
{story_structure}

Detailed Requirements:
1. Character Development and Growth:
   - Give EVERY character a unique name and personality
   - Include detailed physical descriptions and unique traits
   - Show character growth THROUGHOUT the story, not just at the end
   - For the main character, show:
     * What they believe or know at the start
     * How their understanding changes with each challenge
     * Small lessons learned from each encounter
     * How their perspective shifts throughout the story
     * What mistakes they make and what they learn from them
   - For each new character introduced:
     * Describe exactly how and where they meet
     * Show their first interaction in detail
     * Include their initial reaction to each other
     * Describe their unique way of speaking and moving
     * Show how their relationship develops
   - Add meaningful dialogue that reveals character growth
   - When introducing new characters, give them names and describe their appearance

2. Setting and Atmosphere:
   - Create vivid, sensory-rich descriptions of locations
   - Use all five senses in descriptions (sight, sound, smell, touch, taste)
   - Include weather, time of day, and environmental details
   - Make the setting feel alive and interactive
   - Describe how the setting changes as the story progresses

3. Plot and Structure:
   - Follow the story arc structure while adding rich details
   - NEVER use vague descriptions like "faced challenges" or "overcame obstacles"
   - For each challenge, describe:
     * Exactly what the challenge was
     * How it looked, sounded, and felt
     * Why it was difficult
     * How the characters solved it
     * What they learned from it
   - For example, instead of "they solved riddles", write:
     * The specific riddle they had to solve
     * How they figured it out
     * What made it tricky
     * What they learned about themselves or others
     * Show the exact moment of realization
   - For bridges or obstacles, describe:
     * What made them dangerous (rotting wood, missing planks, etc.)
     * How the characters overcame them
     * What they felt while doing it
     * What they learned about courage or perseverance
   - Create clear cause-and-effect relationships
   - Build tension and resolution naturally

4. Language and Style:
   - Use age-appropriate but engaging vocabulary
   - Include descriptive adjectives and adverbs
   - Vary sentence structure for rhythm
   - Add gentle humor where appropriate
   - Use metaphors and similes suitable for children
   - Create vivid imagery that brings scenes to life

5. Emotional Engagement:
   - Create emotional moments that resonate
   - Show characters' feelings through actions and dialogue
   - Include moments of wonder and discovery
   - Balance excitement with calm moments
   - Show how emotions change as characters learn and grow
   - Include moments of tension and release

6. Educational Elements and Life Lessons:
   - Include a clear, meaningful moral or life lesson that children can understand and apply
   - The lesson should be naturally woven into the story, not just stated at the end
   - Show the consequences of both good and bad choices
   - Demonstrate positive values like:
     * Perseverance and never giving up
     * Kindness and empathy
     * Courage in the face of fear
     * Friendship and teamwork
     * Honesty and trust
     * Responsibility and consequences
     * Self-confidence and believing in oneself
   - Make the lesson relatable to children's everyday lives
   - Show how the characters grow and learn from their experiences
   - Include multiple small lessons throughout the story
   - Show exactly how each lesson is learned through specific events

7. Story Length and Pacing:
   - Aim for 1500-2000 words for a rich, detailed story
   - Balance action scenes with quieter moments
   - Include enough detail to paint vivid pictures
   - Maintain steady pacing throughout
   - Allow time for reflection and learning
   - Give each scene enough space to develop fully
   - Ensure each character interaction and challenge is fully developed
   - Include enough detail to make the story immersive and engaging

8. Dialogue Requirements:
   - Make dialogue natural and character-specific
   - Include emotional expressions
   - Use dialogue to advance the plot
   - Show relationships through conversation
   - Give each character a unique way of speaking
   - Use dialogue to show learning and growth
   - Include meaningful conversations that reveal character

9. Sensory Details:
   - Describe how things look, sound, feel, smell, and taste
   - Include environmental sounds and textures
   - Add weather and time-of-day details
   - Make the world feel tangible and real
   - Use sensory details to create atmosphere

10. Ending Requirements:
    - Provide a satisfying conclusion that reinforces the story's moral
    - Show how the characters have grown and learned
    - Include a clear but gentle reminder of the lesson learned
    - Leave room for imagination while ensuring the message is clear
    - End with a positive, hopeful note that encourages children to apply the lesson
    - Show how the main character's understanding has changed from the beginning
    - Tie up all major story threads

11. Specific Encounters:
    - For each challenge, include:
      * The exact nature of the challenge
      * What made it difficult or dangerous
      * How the characters felt about it
      * The specific steps they took to overcome it
      * What they learned from it
      * How their understanding changed
    - Make each encounter unique and memorable
    - Show the consequences of their actions
    - Connect each challenge to the story's main lesson
    - Show how each challenge contributes to the character's growth
    - Include specific details that make each encounter special

Format the story with clear paragraphs, engaging dialogue, and rich descriptions. Make each scene come alive with specific details and sensory information. Remember to name every character and describe specific encounters rather than using general terms. NEVER use vague phrases like "faced challenges" or "overcame obstacles" - always describe exactly what happened. Most importantly, ensure the story shows the main character learning and growing throughout the journey, not just at the end. Make each scene detailed and specific, showing exactly how characters meet, interact, and learn from each other."""

    def judge_story_prompt(self, story: str) -> str:
        """Generate a prompt for story evaluation."""
        return f"""Evaluate this children's story (ages 5-10) and provide feedback in JSON format with the following criteria:
1. Age-appropriateness (1-10)
2. Story structure and arc adherence (1-10)
3. Educational value (1-10)
4. Entertainment value (1-10)
5. Language clarity and richness (1-10)
6. Length appropriateness (1-10)
7. Emotional tone consistency (1-10)
8. Character development (1-10)
9. Setting and atmosphere (1-10)
10. Dialogue quality (1-10)
11. Sensory detail richness (1-10)
12. Overall score (1-10)
13. Specific suggestions for improvement

Story to evaluate:
{story}

Provide the response in valid JSON format with these exact keys: age_appropriateness, story_structure, educational_value, entertainment_value, language_clarity, length_appropriateness, emotional_tone, character_development, setting_atmosphere, dialogue_quality, sensory_details, overall_score, suggestions"""

    def generate_story(self, user_input: str) -> tuple[str, dict]:
        """Generate a story and get judge feedback."""
        # Generate initial story
        story_prompt = self.generate_story_prompt(user_input)
        story = self.call_model(story_prompt)
        
        # Get judge feedback
        judge_prompt = self.judge_story_prompt(story)
        judge_feedback = self.call_model(judge_prompt, temperature=0.3)
        
        try:
            feedback = json.loads(judge_feedback)
        except json.JSONDecodeError:
            feedback = {
                "error": "Could not parse judge feedback",
                "raw_feedback": judge_feedback
            }
        
        return story, feedback

    def generate_pdf(self, story: str, feedback: dict, user_input: str) -> str:
        """Generate a PDF version of the story with illustrations and feedback."""
        # Create a filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bedtime_story_{timestamp}.pdf"
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Create custom styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#2E4053')
        )
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            textColor=colors.HexColor('#566573')
        )
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            leading=18
        )
        feedback_style = ParagraphStyle(
            'CustomFeedback',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#7F8C8D'),
            spaceAfter=12
        )
        
        # Build the PDF content
        story_content = []
        
        # Add title
        story_content.append(Paragraph("A Magical Bedtime Story", title_style))
        story_content.append(Spacer(1, 20))
        
        # Add subtitle with the story request
        story_content.append(Paragraph(f"Based on: {user_input}", subtitle_style))
        story_content.append(Spacer(1, 30))
        
        # Add the story content
        for paragraph in story.split('\n\n'):
            if paragraph.strip():
                story_content.append(Paragraph(paragraph, body_style))
                story_content.append(Spacer(1, 12))
        
        # Add feedback section if available
        if "error" not in feedback:
            story_content.append(Spacer(1, 30))
            story_content.append(Paragraph("Story Evaluation", subtitle_style))
            
            metrics = [
                ("Age Appropriateness", feedback.get("age_appropriateness", "N/A")),
                ("Story Structure", feedback.get("story_structure", "N/A")),
                ("Educational Value", feedback.get("educational_value", "N/A")),
                ("Entertainment Value", feedback.get("entertainment_value", "N/A")),
                ("Language Clarity", feedback.get("language_clarity", "N/A")),
                ("Length Appropriateness", feedback.get("length_appropriateness", "N/A")),
                ("Emotional Tone", feedback.get("emotional_tone", "N/A")),
                ("Character Development", feedback.get("character_development", "N/A")),
                ("Setting and Atmosphere", feedback.get("setting_atmosphere", "N/A")),
                ("Dialogue Quality", feedback.get("dialogue_quality", "N/A")),
                ("Sensory Details", feedback.get("sensory_details", "N/A")),
                ("Overall Score", feedback.get("overall_score", "N/A"))
            ]
            
            for metric, score in metrics:
                story_content.append(Paragraph(f"{metric}: {score}/10", feedback_style))
            
            if "suggestions" in feedback:
                story_content.append(Spacer(1, 12))
                story_content.append(Paragraph("Suggestions for Improvement:", feedback_style))
                story_content.append(Paragraph(feedback["suggestions"], feedback_style))
        
        # Build the PDF
        doc.build(story_content)
        
        return filename

    def display_story(self, story: str, feedback: dict, user_input: str):
        """Display the story and feedback in a nice format."""
        console.print("\n")
        console.print(Panel(Markdown(story), title="Your Bedtime Story", border_style="blue"))
        
        if "error" not in feedback:
            console.print("\n[bold]Story Evaluation:[/bold]")
            metrics = [
                ("Age Appropriateness", feedback.get("age_appropriateness", "N/A")),
                ("Story Structure", feedback.get("story_structure", "N/A")),
                ("Educational Value", feedback.get("educational_value", "N/A")),
                ("Entertainment Value", feedback.get("entertainment_value", "N/A")),
                ("Language Clarity", feedback.get("language_clarity", "N/A")),
                ("Length Appropriateness", feedback.get("length_appropriateness", "N/A")),
                ("Emotional Tone", feedback.get("emotional_tone", "N/A")),
                ("Character Development", feedback.get("character_development", "N/A")),
                ("Setting and Atmosphere", feedback.get("setting_atmosphere", "N/A")),
                ("Dialogue Quality", feedback.get("dialogue_quality", "N/A")),
                ("Sensory Details", feedback.get("sensory_details", "N/A")),
                ("Overall Score", feedback.get("overall_score", "N/A"))
            ]
            
            for metric, score in metrics:
                console.print(f"{metric}: {score}/10")
            
            if "suggestions" in feedback:
                console.print("\n[bold]Suggestions for Improvement:[/bold]")
                console.print(feedback["suggestions"])
            
            # Generate PDF
            pdf_filename = self.generate_pdf(story, feedback, user_input)
            console.print(f"\n[green]Your story has been saved as: {pdf_filename}[/green]")

def main():
    console.print("[bold blue]Welcome to the Magical Story Generator![/bold blue]")
    console.print("I'll create a special bedtime story just for you! 🎨✨")
    
    generator = StoryGenerator()
    
    while True:
        console.print("\n[bold]What kind of story would you like to hear?[/bold]")
        console.print("1. Tell me what kind of story you want")
        console.print("2. Surprise me with a random story")
        console.print("(or type 'exit' to quit)")
        
        user_input = console.input("\n> ")
        
        if user_input.lower() == 'exit':
            break
            
        if user_input.lower() in ['2', 'surprise me', 'random', 'random story']:
            # Generate a random story prompt
            random_prompts = [
                "A magical garden where flowers can talk",
                "A young dragon learning to fly",
                "A friendly robot making new friends",
                "A space adventure with talking planets",
                "A magical library where books come to life",
                "A young wizard's first spell",
                "A friendly monster under the bed",
                "A journey to the center of a rainbow",
                "A day in the life of a cloud",
                "A magical treehouse in the forest"
            ]
            user_input = random.choice(random_prompts)
            console.print(f"\n[bold]I'll create a story about: {user_input}[/bold]")
            
        with console.status("[bold green]Creating your magical story...[/bold green]"):
            story, feedback = generator.generate_story(user_input)
            generator.display_story(story, feedback, user_input)
        
        console.print("\n[bold]Would you like another story?[/bold]")

if __name__ == "__main__":
    main() 