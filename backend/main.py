# main.py
import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, Optional, List
from models.damage_assessment import AutomaticDamageAssessment

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DamageAssessmentManager:
    """Manages the damage assessment process for single or multiple images."""
    
    def __init__(self, property_info: Optional[str] = None):
        self.assessor = AutomaticDamageAssessment(property_info=property_info)

    async def process_single_image(self, image_path: str) -> Optional[Dict]:
        """Process a single image and return assessment results."""
        try:
            logger.info(f"Starting assessment for image: {image_path}")
            
            result = await self.assessor.run_assessment(
                image_path=image_path,
                initial_vision_prompt=(
                    f"""1. PRIMARY DAMAGE ASSESSMENT
- What specific type of damage is visible?
- What is the apparent cause of the damage (age, weather, wear, etc.)?
- Precisely describe the visual characteristics of the damage
- Classify the severity: none, minimal, moderate, or severe
- Estimate the approximate age of the damage
- Note any immediate safety concerns

2. EXTENT AND DISTRIBUTION
- What percentage of the visible area shows damage?
- Is the damage localized or widespread?
- Identify all affected components and materials
- Note any patterns in the damage distribution
- Document any signs of progressive deterioration
- Estimate the total affected area in square feet or percentage

3. MATERIAL AND CONSTRUCTION DETAILS
- Identify all visible construction materials
- Note the quality and grade of materials
- Document any visible previous repairs
- Identify any non-standard or specialty materials
- Note the condition of surrounding/adjacent materials
- Identify any architectural features affecting repair

4. REPAIR COMPLEXITY FACTORS
- Assess accessibility for repairs
- Identify potential complications or challenges
- Note any special equipment requirements
- Consider seasonal or weather impact on repairs
- Identify any code compliance considerations
- Document any factors that could affect repair costs

5. UNDERLYING DAMAGE ASSESSMENT
- Are there signs of hidden or structural damage?
- Is there evidence of water infiltration?
- Note any visible mold or moisture damage
- Identify any potential systemic issues
- Document signs of long-term deterioration
- Note any risk factors for future damage

6. ADDITIONAL OBSERVATIONS
- Document any unusual features or conditions
- Note environmental factors affecting the damage
- Identify any maintenance issues contributing to damage
- Record any relevant historical repair evidence
- Note any immediate temporary remediation needs

If you observe NO SIGNIFICANT DAMAGE:
- Explicitly state that no significant damage is visible
- Document the current condition thoroughly
- Note any preventive maintenance recommendations
- Identify any early warning signs to monitor

SUMMARY REQUIREMENTS:
- Provide clear severity classification
- Estimate scope of needed repairs
- List key factors affecting repair costs
- Prioritize repair urgency
- Note any special considerations
Property Info: {self.assessor.property_info}""" 
                )
            )
            
            self._save_results(image_path, result)
            return result
            
        except Exception as e:
            logger.error(f"Failed to process image {image_path}: {str(e)}")
            return None

    async def process_batch(self, image_paths: List[str]) -> Dict[str, Dict]:
        """Process multiple images concurrently."""
        tasks = [self.process_single_image(path) for path in image_paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            path: result for path, result in zip(image_paths, results)
            if result is not None
        }

    def _save_results(self, image_path: str, result: Dict):
        """Save assessment results to a JSON file."""
        output_path = Path(image_path).stem + "_assessment.json"
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        logger.info(f"Assessment saved to {output_path}")

def main():
    """Main entry point for the damage assessment tool."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Property Damage Assessment Tool')
    parser.add_argument('--image', type=str, help='Path to single image')
    parser.add_argument('--batch', type=str, nargs='+', help='Paths to multiple images for batch assessment')
    parser.add_argument('--propertyinfo', type=str, help='Property information string')
    
    args = parser.parse_args()
    
    async def run_assessment():
        if args.propertyinfo:
            manager = DamageAssessmentManager(args.propertyinfo)
        else:
            manager = DamageAssessmentManager()
        
        if args.image:
            result = await manager.process_single_image(args.image)
            if result:
                print(json.dumps(result, indent=2))
                
        elif args.batch:
            results = await manager.process_batch(args.batch)
            for path, result in results.items():
                print(f"\nResults for {path}:")
                print(json.dumps(result, indent=2))
        
        else:
            print("Please provide an image path using --image or --batch")

    try:
        asyncio.run(run_assessment())
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.error(f"Process failed: {str(e)}")

if __name__ == "__main__":
    main()