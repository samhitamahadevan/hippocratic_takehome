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
import requests
from PIL import Image as PILImage
from io import BytesIO
import base64

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
IMAGE_GEN_API_KEY = os.getenv("IMAGE_GEN_API_KEY") 
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
                        "description": "Character faces specific obstacles and meets helpers",
                        "emotional_tone": "challenging but hopeful",
                        "age_adaptations": {
                            "5-6": "Simple problems with friendly helpers",
                            "7-8": "Puzzles to solve with teammates",
                            "9-10": "Complex challenges requiring multiple attempts"
                        },
                        "specific_requirements": {
                            "challenges": [
                                "Physical obstacle (bridge, mountain, river)",
                                "Mental challenge (riddle, puzzle, test)",
                                "Emotional challenge (fear, doubt, loneliness)"
                            ],
                            "helpers": [
                                "Wise mentor with specific knowledge",
                                "Loyal friend with unique skills",
                                "Unexpected ally with special abilities"
                            ],
                            "interactions": [
                                "Show how each helper is met",
                                "Describe their unique appearance and personality",
                                "Explain how they help with specific challenges"
                            ]
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
                        },
                        "specific_requirements": {
                            "victory_elements": [
                                "Show the exact moment of success",
                                "Describe how the challenge is overcome",
                                "Include the emotional impact"
                            ],
                            "learning_elements": [
                                "Specific lesson learned",
                                "How the character changed",
                                "What they can do now that they couldn't before"
                            ]
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
                        "description": "Specific misunderstanding or conflict arises between friends",
                        "emotional_tone": "sad but hopeful",
                        "age_adaptations": {
                            "5-6": "Simple disagreement about what to play",
                            "7-8": "Misunderstanding about intentions",
                            "9-10": "Complex conflict requiring empathy"
                        },
                        "specific_requirements": {
                            "conflict_types": [
                                "Misunderstanding about actions or words",
                                "Disagreement about how to solve a problem",
                                "Feeling left out or excluded",
                                "Different opinions about what to do"
                            ],
                            "emotional_impact": [
                                "Show how each character feels",
                                "Describe their reactions",
                                "Include their thoughts about the situation"
                            ],
                            "conflict_development": [
                                "How the problem starts",
                                "What makes it worse",
                                "How it affects their friendship"
                            ]
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
                        },
                        "specific_requirements": {
                            "resolution_steps": [
                                "Realizing the misunderstanding",
                                "Expressing feelings clearly",
                                "Listening to each other",
                                "Finding a solution together"
                            ],
                            "emotional_growth": [
                                "Learning to see another's perspective",
                                "Understanding the importance of communication",
                                "Developing empathy and understanding"
                            ],
                            "reconciliation": [
                                "Specific words of apology",
                                "Actions that show forgiveness",
                                "Plans to prevent future misunderstandings"
                            ]
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
            },
            "three_act": {
                "name": "Classic Three-Act Story",
                "stages": [
                    {
                        "name": "Setup",
                        "description": "Introduce characters, setting, and the central conflict",
                        "emotional_tone": "intriguing, engaging",
                        "age_adaptations": {
                            "5-6": "Simple character and one clear problem",
                            "7-8": "Character relationships and building tension",
                            "9-10": "Complex setup with multiple story elements"
                        }
                    },
                    {
                        "name": "Rising Action",
                        "description": "Conflict develops and complications arise",
                        "emotional_tone": "escalating, engaging",
                        "age_adaptations": {
                            "5-6": "Problem gets a bit bigger but not scary",
                            "7-8": "Multiple attempts to solve the problem",
                            "9-10": "Layered complications and character development"
                        }
                    },
                    {
                        "name": "Climax",
                        "description": "The main conflict reaches its peak",
                        "emotional_tone": "intense but appropriate",
                        "age_adaptations": {
                            "5-6": "Clear moment where problem is solved",
                            "7-8": "Exciting resolution requiring character's best effort",
                            "9-10": "Pivotal moment showing character's growth"
                        }
                    },
                    {
                        "name": "Resolution",
                        "description": "Conflicts are resolved and loose ends tied up",
                        "emotional_tone": "resolved, peaceful",
                        "age_adaptations": {
                            "5-6": "Everything works out happily",
                            "7-8": "Consequences addressed, lessons learned",
                            "9-10": "Character reflection and future implications"
                        }
                    }
                ],
                "description": "Setup, confrontation, and resolution in three clear parts",
                "themes": ["conflict resolution", "character development", "cause and effect"]
            },
            "problem_solution": {
                "name": "Problem and Solution",
                "stages": [
                    {
                        "name": "Happy Beginning",
                        "description": "Character is content in their world",
                        "emotional_tone": "cheerful, content",
                        "age_adaptations": {
                            "5-6": "Simple, happy activity",
                            "7-8": "Character enjoying time with others",
                            "9-10": "Character's normal life with small details"
                        }
                    },
                    {
                        "name": "Problem Appears",
                        "description": "A manageable problem disrupts the happiness",
                        "emotional_tone": "concerned but not scared",
                        "age_adaptations": {
                            "5-6": "Very simple problem (toy broken, friend sad)",
                            "7-8": "Problem affecting multiple characters",
                            "9-10": "Problem requiring thought and planning"
                        }
                    },
                    {
                        "name": "First Attempts",
                        "description": "Character tries to solve the problem",
                        "emotional_tone": "determined, trying",
                        "age_adaptations": {
                            "5-6": "One simple attempt that almost works",
                            "7-8": "Two different approaches tried",
                            "9-10": "Multiple creative solutions attempted"
                        }
                    },
                    {
                        "name": "Breakthrough",
                        "description": "Character finds the right solution",
                        "emotional_tone": "excited, proud",
                        "age_adaptations": {
                            "5-6": "Simple solution that works perfectly",
                            "7-8": "Solution that helps everyone involved",
                            "9-10": "Creative solution showing character growth"
                        }
                    },
                    {
                        "name": "Happy Ending",
                        "description": "Problem solved, everyone happy, lesson learned",
                        "emotional_tone": "joyful, peaceful",
                        "age_adaptations": {
                            "5-6": "Simple celebration of success",
                            "7-8": "Sharing success with others",
                            "9-10": "Reflection on what was learned"
                        }
                    }
                ],
                "description": "Simple structure: problem appears, attempts are made, solution found",
                "themes": ["problem-solving", "persistence", "helping others", "creativity"]
            },
            "learning": {
                "name": "Learning and Growth",
                "stages": [
                    {
                        "name": "Curiosity or Need",
                        "description": "Character encounters something they want or need to learn",
                        "emotional_tone": "curious, interested",
                        "age_adaptations": {
                            "5-6": "Want to do something others can do",
                            "7-8": "Need skill for specific goal or activity",
                            "9-10": "Complex problem requiring new knowledge"
                        }
                    },
                    {
                        "name": "First Attempts",
                        "description": "Character tries but struggles with new skill",
                        "emotional_tone": "trying, frustrated but not giving up",
                        "age_adaptations": {
                            "5-6": "One attempt that doesn't work perfectly",
                            "7-8": "Multiple attempts with gradual improvement",
                            "9-10": "Complex learning process with setbacks"
                        }
                    },
                    {
                        "name": "Getting Help",
                        "description": "Character seeks or receives guidance",
                        "emotional_tone": "humble, receptive",
                        "age_adaptations": {
                            "5-6": "Simple help from parent or friend",
                            "7-8": "Learning from teacher or mentor",
                            "9-10": "Multiple sources of help and advice"
                        }
                    },
                    {
                        "name": "Practice and Progress",
                        "description": "Character practices and slowly improves",
                        "emotional_tone": "determined, gradually more confident",
                        "age_adaptations": {
                            "5-6": "Simple practice with visible improvement",
                            "7-8": "Structured practice with milestones",
                            "9-10": "Self-directed practice and goal-setting"
                        }
                    },
                    {
                        "name": "Success and Sharing",
                        "description": "Character masters the skill and teaches or helps others",
                        "emotional_tone": "proud, generous",
                        "age_adaptations": {
                            "5-6": "Simple success and showing others",
                            "7-8": "Helping friend learn the same skill",
                            "9-10": "Using new skill to solve problems for others"
                        }
                    }
                ],
                "description": "Character learns new skill or concept through experience",
                "themes": ["learning", "persistence", "growth mindset", "asking for help", "sharing knowledge"]
            },
            "bedtime_gentle": {
                "name": "Gentle Bedtime Journey",
                "stages": [
                    {
                        "name": "Peaceful Setting",
                        "description": "Establish a calm, beautiful, safe environment",
                        "emotional_tone": "peaceful, serene",
                        "age_adaptations": {
                            "5-6": "Simple, cozy place like bedroom or garden",
                            "7-8": "Magical but gentle setting like starlit meadow",
                            "9-10": "Rich, peaceful world with calming details"
                        }
                    },
                    {
                        "name": "Gentle Activity",
                        "description": "Character engages in calm, pleasant activity",
                        "emotional_tone": "content, relaxed",
                        "age_adaptations": {
                            "5-6": "Simple activity like watching clouds",
                            "7-8": "Gentle exploration or quiet conversation",
                            "9-10": "Thoughtful activity like stargazing"
                        }
                    },
                    {
                        "name": "Quiet Wisdom",
                        "description": "Character learns gentle lesson or gains peaceful insight",
                        "emotional_tone": "wise, calm",
                        "age_adaptations": {
                            "5-6": "Simple realization about kindness or beauty",
                            "7-8": "Gentle lesson about nature or friendship",
                            "9-10": "Deeper insight about life or relationships"
                        }
                    },
                    {
                        "name": "Sleepy Conclusion",
                        "description": "Story winds down with character feeling peaceful and sleepy",
                        "emotional_tone": "drowsy, secure",
                        "age_adaptations": {
                            "5-6": "Character getting sleepy and cozy",
                            "7-8": "Peaceful ending with character resting",
                            "9-10": "Contemplative, drowsy conclusion"
                        }
                    }
                ],
                "description": "Calm, soothing story arc designed to help children wind down",
                "themes": ["peace", "comfort", "nature", "reflection", "security"]
            }
        }
        self.image_cache = {}  
        
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
3. Three-Act - for stories with a clear setup, rising action, climax, and resolution
4. Problem and Solution - for stories about solving problems
5. Learning and Growth - for stories about learning new skills or concepts
6. Bedtime Gentle - for calming bedtime stories

