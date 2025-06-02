import httpx
import json
from typing import List, Dict, Optional

class ImageGenerator:
    def __init__(self):
        self.base_url = "https://api.unsplash.com"
        # Using the demo access key which is rate-limited but requires no signup
        self.access_key = "demo"
        
    async def get_section_image(self, section_title: str, description: str) -> Optional[Dict]:
        """
        Fetch a relevant image for a blog section using Unsplash API
        """
        try:
            search_query = f"{section_title} {description}"
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/photos/random",
                    params={
                        "query": search_query,
                        "client_id": self.access_key,
                        "orientation": "landscape"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "url": data["urls"]["regular"],
                        "description": data["description"] or data["alt_description"],
                        "photographer": data["user"]["name"],
                        "photographer_url": data["user"]["links"]["html"]
                    }
                return None
        except Exception as e:
            print(f"Error fetching image: {str(e)}")
            return None
            
    async def get_images_for_blog(self, sections: List[Dict]) -> List[Dict]:
        """
        Fetch images for all blog sections
        """
        enriched_sections = []
        for section in sections:
            image_data = await self.get_section_image(
                section["title"],
                section.get("content", "")[:100]  # Use first 100 chars of content for context
            )
            section["image"] = image_data
            enriched_sections.append(section)
        return enriched_sections

    def format_image_markdown(self, image_data: Dict) -> str:
        """
        Format image data into markdown with proper attribution
        """
        if not image_data:
            return ""
            
        return f"""
![{image_data['description']}]({image_data['url']})
*Photo by [{image_data['photographer']}]({image_data['photographer_url']}) on Unsplash*
""" 