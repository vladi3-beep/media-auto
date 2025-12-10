"""
Sistem automat de creare video - VERSION CORECTATĂ
"""

import os
import cv2
import numpy as np
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import requests
from loguru import logger

# Try to import moviepy with fallback
try:
    from moviepy.editor import *
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    logger.warning("MoviePy not installed. Video creation will be limited.")

class VideoCreator:
    def __init__(self):
        self.assets_dir = "assets"
        self.output_dir = "uploads/videos"
        self.preview_dir = "static/previews"
        
        # Creează directoarele necesare
        for dir_path in [self.assets_dir, self.output_dir, self.preview_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
    def create_from_content(self, content: dict, 
                           languages: list = None,
                           style: str = "professional") -> str:
        """Creează video din conținutul generat - versiune simplificată"""
        if languages is None:
            languages = ['ro']
        
        # Creează o imagine simplă pentru test
        width, height = 1080, 1920
        
        # Creează imaginea
        img = Image.new('RGB', (width, height), color=(20, 30, 50))
        draw = ImageDraw.Draw(img)
        
        # Adaugă titlu
        title = content.get("topic", "Social Media Content")
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        # Desenează titlu
        text_width = draw.textlength(title, font=font)
        x = (width - text_width) // 2
        y = height // 3
        
        draw.text((x, y), title, fill=(255, 255, 255), font=font)
        
        # Adaugă subtitlu
        subtitle = f"Generated in {', '.join(languages)} languages"
        draw.text((50, y + 100), subtitle, fill=(200, 200, 255), font=font)
        
        # Adaugă timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        draw.text((50, height - 100), f"Generated: {timestamp}", 
                 fill=(150, 150, 150), font=font)
        
        # Salvează imaginea temporar
        temp_image = f"{self.assets_dir}/temp_frame.jpg"
        img.save(temp_image)
        
        if MOVIEPY_AVAILABLE:
            # Creează video simplu din imagine
            clip = ImageClip(temp_image, duration=5)  # 5 secunde
            
            # Adaugă audio dacă este disponibil
            audio_path = self._create_test_audio()
            if audio_path and os.path.exists(audio_path):
                audio_clip = AudioFileClip(audio_path)
                clip = clip.set_audio(audio_clip)
            
            # Salvează video-ul
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_path = f"{self.output_dir}/video_{timestamp}.mp4"
            
            clip.write_videofile(
                video_path,
                fps=24,
                codec='libx264',
                audio_codec='aac' if audio_path else None
            )
            
            # Generează preview
            preview_path = self.generate_preview(video_path)
            
            return video_path
        else:
            # Fallback: salvează doar imaginea
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = f"{self.output_dir}/content_{timestamp}.jpg"
            img.save(image_path)
            
            # Generează preview
            preview_path = self.generate_preview(image_path)
            
            return image_path
    
    def _create_test_audio(self):
        """Creează audio de test (implementare simplă)"""
        # Într-o implementare reală, aici ai genera audio
        # Pentru acum, returnează None
        return None
    
    def generate_preview(self, media_path: str) -> str:
        """Generează o imagine de preview"""
        try:
            if media_path.endswith(('.mp4', '.avi', '.mov')):
                # Extrage un frame din video
                cap = cv2.VideoCapture(media_path)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        preview_path = media_path.replace('.mp4', '_preview.jpg')
                        preview_path = preview_path.replace('uploads/videos', 'static/previews')
                        
                        cv2.imwrite(preview_path, frame)
                        cap.release()
                        
                        # Adaugă watermark
                        self._add_watermark(preview_path)
                        return preview_path
                cap.release()
            
            elif media_path.endswith(('.jpg', '.jpeg', '.png')):
                # Creează copie pentru preview
                preview_path = media_path.replace('uploads/videos', 'static/previews')
                os.makedirs(os.path.dirname(preview_path), exist_ok=True)
                
                # Copiază imaginea
                import shutil
                shutil.copy2(media_path, preview_path)
                
                # Adaugă watermark
                self._add_watermark(preview_path)
                return preview_path
        
        except Exception as e:
            logger.error(f"Error generating preview: {e}")
        
        # Fallback: creează o imagine de preview simplă
        return self._create_fallback_preview()
    
    def _add_watermark(self, image_path: str):
        """Adaugă watermark la imagine"""
        try:
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)
            
            # Adaugă text watermark
            watermark = "AutoGenerated"
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            
            # Calculează poziția
            text_width = draw.textlength(watermark, font=font)
            x = img.width - text_width - 10
            y = img.height - 30
            
            # Desenează text
            draw.text((x, y), watermark, font=font, fill=(255, 255, 255, 128))
            
            img.save(image_path)
        
        except Exception as e:
            logger.error(f"Error adding watermark: {e}")
    
    def _create_fallback_preview(self):
        """Creează o imagine de preview fallback"""
        preview_dir = "static/previews"
        os.makedirs(preview_dir, exist_ok=True)
        
        preview_path = f"{preview_dir}/fallback_preview.jpg"
        
        # Creează o imagine simplă
        img = Image.new('RGB', (300, 200), color=(40, 40, 40))
        draw = ImageDraw.Draw(img)
        
        # Adaugă text
        draw.text((50, 80), "Preview", fill=(255, 255, 255))
        draw.text((40, 120), "Not Available", fill=(200, 200, 200))
        
        img.save(preview_path)
        
        return preview_path