Respond with just the name of the arc (hero's_journey, friendship, three_act, problem_solution, learning, bedtime_gentle)."""
        
        arc_choice = self.call_model(prompt, temperature=0.3).strip().lower()
        return arc_choice if arc_choice in self.story_arcs else "hero's_journey" 
        
    def generate_story_prompt(self, user_input: str) -> str:
        """Generate a prompt for story creation."""
        selected_arc = self.select_story_arc(user_input)
        arc_info = self.story_arcs[selected_arc]
        
        age_category = "7-8"  
        
        story_structure = "\n".join([
            f"\n{stage['name']}:\n"
            f"Purpose: {stage['description']}\n"
            f"Emotional Tone: {stage['emotional_tone']}\n"
            f"Age-Appropriate Approach: {stage['age_adaptations'][age_category]}"
            for stage in arc_info['stages']
        ])
        
        return f"""Create a rich, detailed, and engaging bedtime story (for ages 5-10) based on the following request: "{user_input}"

IMPORTANT: The story MUST be between 1500-2000 words in length. This is a strict requirement.

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
     * Include the actual riddle and solution
     * Show the characters' thought process
     * Include their discussion about the riddle
   - For bridges or obstacles, describe:
     * What made them dangerous (rotting wood, missing planks, etc.)
     * How the characters overcame them
     * What they felt while doing it
     * What they learned about courage or perseverance
     * Show the specific steps they took to cross
     * Include any tools or help they used
     * Describe the physical sensations (sweaty palms, racing heart, etc.)
     * Show how they supported each other
   - For each challenge, show:
     * The initial attempt
     * What went wrong (if anything)
     * How they adjusted their approach
     * The final solution
     * What they learned from the process
     * The emotional impact on each character
   - For each new character introduced:
     * Show their first meeting in detail
     * Include their initial conversation
     * Describe how they decide to work together
     * Show their unique contributions to the team
   - Create clear cause-and-effect relationships
   - Build tension and resolution naturally
   - Show the thought process behind each solution
   - Include specific dialogue during challenges
   - Show how each character contributes to solving problems

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
   - The story MUST be between 1500-2000 words in length
   - This is a strict requirement - do not make the story shorter
   - Balance action scenes with quieter moments
   - Include enough detail to paint vivid pictures
   - Maintain steady pacing throughout
   - Allow time for reflection and learning
   - Give each scene enough space to develop fully
   - Ensure each character interaction and challenge is fully developed
   - Include enough detail to make the story immersive and engaging
   - Each major scene should be at least 200-300 words
   - Each character introduction should be at least 150-200 words
   - Each challenge and its resolution should be at least 250-300 words

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

Format the story with clear paragraphs, engaging dialogue, and rich descriptions. Make each scene come alive with specific details and sensory information. Remember to name every character and describe specific encounters rather than using general terms. NEVER use vague phrases like "faced challenges" or "overcame obstacles" - always describe exactly what happened. Most importantly, ensure the story shows the main character learning and growing throughout the journey, not just at the end. Make each scene detailed and specific, showing exactly how characters meet, interact, and learn from each other.

IMPORTANT: The story MUST be between 1500-2000 words in length. This is a strict requirement."""

    def judge_story_prompt(self, story: str) -> str:
        """Generate a prompt for story evaluation."""
        return f"""Evaluate this children's story (ages 5-10) and provide feedback in JSON format with the following criteria. Please evaluate it fairly without bias:
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

    def generate_image(self, scene_description: str) -> str:
        """Generate an image for a story scene using the image generation API."""
        try:
            # Temporarily set the API key for image generation
            original_api_key = openai.api_key
            openai.api_key = IMAGE_GEN_API_KEY
            
            # Create image using the openai module directly
            response = openai.Image.create(
                prompt=f"Children's book illustration style: {scene_description}",
                n=1,
                size="512x512",
                response_format="b64_json"
            )
            
            # Restore the original API key for story generation
            openai.api_key = original_api_key
            
            if response and 'data' in response:
                # Get the base64 image data
                image_data = response['data'][0]['b64_json']
                
                # Save the image
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_filename = f"story_image_{timestamp}.png"
                
                with open(image_filename, "wb") as f:
                    f.write(base64.b64decode(image_data))
                
                return image_filename
            else:
                console.print("[red]No image data received from the API[/red]")
                return None
                
        except Exception as e:
            # Make sure to restore the original API key even if there's an error
            openai.api_key = original_api_key
            console.print(f"[red]Error in image generation: {str(e)}[/red]")
            return None

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
        
        # Split story into scenes and generate images
        paragraphs = story.split('\n\n')
        for i, paragraph in enumerate(paragraphs):
            if paragraph.strip():
                # Add story paragraph
                story_content.append(Paragraph(paragraph, body_style))
                story_content.append(Spacer(1, 12))
                
                # Generate image for every third paragraph (to avoid too many images)
                if i % 3 == 0:
                    # Create a scene description for image generation
                    scene_description = f"Children's book illustration of: {paragraph[:200]}"
                    
                    # Check if we already have this image in cache
                    if scene_description not in self.image_cache:
                        image_filename = self.generate_image(scene_description)
                        if image_filename:
                            self.image_cache[scene_description] = image_filename
                    
                    # Add image if we have it
                    if scene_description in self.image_cache:
                        try:
                            img = Image(self.image_cache[scene_description], width=400, height=400)
                            story_content.append(img)
                            story_content.append(Spacer(1, 20))
                        except Exception as e:
                            console.print(f"[yellow]Warning: Could not add image to PDF: {str(e)}[/yellow]")
        
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
        
        # Clean up generated images
        for image_file in self.image_cache.values():
            try:
                os.remove(image_file)
            except:
                pass
        
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
