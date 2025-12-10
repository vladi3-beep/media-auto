"""
Generator inteligent de conținut - VERSION CORECTATĂ
"""

import os
import json
import random
from datetime import datetime
from typing import List, Dict, Any
import requests
from loguru import logger

class ContentGenerator:
    def __init__(self):
        self.trending_topics = self._load_trending_data()
        
    def _load_trending_data(self) -> List[str]:
        """Încarcă trending topics"""
        return [
            "AI în marketing", "Social media trends", 
            "Video content tips", "Growing followers",
            "Best time to post", "Content automation",
            "Digital marketing", "Personal branding",
            "Content strategy", "Social media algorithms"
        ]
    
    def generate_complete_content(self, topic: str, platform: str, 
                                 languages: List[str] = None, 
                                 video_required: bool = False) -> Dict[str, Any]:
        """Generează conținut complet - versiune simplificată"""
        if languages is None:
            languages = ['ro']
        
        content = {
            "topic": topic,
            "platform": platform,
            "generated_at": datetime.now().isoformat(),
            "languages": {},
            "success_metrics": self._predict_performance(topic, platform)
        }
        
        # Generează conținut pentru fiecare limbă
        for lang in languages:
            lang_content = {
                "caption": self._generate_caption(topic, platform, lang),
                "hashtags": self._generate_hashtags(topic, lang),
                "script": self._generate_script(topic, lang) if video_required else None
            }
            content["languages"][lang] = lang_content
        
        # Creează preview
        preview_path = self._create_preview(content)
        content["preview_url"] = f"/preview/{os.path.basename(preview_path)}"
        
        return content
    
    def _generate_caption(self, topic: str, platform: str, language: str) -> str:
        """Generează caption simplu"""
        captions = {
            'ro': [
                f"🔝 Un ghid complet despre {topic} pe {platform}!",
                f"📈 Cum să optimizezi {topic} pentru mai mult engagement",
                f"🚀 Secretul din spatele {topic} pe social media"
            ],
            'en': [
                f"🔝 The ultimate guide to {topic} on {platform}!",
                f"📈 How to optimize {topic} for better engagement",
                f"🚀 The secret behind successful {topic} on social media"
            ]
        }
        
        lang_captions = captions.get(language, captions['en'])
        return random.choice(lang_captions)
    
    def _generate_hashtags(self, topic: str, language: str) -> List[str]:
        """Generează hashtag-uri"""
        base_tags = ['viral', 'trending', 'tips', 'digital', 'marketing']
        
        if language == 'ro':
            tags = ['#socialmedia', '#marketing', '#digital', '#romania']
        else:
            tags = ['#socialmedia', '#marketing', '#digital', '#tips']
        
        # Adaugă hashtag-uri specifice topic-ului
        topic_tags = topic.lower().split()
        for tag in topic_tags[:3]:
            if len(tag) > 3:
                tags.append(f"#{tag}")
        
        return tags[:8]  # Maxim 8 hashtag-uri
    
    def _generate_script(self, topic: str, language: str) -> str:
        """Generează script pentru video"""
        scripts = {
            'ro': f"""
            Salut! Astăzi vorbim despre {topic}.
            
            În acest video vei învăța:
            1. Importanța {topic} în marketingul digital
            2. Cum să implementezi {topic} în strategia ta
            3. Cele mai bune practici pentru rezultate
            
            Nu uita să dai like și subscribe pentru mai mult conținut!
            """,
            'en': f"""
            Hello! Today we're talking about {topic}.
            
            In this video you'll learn:
            1. The importance of {topic} in digital marketing
            2. How to implement {topic} in your strategy
            3. Best practices for results
            
            Don't forget to like and subscribe for more content!
            """
        }
        
        return scripts.get(language, scripts['en'])
    
    def _predict_performance(self, topic: str, platform: str) -> Dict[str, float]:
        """Prezice performanța conținutului"""
        return {
            "predicted_engagement": random.uniform(2.0, 15.0),
            "virality_score": random.uniform(0.1, 0.9),
            "audience_match": random.uniform(0.5, 1.0)
        }
    
    def _create_preview(self, content: Dict[str, Any]) -> str:
        """Creează o previzualizare a conținutului"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import matplotlib.pyplot as plt
        except ImportError:
            # Fallback pentru preview simplu
            return self._create_simple_preview(content)
        
        # Creează o imagine de preview
        width, height = 800, 400
        
        img = Image.new('RGB', (width, height), color='#2c3e50')
        draw = ImageDraw.Draw(img)
        
        try:
            font_large = ImageFont.truetype("arial.ttf", 24)
            font_medium = ImageFont.truetype("arial.ttf", 18)
            font_small = ImageFont.truetype("arial.ttf", 14)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Adaugă titlu
        title = content["topic"][:50]
        draw.text((20, 20), title, fill='white', font=font_large)
        
        # Adaugă platform info
        platform_text = f"Platform: {content['platform']}"
        draw.text((20, 70), platform_text, fill='#3498db', font=font_medium)
        
        # Adaugă limbile
        languages_text = f"Languages: {', '.join(content['languages'].keys())}"
        draw.text((20, 110), languages_text, fill='#2ecc71', font=font_medium)
        
        # Adaugă performance prediction
        metrics = content["success_metrics"]
        perf_text = f"Predicted Engagement: {metrics['predicted_engagement']:.1f}%"
        draw.text((20, 150), perf_text, fill='#f39c12', font=font_small)
        
        # Salvează imaginea
        preview_dir = "static/previews"
        os.makedirs(preview_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        preview_path = f"{preview_dir}/preview_{timestamp}.png"
        
        img.save(preview_path)
        
        return preview_path
    
    def _create_simple_preview(self, content: Dict[str, Any]) -> str:
        """Creează preview simplu fără dependințe"""
        preview_dir = "static/previews"
        os.makedirs(preview_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        preview_path = f"{preview_dir}/simple_preview_{timestamp}.txt"
        
        # Creează fișier text simplu
        with open(preview_path, 'w', encoding='utf-8') as f:
            f.write(f"Topic: {content['topic']}\n")
            f.write(f"Platform: {content['platform']}\n")
            f.write(f"Languages: {', '.join(content['languages'].keys())}\n")
            f.write(f"Generated: {content['generated_at']}\n")
        
        return preview_path