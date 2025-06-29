from typing import List, Dict, Optional
import random
import httpx
import json
from tools.outline import generate_outline
from tools.sections import write_section
from tools.styler import (
    style_with_emojis,
    format_code_block,
    format_quote,
    format_table
)

class BlogAgent:
    def __init__(self):
        self.topic: str = ""
        self.domain: str = "technology"
        self.outline: List[str] = []
        self.content: Dict[str, str] = {}
        
    async def get_topic_info(self, topic: str) -> Dict[str, str]:
        """Get comprehensive information about any topic from multiple sources."""
        async with httpx.AsyncClient() as client:
            try:
                wiki_response = await client.get(
                    "https://en.wikipedia.org/api/rest_v1/page/summary/" + topic.replace(" ", "_"),
                    headers={'User-Agent': 'BlogGeneratorBot/1.0'},
                    timeout=10.0
                )
                wiki_data = wiki_response.json() if wiki_response.status_code == 200 else {}
                
                dbpedia_response = await client.get(
                    f"https://dbpedia.org/data/{topic.replace(' ', '_')}.json",
                    headers={'User-Agent': 'BlogGeneratorBot/1.0'},
                    timeout=10.0
                )
                dbpedia_data = dbpedia_response.json() if dbpedia_response.status_code == 200 else {}
                
                search_response = await client.get(
                    "https://en.wikipedia.org/w/api.php",
                    params={
                        "action": "query",
                        "format": "json",
                        "list": "search",
                        "srsearch": topic,
                        "srlimit": 10,
                        "srqiprofile": "popular_inclinks_pv",
                        "srprop": "snippet|titlesnippet|sectiontitle|categorysnippet"
                    },
                    headers={'User-Agent': 'BlogGeneratorBot/1.0'},
                    timeout=10.0
                )
                search_data = search_response.json() if search_response.status_code == 200 else {}
                
                topic_info = {
                    "title": wiki_data.get("title", topic),
                    "extract": wiki_data.get("extract", ""),
                    "description": wiki_data.get("description", ""),
                    "thumbnail": wiki_data.get("thumbnail", {}).get("source", ""),
                    "related": [],
                    "metadata": {
                        "categories": [],
                        "external_links": [],
                        "references": []
                    }
                }
                
                if search_data.get("query", {}).get("search"):
                    for result in search_data["query"]["search"][:5]:
                        if result["title"].lower() != topic.lower():
                            topic_info["related"].append({
                                "title": result["title"],
                                "snippet": result.get("snippet", ""),
                                "section": result.get("sectiontitle", ""),
                                "category": result.get("categorysnippet", "")
                            })
                
                if dbpedia_data:
                    resource_uri = f"http://dbpedia.org/resource/{topic.replace(' ', '_')}"
                    if resource_uri in dbpedia_data:
                        resource_info = dbpedia_data[resource_uri]
                        topic_info["metadata"]["external_links"].extend(
                            resource_info.get("http://www.w3.org/2000/01/rdf-schema#seeAlso", [])
                        )
                        
                return topic_info
                
            except Exception as e:
                print(f"Error fetching topic information: {str(e)}")
                return {
                    "title": topic,
                    "extract": "",
                    "description": f"Information about {topic} could not be retrieved.",
                    "thumbnail": "",
                    "related": [],
                    "metadata": {"categories": [], "external_links": [], "references": []}
                }
    
    def analyze_topic(self, topic: str) -> Dict[str, bool]:
        """Analyze topic to determine what elements to include and content structure."""
        topic_lower = topic.lower()
        words = set(topic_lower.split())
        
        domain_keywords = {
            "technology": {
                "code", "programming", "software", "api", "web", "app", "database",
                "cloud", "ai", "machine learning", "cybersecurity", "blockchain",
                "devops", "frontend", "backend", "fullstack", "mobile"
            },
            "medical": {
                "health", "medical", "medicine", "healthcare", "disease", "treatment",
                "diagnosis", "therapy", "clinical", "doctor", "patient", "hospital",
                "surgery", "pharmaceutical", "drug", "vaccine", "anatomy"
            },
            "science": {
                "physics", "chemistry", "biology", "astronomy", "space", "research",
                "experiment", "laboratory", "scientific", "theory", "hypothesis",
                "molecule", "atom", "cell", "galaxy", "planet", "star"
            },
            "fitness": {
                "gym", "workout", "exercise", "fitness", "training", "muscle",
                "strength", "cardio", "nutrition", "diet", "health", "bodybuilding",
                "weight", "yoga", "sports", "athlete", "wellness"
            },
            "finance": {
                "money", "finance", "investment", "stock", "market", "trading",
                "cryptocurrency", "banking", "economy", "financial", "budget",
                "wealth", "asset", "portfolio", "fund", "revenue", "profit"
            },
            "business": {
                "business", "startup", "entrepreneur", "management", "marketing",
                "strategy", "leadership", "company", "corporate", "enterprise",
                "innovation", "growth", "sales", "customer", "product"
            },
            "arts": {
                "art", "design", "music", "film", "photography", "creative",
                "artist", "visual", "drawing", "painting", "sculpture", "digital",
                "fashion", "architecture", "craft", "illustration"
            },
            "education": {
                "education", "learning", "teaching", "student", "school",
                "university", "academic", "course", "study", "knowledge",
                "skill", "training", "curriculum", "pedagogy", "e-learning"
            },
            "lifestyle": {
                "lifestyle", "travel", "food", "cooking", "recipe", "home",
                "decoration", "fashion", "beauty", "hobby", "entertainment",
                "relationship", "self-improvement", "mindfulness"
            },
            "environment": {
                "environment", "climate", "sustainability", "green", "eco",
                "renewable", "conservation", "nature", "wildlife", "pollution",
                "recycling", "biodiversity", "energy", "earth"
            }
        }
        
        domain_scores = {
            domain: len(words.intersection(keywords))
            for domain, keywords in domain_keywords.items()
        }
        primary_domain = max(domain_scores.items(), key=lambda x: x[1])[0]
        
        content_types = {
            "tutorial": {
                "how", "guide", "tutorial", "learn", "step", "begin", "start",
                "introduction", "basics", "fundamental", "essential"
            },
            "comparison": {
                "vs", "versus", "compare", "difference", "better", "alternative",
                "pros", "cons", "advantages", "disadvantages"
            },
            "analysis": {
                "analysis", "review", "overview", "examination", "study",
                "investigation", "research", "insight", "perspective"
            },
            "news": {
                "news", "update", "latest", "announcement", "release",
                "breakthrough", "development", "trend"
            },
            "opinion": {
                "why", "opinion", "perspective", "think", "believe",
                "should", "could", "would", "debate"
            }
        }
        
        content_type_matches = {
            ctype: bool(words.intersection(keywords))
            for ctype, keywords in content_types.items()
        }
        
        needs_visuals = primary_domain in {"science", "technology", "medical", "fitness", "arts"}
        needs_data = primary_domain in {"finance", "science", "medical", "technology"}
        needs_examples = primary_domain in {"technology", "fitness", "education", "business"}
        needs_citations = primary_domain in {"medical", "science", "finance", "education"}
        
        return {
            "primary_domain": primary_domain,
            "content_types": content_type_matches,
            "needs_code": primary_domain == "technology",
            "needs_table": any(content_type_matches.values()) or primary_domain in {"finance", "science"},
            "needs_quote": True,
            "needs_visuals": needs_visuals,
            "needs_data": needs_data,
            "needs_examples": needs_examples,
            "needs_citations": needs_citations,
            "is_technical": primary_domain in {"technology", "science", "medical"},
            "is_educational": primary_domain in {"education", "science", "medical", "technology"},
            "is_practical": primary_domain in {"fitness", "lifestyle", "business"},
            "reading_level": "advanced" if primary_domain in {"medical", "science", "technology"} else "intermediate"
        }
    
    async def generate_blog(self, topic: str) -> str:
        """Generate a detailed blog post."""
        self.topic = topic
        analysis = self.analyze_topic(topic)
        
        topic_info = await self.get_topic_info(topic)
        self.outline = generate_outline(topic)
        blog_content = []
        
        # Title
        blog_content.append(f"# {topic_info['title'] or topic}\n\n")
        
        # Add horizontal rule after title
        blog_content.append("---\n\n")
        
        # Introduction
        if topic_info["extract"]:
            blog_content.append(topic_info["extract"])
            blog_content.append("\n\n---\n\n")
        
        # Table of Contents
        blog_content.append("## 📌 Why This Matters?\n\n")
        
        # Benefits table
        benefits = [
            ["Benefit", "Description"],
            ["🔁 Reusability", "Write once, use everywhere pattern"],
            ["🧹 Clean Code", "Better organization and maintainability"],
            ["🧪 Testability", "Easier to test and validate"],
            ["🗂️ Structure", "Clear and consistent architecture"]
        ]
        blog_content.append(format_table(benefits[0], benefits[1:]))
        blog_content.append("\n\n---\n\n")
        
        # Main content sections
        for section in self.outline[1:]:
            blog_content.append(f"## {style_with_emojis(section)}\n\n")
            
            content = write_section(section, self.topic, self.domain)
            blog_content.append(content)
            blog_content.append("\n\n")
            
            # Add code examples for implementation sections
            if section == "Implementation Details" and analysis["needs_code"]:
                blog_content.append("### 🔸 Code Example\n\n")
                code_examples = self.generate_code_examples()
                for title, code in code_examples.items():
                    blog_content.append(f"#### {title}\n\n")
                    blog_content.append(format_code_block(code))
                    blog_content.append("\n\n")
            
            # Add comparison tables where relevant
            if section == "Detailed Comparison" and analysis["needs_table"]:
                blog_content.append("### 🔍 Feature Comparison\n\n")
                table = self.generate_comparison_table()
                blog_content.append(table)
                blog_content.append("\n\n")
                
                pros_cons = self.generate_pros_cons()
                blog_content.append("### ✅ Pros and Cons\n\n")
                blog_content.append(pros_cons)
                blog_content.append("\n\n")
            
            # Add summary for conclusion
            if section == "Conclusion":
                blog_content.append("### 🎯 Key Takeaways\n\n")
                takeaways = self.generate_key_takeaways()
                blog_content.append(takeaways)
                blog_content.append("\n\n")
                
                quote = self.generate_quote()
                blog_content.append("### 💭 Final Thoughts\n\n")
                blog_content.append(format_quote(quote))
                blog_content.append("\n\n")
            
            blog_content.append("---\n\n")
        
        return "".join(blog_content)
    
    def generate_code_examples(self) -> Dict[str, str]:
        """Generate multiple relevant code examples."""
        examples = {}
        
        if "api" in self.topic.lower():
            examples["REST API Example"] = """async def fetch_data(endpoint: str, api_key: str) -> Dict[str, Any]:
    \"\"\"Example function demonstrating API usage with proper error handling.\"\"\"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"https://api.example.com/v1/{endpoint}",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            raise Exception("API request timed out")
        except httpx.HTTPError as e:
            raise Exception(f"API request failed: {str(e)}")"""
            
            examples["Error Handling"] = """class APIError(Exception):
    \"\"\"Custom exception for API errors\"\"\"
    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

def handle_api_error(error: APIError) -> Dict[str, str]:
    \"\"\"Handle different types of API errors\"\"\"
    if error.status_code == 404:
        return {"error": "Resource not found"}
    elif error.status_code == 429:
        return {"error": "Rate limit exceeded"}
    return {"error": "An unexpected error occurred"}"""
        
        elif any(kw in self.topic.lower() for kw in ["class", "object", "oop"]):
            examples["Class Definition"] = """from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class User:
    \"\"\"Example user class with type hints and validation\"\"\"
    id: int
    username: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    posts: List[str] = field(default_factory=list)
    
    def add_post(self, content: str) -> None:
        \"\"\"Add a new post for the user\"\"\"
        self.posts.append(content)
        
    @property
    def post_count(self) -> int:
        \"\"\"Get the total number of posts\"\"\"
        return len(self.posts)"""
        
        else:
            examples["Basic Implementation"] = """def process_data(data: Dict[str, Any]) -> Dict[str, Any]:
    \"\"\"Process input data and return results\"\"\"
    results = {
        'processed_at': datetime.now(),
        'status': 'success',
        'data': data
    }
    return results"""
        
        return examples
    
    def generate_comparison_table(self) -> str:
        """Generate a detailed comparison table."""
        if "vs" in self.topic.lower() or "versus" in self.topic.lower():
            parts = self.topic.lower().split(" vs " if " vs " in self.topic.lower() else " versus ")
            headers = ["Feature", parts[0].title(), parts[1].title()]
        else:
            headers = ["Feature", "Traditional Approach", "Modern Approach"]
            
        rows = [
            ["Complexity", "Simple and straightforward", "More complex but powerful"],
            ["Learning Curve", "Gentle learning curve", "Steeper learning curve"],
            ["Performance", "Adequate for basic needs", "Optimized for scale"],
            ["Scalability", "Limited scalability", "Highly scalable"],
            ["Maintenance", "Easy to maintain", "Requires more expertise"],
            ["Community Support", "Established community", "Growing community"],
            ["Integration", "Basic integration options", "Extensive ecosystem"],
            ["Cost", "Lower initial cost", "Higher initial investment"]
        ]
        return format_table(headers, rows)
    
    def generate_pros_cons(self) -> str:
        """Generate detailed pros and cons analysis based on the topic."""
        output = []
        
        if "vs" in self.topic.lower():
            parts = self.topic.lower().split(" vs ")
            
            comparisons = {
                "python": {
                    "pros": [
                        "Simple and readable syntax that enhances developer productivity",
                        "Extensive standard library and rich ecosystem of packages",
                        "Strong support for data science, AI, and machine learning",
                        "Great for rapid prototyping and quick development",
                        "Excellent documentation and community support"
                    ],
                    "cons": [
                        "Generally slower execution compared to compiled languages",
                        "Global Interpreter Lock (GIL) limits true multithreading",
                        "High memory usage for simple programs",
                        "Dynamic typing can lead to runtime errors",
                        "Mobile development is not a strong point"
                    ]
                },
                "javascript": {
                    "pros": [
                        "Runs in every browser and essential for web development",
                        "Full-stack development possible with Node.js",
                        "Rich ecosystem with npm and modern frameworks",
                        "Asynchronous programming with Promises and async/await",
                        "Large and active developer community"
                    ],
                    "cons": [
                        "Loose typing can lead to unexpected behavior",
                        "Browser compatibility issues can be challenging",
                        "Callback hell in asynchronous programming",
                        "Security vulnerabilities if not properly handled",
                        "Framework fatigue and rapid ecosystem changes"
                    ]
                },
                "react": {
                    "pros": [
                        "Virtual DOM for efficient UI updates",
                        "Component-based architecture for reusability",
                        "Large ecosystem and community support",
                        "Strong developer tools and debugging",
                        "Backed by Facebook/Meta"
                    ],
                    "cons": [
                        "Steep learning curve for beginners",
                        "JSX syntax might be confusing initially",
                        "Frequent updates and changes",
                        "Requires additional libraries for complex features",
                        "Build configuration can be complex"
                    ]
                },
                "angular": {
                    "pros": [
                        "Complete framework with built-in features",
                        "TypeScript support for better type safety",
                        "Dependency injection for better testing",
                        "CLI tools for easy project setup",
                        "Enterprise-level support from Google"
                    ],
                    "cons": [
                        "Complex learning curve",
                        "Heavier than other frameworks",
                        "Verbose and ceremonious syntax",
                        "Migration between versions can be difficult",
                        "Overkill for simple applications"
                    ]
                },
                "sql": {
                    "pros": [
                        "ACID compliance for data integrity",
                        "Structured and standardized query language",
                        "Powerful join operations and relationships",
                        "Mature and well-understood technology",
                        "Strong data consistency guarantees"
                    ],
                    "cons": [
                        "Scaling horizontally can be challenging",
                        "Schema changes can be difficult",
                        "Limited flexibility with unstructured data",
                        "Can be expensive for large datasets",
                        "Complex queries can impact performance"
                    ]
                },
                "nosql": {
                    "pros": [
                        "Flexible schema for evolving data structures",
                        "Horizontal scaling capabilities",
                        "Better performance for specific use cases",
                        "Handles unstructured data well",
                        "Suitable for rapid development"
                    ],
                    "cons": [
                        "Limited transaction support",
                        "Eventual consistency model",
                        "Less standardization across databases",
                        "Complex querying compared to SQL",
                        "Learning curve for SQL developers"
                    ]
                }
            }
            
            for part in parts:
                part = part.strip()
                output.append(f"#### {part.title()}")
                output.append("**Pros:**")
                
                if part in comparisons:
                    for pro in comparisons[part]["pros"]:
                        output.append(f"- {pro}")
                    output.append("\n**Cons:**")
                    for con in comparisons[part]["cons"]:
                        output.append(f"- {con}")
                else:
                    pros = [
                        f"Strong {part} community and ecosystem",
                        f"Well-documented {part} features and APIs",
                        f"Regular updates and improvements to {part}",
                        f"Good integration capabilities with other tools",
                        f"Proven track record in production environments"
                    ]
                    cons = [
                        f"Learning curve for new {part} developers",
                        f"Some limitations in specific use cases",
                        f"Resource requirements for larger {part} projects",
                        f"Maintenance and update considerations",
                        f"Integration challenges in legacy systems"
                    ]
                    
                    for pro in pros:
                        output.append(f"- {pro}")
                    output.append("\n**Cons:**")
                    for con in cons:
                        output.append(f"- {con}")
                
                output.append("\n")
        else:
            topic_words = set(self.topic.lower().split())
            
            if any(word in topic_words for word in {"cloud", "aws", "azure", "devops"}):
                output.append("**Advantages:**")
                output.append("- Improved scalability and flexibility")
                output.append("- Reduced infrastructure maintenance")
                output.append("- Pay-as-you-go cost model")
                output.append("- Automatic updates and security patches")
                output.append("- Global deployment capabilities")
                output.append("\n**Challenges:**")
                output.append("- Cost management and optimization")
                output.append("- Security and compliance considerations")
                output.append("- Vendor lock-in concerns")
                output.append("- Network dependency and latency")
                output.append("- Complex service integration")
            
            elif any(word in topic_words for word in {"ai", "ml", "machine learning", "artificial"}):
                output.append("**Advantages:**")
                output.append("- Automation of complex tasks")
                output.append("- Pattern recognition and insights")
                output.append("- Continuous improvement through learning")
                output.append("- Handling large-scale data analysis")
                output.append("- 24/7 operation capability")
                output.append("\n**Challenges:**")
                output.append("- Data quality and quantity requirements")
                output.append("- High computational resources needed")
                output.append("- Ethical considerations and bias")
                output.append("- Model interpretability issues")
                output.append("- Integration with existing systems")
            
            else:
                output.append("**Advantages:**")
                output.append(f"- Enhanced efficiency in {self.topic} implementation")
                output.append("- Improved resource utilization")
                output.append("- Better user experience and satisfaction")
                output.append("- Increased productivity and automation")
                output.append("- Future-proof technology adoption")
                output.append("\n**Challenges:**")
                output.append("- Initial implementation complexity")
                output.append("- Resource and training requirements")
                output.append("- Integration with existing systems")
                output.append("- Ongoing maintenance needs")
                output.append("- Change management considerations")
        
        return "\n".join(output)
    
    def generate_key_takeaways(self) -> str:
        """Generate key takeaways for the conclusion."""
        takeaways = [
            f"Understanding {self.topic} is crucial in today's technological landscape",
            "Proper implementation requires careful planning and consideration",
            "Regular updates and maintenance are essential for long-term success",
            "Community support and documentation play vital roles",
            "Continuous learning and adaptation are key to staying current"
        ]
        
        return "\n".join([f"- {point}" for point in takeaways])
    
    def generate_quote(self) -> str:
        """Generate a relevant quote based on the topic."""
        tech_quotes = [
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "The best way to predict the future is to create it. - Peter Drucker",
            "Technology is best when it brings people together. - Matt Mullenweg",
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Every once in a while, a new technology, an old problem, and a big idea turn into an innovation. - Dean Kamen",
            "The advance of technology is based on making it fit in so that you don't really even notice it. - Bill Gates",
            "Any sufficiently advanced technology is indistinguishable from magic. - Arthur C. Clarke",
            "Technology is nothing. What's important is that you have a faith in people. - Steve Jobs"
        ]
        return random.choice(tech_quotes)
