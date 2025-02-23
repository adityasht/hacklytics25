# main.py
import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, Optional, List
from models.damage_assessment import AutomaticDamageAssessment
import os
import requests
import pandas as pd
import io
from dotenv import load_dotenv

load_dotenv()

RENTCAST_API_KEY = os.getenv("RENTCAST_API_KEY")
RENTCAST_URL = 'https://api.rentcast.io/v1/properties'


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
def retrievePropertyData(address):
    querystring = {"address" : address}

    headers = {
        "accept": "application/json",
        "X-Api-Key": RENTCAST_API_KEY
    }

    response = requests.get(RENTCAST_URL, headers=headers, params=querystring)

    if response.status_code == 200:
        df = pd.DataFrame(response.json()).drop(columns= ['id','addressLine1','addressLine2','assessorID','legalDescription','owner'])
        setGlobalDf(df)
        buffer = io.StringIO()
        df.to_string(buffer)
        return buffer.getvalue()

    else:
        return {"error": f"Failed to fetch data. Status Code: {response.status_code}"}
    
def setGlobalDf(df):
    global global_df
    global_df = df
    
def returnGlobalDf():
    return global_df

def main(images_of_damages, propertyinfo):
    async def run_assessment():
        if propertyinfo:
            manager = DamageAssessmentManager(propertyinfo)
        else:
            manager = DamageAssessmentManager()

        if images_of_damages:
            result = await manager.process_single_image(str(images_of_damages))

            if result:
                return json.dumps(result, indent=2)

        elif images_of_damages.batch:
            results = await manager.process_batch(images_of_damages.batch)
            for path, result in results.items():
            
                return json.dumps(result, indent=2)

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