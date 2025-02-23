# models/damage_assessment.py
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from session.llm_session import LLMSession

@dataclass
class DamageAssessment:
    """Data class for storing damage assessment results."""
    description: str
    estimated_cost: Optional[Dict[str, float]] = None
    confidence_level: Optional[float] = None
    repair_details: Optional[Dict] = None

class AutomaticDamageAssessment(LLMSession):
    """Handles the automated damage assessment process using vision and text models."""
    
    def __init__(self, property_info: Optional[str] = None):
        super().__init__()
        self.property_info = property_info
        self.current_assessment: Optional[DamageAssessment] = None
        self.assessment_complete = False
        self.max_iterations = 10

    def _extract_command(self, text_response: str) -> Tuple[str, str]:
        """Extract command type and content from text model response."""
        lines = text_response.split('\n')
        for line in lines:
            if line.strip().lower().startswith('prompt:'):
                return 'prompt', line[7:].strip()
            elif line.strip().lower().startswith('end:'):
                return 'end', text_response[text_response.lower().find('end:') + 4:].strip()
        return 'unknown', text_response

    def _parse_cost_estimate(self, estimate_text: str) -> Dict:
        """Parse the cost estimate text into structured data."""
        try:
            # Extract total cost range
            lines = estimate_text.split('\n')
            cost_line = next(line for line in lines if 'Total Estimated Cost:' in line)
            cost_range = cost_line.split(':')[1].strip()
            min_cost, max_cost = self._extract_cost_range(cost_range)

            # Parse breakdown if present
            breakdown = self._parse_cost_breakdown(estimate_text)

            return {
                'total_cost_range': {'min': min_cost, 'max': max_cost},
                'breakdown': breakdown,
                'notes': self._extract_notes(estimate_text)
            }
        except Exception as e:
            raise ValueError(f"Failed to parse cost estimate: {str(e)}")

    def _extract_cost_range(self, cost_range: str) -> Tuple[float, float]:
        """Extract minimum and maximum costs from a range string."""
        # Clean the string of any markdown or special characters
        cleaned = cost_range.replace('*', '').replace('$', '').replace(',', '').strip()
        
        # Split on various possible delimiters
        if ' to ' in cleaned:
            min_str, max_str = cleaned.split(' to ')
        elif '-' in cleaned:
            min_str, max_str = cleaned.split('-')
        else:
            raise ValueError(f"Could not parse cost range from: {cost_range}")
            
        try:
            return float(min_str.strip()), float(max_str.strip())
        except ValueError as e:
            raise ValueError(f"Could not convert costs to numbers: {min_str}, {max_str}")

    def _parse_cost_breakdown(self, estimate_text: str) -> Dict:
        """Parse the breakdown section of the cost estimate."""
        breakdown = {}
        if "Breakdown:" in estimate_text:
            # Split into breakdown and notes sections first
            main_sections = estimate_text.split("Notes:", 1)
            
            # Parse the breakdown section
            breakdown_text = main_sections[0].split("Breakdown:")[1].strip()
            sections = breakdown_text.split('\n\n')[0].split('\n')
            
            for section in sections:
                if ':' in section:
                    category, amount = section.split(':', 1)
                    amount = amount.strip()
                    if '-' in amount:
                        min_val, max_val = self._extract_cost_range(amount)
                        breakdown[category.strip()] = {
                            'min': min_val,
                            'max': max_val
                        }
            
            # Add notes if they exist
            if len(main_sections) > 1:
                breakdown['notes'] = main_sections[1].strip()

        return breakdown

    def _extract_notes(self, estimate_text: str) -> Optional[str]:
        """Extract notes from the cost estimate text."""
        return

    async def run_assessment(self, image_path: str, initial_vision_prompt: str) -> Dict:
        """Run the complete automated assessment process."""
        assessment_data = {
            'status': 'in_progress',
            'vision_responses': [],
            'final_assessment': None,
            'error': None,
            'property_info': self.property_info
        }
  

        try:
            # Get initial vision analysis
            initial_analysis = await self._get_initial_analysis(
                image_path, initial_vision_prompt, assessment_data
            )
            
            # Run the assessment loop
            await self._run_assessment_loop(initial_analysis, assessment_data)

            if not self.assessment_complete:
                assessment_data.update({
                    'status': 'incomplete',
                    'error': 'Maximum iterations reached without completion'
                })

        except Exception as e:
            assessment_data.update({
                'status': 'error',
                'error': str(e)
            })
            
        return assessment_data


    async def _get_initial_analysis(
        self, image_path: str, initial_vision_prompt: str, assessment_data: Dict
    ) -> str:
        """Get initial vision analysis of the image."""
        vision_response = await self.ask_vision(initial_vision_prompt, image_path)
        initial_analysis = vision_response["choices"][0]["message"]["content"]
        
        assessment_data['vision_responses'].append({
            'prompt': initial_vision_prompt,
            'response': f"{initial_analysis} Property Info {self.property_info}"
        })
        
        return initial_analysis

    def _create_text_prompt(self, initial_analysis: str) -> str:
        """Create the initial prompt for the text model."""
        return f"""
        You are performing an automated damage assessment based on vision model analysis.
        Here is the initial analysis:
        {initial_analysis}
        
        Based on this information, you should either:
        1. Respond with 'Prompt:' followed by a specific question to get more details from the vision model
        2. If you do not see any significant damage beyond wear and tear, or do not see damage at all. Respond with the complete cost assessment below with all feilds '0' and add an explanation in notes.
        3. Respond with 'End:' followed by a complete cost assessment in this exact format and keep the ranges as small as possible:

        'Total Estimated Cost: $X - $Y
        
        Breakdown:
        Labor: $A - $B
        Materials: $C - $D
        Additional Costs: $E - $F
        Notes: [Fill out with the reasoning behind the estimated cost and breakdown]'
        
        More Guidelines for Cost Assessment:
        - Make sure to reach a resolution and a completed cost assessment using less than eight prompts, using any avaliable information. Try not to repetitively ask the same prompts.
        - ALWAYS start response with either 'Prompt:' or 'End:'
        - Factor in location, property age, and market rates
        - Consider property value impact on material quality
        - Include permit costs and overhead in additional costs
        - Aim for narrower price ranges (max 25% difference between min and max)
        """

    async def _run_assessment_loop(self, initial_analysis: str, assessment_data: Dict):
        """Run the main assessment loop until completion or max iterations."""
        # Create initial conversation context
        conversation_context = self._create_text_prompt(initial_analysis)
        iteration_count = 0

        while not self.assessment_complete and iteration_count < self.max_iterations:
            # Get text model's decision using full context
            text_response = await self.ask_text(conversation_context)
            text_content = text_response["choices"][0]["message"]["content"]
            
            # Process the command
            command, content = self._extract_command(text_content)
            
            if command == 'prompt':
                # Get vision response
                vision_response = await self.ask_vision(content)
                vision_content = vision_response["choices"][0]["message"]["content"]
                
                # Update conversation context with new Q&A
                conversation_context += f"\n\nQuestion: {content}\nResponse: {vision_content}\n\n"
                conversation_context += "Based on all the information above, provide either:\n"
                conversation_context += "1. Another specific question starting with 'Prompt:' if you need more details\n"
                conversation_context += "2. A final cost assessment starting with 'End:' in the exact format specified\n"
                
                # Update assessment data
                assessment_data['vision_responses'].append({
                    'prompt': content,
                    'response': vision_content
                })
            
            elif command == 'end':
                self._handle_end_command(content, initial_analysis, assessment_data)
            else:
                print(f"Unknown command: {command}", content)
                
            iteration_count += 1

    async def _process_command(
        self, 
        command: str, 
        content: str, 
        text_prompt: str, 
        initial_analysis: str,  # Add initial_analysis parameter
        assessment_data: Dict
    ):
        """Process the command from the text model."""
        if command == 'prompt':
            await self._handle_prompt_command(content, text_prompt, assessment_data)
        elif command == 'end':
            self._handle_end_command(content, initial_analysis, assessment_data)
        else:
         
            raise ValueError("Invalid response format from text model")
        
    async def _handle_prompt_command(
        self, content: str, text_prompt: str, assessment_data: Dict
    ):
        """Handle a prompt command from the text model."""
        vision_response = await self.ask_vision(content)
        vision_content = vision_response["choices"][0]["message"]["content"]
        
        assessment_data['vision_responses'].append({
            'prompt': content,
            'response': vision_content
        })
        
        # Update text model context
        text_prompt += f"\n\nNew Information:\nQuestion: {content}\nResponse: {vision_content}"

    def _handle_end_command(
        self, content: str, initial_analysis: str, assessment_data: Dict
    ):
        """Handle an end command from the text model."""
        final_assessment = self._parse_cost_estimate(content)
        
        self.current_assessment = DamageAssessment(
            description=initial_analysis,
            estimated_cost=final_assessment['total_cost_range'],
            repair_details=final_assessment['breakdown']
        )
        
        self.assessment_complete = True
        assessment_data.update({
            'status': 'complete',
            'final_assessment': final_assessment
        })

    def get_current_assessment(self) -> Optional[DamageAssessment]:
        """Get the current assessment if available."""
        return self.current_assessment

    def is_assessment_complete(self) -> bool:
        """Check if the assessment is complete."""
        return self.assessment_complete