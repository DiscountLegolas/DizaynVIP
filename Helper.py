from typing import Dict, List, Tuple
import re
KEYWORDS = {
        "fruits_vegetables": {
            "primary": [
                "fruits",
                "vegetables",
                "fruit",
                "vegetable",
                "produce",
                "fresh produce",
                "green leafy vegetables",
                "leafy greens",
                "berries",
                "citrus",
                "salad",
                "raw vegetables",
                "seasonal fruit",
                "whole fruit"
            ],
            "related": [
                "vitamins",
                "fiber",
                "antioxidants",
                "fresh",
                "organic",
                "variety",
                "daily intake",
                "servings",
                "nutritional benefits",
                "5 a day",
                "plant based",
                "plant-based",
                "colorful plate",
                "phytochemicals",
                "micronutrients",
                "immune support"
            ],
            "weight": 20  # Each keyword category has equal weight (20 points)
        },
        "hydration": {
            "primary": [
                "water",
                "hydration",
                "hydrated",
                "drinking",
                "fluids",
                "drink water",
                "water intake",
                "glass of water",
                "bottle of water",
                "plain water"
            ],
            "related": [
                "dehydration",
                "thirst",
                "daily intake",
                "glasses",
                "liters",
                "importance",
                "throughout the day",
                "sip water",
                "staying hydrated",
                "electrolytes",
                "sports drink",
                "herbal tea",
                "sugar free drinks",
                "low sugar drinks"
            ],
            "weight": 20
        },
        "balanced_meals": {
            "primary": [
                "balanced",
                "meals",
                "proteins",
                "protein",
                "carbs",
                "carbohydrates",
                "fats",
                "healthy eating",
                "healthy fats",
                "proportions",
                "macronutrients",
                "balanced plate",
                "balanced diet",
                "healthy plate",
                "portion",
                "portion control"
            ],
            "related": [
                "nutrition",
                "nutrients",
                "combining",
                "proper",
                "balanced diet",
                "meal composition",
                "food groups",
                "whole grains",
                "lean protein",
                "complex carbs",
                "healthy choices",
                "nutrient dense",
                "nutrient-dense",
                "moderation"
            ],
            "weight": 20
        },
        "processed_foods": {
            "primary": [
                "processed",
                "foods",
                "processed food",
                "junk food",
                "fast food",
                "packaged food",
                "snack foods",
                "ready meals",
                "additives",
                "preservatives"
            ],
            "related": [
                "sugar",
                "salt",
                "sodium",
                "unhealthy fats",
                "trans fats",
                "saturated fats",
                "awareness",
                "avoid",
                "limit",
                "highly processed",
                "ultra processed",
                "artificial",
                "refined sugar",
                "refined flour",
                "fried foods",
                "deep fried"
            ],
            "weight": 20
        },
        "meal_timing": {
            "primary": [
                "meal timing",
                "eating patterns",
                "regular meals",
                "breakfast",
                "lunch",
                "dinner",
                "snacks",
                "snacking",
                "regular schedule",
                "eating schedule"
            ],
            "related": [
                "schedule",
                "gaps",
                "skipping meals",
                "skip breakfast",
                "late night eating",
                "late-night eating",
                "intermittent",
                "intermittent fasting",
                "routine",
                "consistent",
                "time of day",
                "night snacking",
                "meal frequency",
                "eating window"
            ],
            "weight": 20
        }
    }
def detect_keywords(text: str) -> Dict[str, Dict]:
        """
        Detect keywords in the user's text and analyze their context.
        
        Args:
            text: User's input text
            
        Returns:
            Dictionary with keyword detection results for each category
        """
        text_lower = text.lower()
        results = {}
        
        for category, keyword_data in KEYWORDS.items():
            primary_matches = []
            related_matches = []
            
            # Check primary keywords
            for keyword in keyword_data["primary"]:
                if keyword.lower() in text_lower:
                    primary_matches.append(keyword)
            
            # Check related keywords
            for keyword in keyword_data["related"]:
                if keyword.lower() in text_lower:
                    related_matches.append(keyword)
            
            # Calculate relevance score (0-1) based on matches
            relevance = 0.0
            if primary_matches:
                relevance = 0.8 + (len(primary_matches) * 0.1)
            elif related_matches:
                relevance = 0.5 + (len(related_matches) * 0.05)
            
            relevance = min(relevance, 1.0)  # Cap at 1.0
            
            results[category] = {
                "primary_matches": primary_matches,
                "related_matches": related_matches,
                "relevance": relevance,
                "mentioned": len(primary_matches) > 0 or len(related_matches) > 0
            }
        
        return results
    
def evaluate_response( user_text: str, keyword_results: Dict) -> Tuple[int, Dict]:
    """
    Evaluate user response and assign a score based on keyword occurrence and context.
    
    Args:
        user_text: User's response text
        keyword_results: Results from keyword detection
        
    Returns:
        Tuple of (total_score, detailed_breakdown)
    """
    total_score = 0
    breakdown = {}
    
    for category, keyword_data in KEYWORDS.items():
        category_result = keyword_results[category]
        category_score = 0
        
        if category_result["mentioned"]:
            # Base score for mentioning the topic
            base_score = keyword_data["weight"] * 0.5  # 50% for mentioning
            
            # Bonus for primary keywords
            if category_result["primary_matches"]:
                base_score = keyword_data["weight"] * 0.7  # 70% for primary keywords
            
            # Apply relevance multiplier
            category_score = base_score * category_result["relevance"]
            
            # Bonus for context quality (check if user provides meaningful context)
            context_quality = _assess_context_quality(user_text, category)
            category_score += (keyword_data["weight"] * 0.3 * context_quality)
        
        category_score = min(category_score, keyword_data["weight"])  # Cap at max weight
        total_score += category_score
        
        breakdown[category] = {
            "score": round(category_score, 2),
            "max_score": keyword_data["weight"],
            "mentioned": category_result["mentioned"],
            "matches": {
                "primary": category_result["primary_matches"],
                "related": category_result["related_matches"]
            }
        }
    
    total_score = min(total_score, 100)  # Cap at 100
    return round(total_score, 2), breakdown

def _assess_context_quality( text: str, category: str) -> float:
    """
    Assess the quality of context provided for a category.
    Looks for indicators of meaningful discussion beyond just keyword mention.
    
    Args:
        text: User's response text
        category: The keyword category being assessed
        
    Returns:
        Context quality score (0-1)
    """
    text_lower = text.lower()
    quality_indicators = [
        "because", "since", "for example", "such as", "like", 
        "important", "benefits", "helps", "should", "need",
        "avoid", "limit", "include", "eat", "drink"
    ]
    
    # Count quality indicators
    indicator_count = sum(1 for indicator in quality_indicators if indicator in text_lower)
    
    # Check for sentence length (longer responses often have more context)
    sentences = re.split(r'[.!?]+', text)
    avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
    
    # Calculate quality score
    quality = min(0.3 + (indicator_count * 0.1) + (min(avg_sentence_length / 20, 0.3)), 1.0)
    return quality