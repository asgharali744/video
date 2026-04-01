import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from .video_processor import VideoProcessor
from .scene_detector import SceneDetector
from .caption_generator import CaptionGenerator

logger = logging.getLogger(__name__)


class VideoCutter:
    """Extracts and creates viral clips from long videos"""
    
    def __init__(self, video_path: str, output_dir: str = "."):
        """
        Initialize video cutter
        
        Args:
            video_path: Path to input video
            output_dir: Directory for output clips
        """
        self.video_path = Path(video_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.processor = VideoProcessor(str(self.video_path))
        self.detector = SceneDetector(str(self.video_path))
        self.caption_gen = CaptionGenerator()
    
    def find_best_clips(self, clip_duration: float = 30, num_clips: int = 5) -> List[Dict]:
        """
        Find best clips from video based on motion and scene changes
        
        Args:
            clip_duration: Duration of each clip in seconds
            num_clips: Number of clips to extract
        
        Returns:
            List of clip information dictionaries
        """
        logger.info(f"Finding best {num_clips} clips of {clip_duration}s each")
        
        # Detect motion areas
        motion_intervals = self.detector.detect_motion_areas()
        
        # Detect scenes
        scenes = self.detector.detect_scene_changes()
        
        # Combine motion and scene data to find interesting moments
        candidates = []
        
        for motion_start, motion_end in motion_intervals:
            motion_duration = motion_end - motion_start
            
            # Create clips from motion intervals
            if motion_duration > clip_duration:
                # Multiple clips possible
                num_clips_in_interval = int(motion_duration / clip_duration)
                for i in range(num_clips_in_interval):
                    clip_start = motion_start + (i * clip_duration)
                    clip_end = min(clip_start + clip_duration, motion_end)
                    
                    # Check for scene changes
                    scene_count = sum(1 for s, e in scenes 
                                    if s <= clip_end and e >= clip_start)
                    
                    candidates.append({
                        "start": clip_start,
                        "end": clip_end,
                        "duration": clip_end - clip_start,
                        "score": motion_duration + scene_count * 5
                    })
            else:
                candidates.append({
                    "start": motion_start,
                    "end": motion_end,
                    "duration": motion_end - motion_start,
                    "score": motion_duration
                })
        
        # Sort by score and select top clips
        candidates.sort(key=lambda x: x["score"], reverse=True)
        best_clips = candidates[:num_clips]
        
        logger.info(f"Found {len(best_clips)} best clips")
        return best_clips
    
    def extract_clips(self, clips: List[Dict], output_prefix: str = "clip") -> List[str]:
        """
        Extract video clips
        
        Args:
            clips: List of clip dictionaries with start/end times
            output_prefix: Prefix for output filenames
        
        Returns:
            List of output file paths
        """
        output_files = []
        
        for i, clip in enumerate(clips):
            output_filename = self.output_dir / f"{output_prefix}_{i+1:02d}.mp4"
            
            success = self.processor.cut_video_clip(
                clip["start"],
                clip["end"],
                str(output_filename)
            )
            
            if success:
                output_files.append(str(output_filename))
                logger.info(f"Clip {i+1} extracted: {output_filename}")
            else:
                logger.error(f"Failed to extract clip {i+1}")
        
        return output_files
    
    def add_captions_to_clips(self, clip_files: List[str]) -> Dict[str, str]:
        """
        Add captions to extracted clips
        
        Args:
            clip_files: List of clip file paths
        
        Returns:
            Dictionary mapping original clip path to captioned clip path
        """
        captioned_clips = {}
        
        for i, clip_file in enumerate(clip_files):
            try:
                # Transcribe clip
                result = self.caption_gen.transcribe_video(clip_file)
                if not result:
                    logger.warning(f"Failed to transcribe clip {i+1}")
                    continue
                
                # Generate captions
                captions = self.caption_gen.generate_captions_from_segments(
                    result.get("segments", [])
                )
                
                # Create output filename
                output_filename = str(clip_file).replace(".mp4", "_captioned.mp4")
                
                # Add captions to video
                success = self.processor.add_captions_to_video(
                    clip_file,
                    captions,
                    output_filename
                )
                
                if success:
                    captioned_clips[clip_file] = output_filename
                    logger.info(f"Captions added to clip {i+1}")
                
            except Exception as e:
                logger.error(f"Error processing clip {i+1}: {e}")
        
        return captioned_clips
    
    def resize_clips_for_vertical(self, clip_files: List[str], 
                                  width: int = 1080, height: int = 1920) -> List[str]:
        """
        Resize clips to vertical format (TikTok/Instagram Reels)
        
        Args:
            clip_files: List of clip file paths
            width: Target width
            height: Target height
        
        Returns:
            List of resized clip paths
        """
        resized_clips = []
        
        for i, clip_file in enumerate(clip_files):
            try:
                output_filename = str(clip_file).replace(".mp4", "_vertical.mp4")
                
                success = self.processor.resize_video(
                    output_filename,
                    width=width,
                    height=height
                )
                
                if success:
                    resized_clips.append(output_filename)
                    logger.info(f"Clip {i+1} resized to vertical format")
                
            except Exception as e:
                logger.error(f"Error resizing clip {i+1}: {e}")
        
        return resized_clips
    
    def process_complete_pipeline(self, clip_duration: float = 30, 
                                  num_clips: int = 5,
                                  add_captions: bool = True,
                                  resize_vertical: bool = True) -> Dict:
        """
        Complete pipeline: find clips -> extract -> caption -> resize
        
        Args:
            clip_duration: Duration of each clip
            num_clips: Number of clips to extract
            add_captions: Whether to add captions
            resize_vertical: Whether to resize for vertical format
        
        Returns:
            Dictionary with processing results
        """
        logger.info("Starting complete video processing pipeline")
        
        # Step 1: Find best clips
        best_clips = self.find_best_clips(clip_duration, num_clips)
        logger.info(f"Step 1 complete: Found {len(best_clips)} best clips")
        
        # Step 2: Extract clips
        extracted_files = self.extract_clips(best_clips)
        logger.info(f"Step 2 complete: Extracted {len(extracted_files)} clips")
        
        # Step 3: Add captions
        captioned_files = {}
        if add_captions:
            captioned_files = self.add_captions_to_clips(extracted_files)
            logger.info(f"Step 3 complete: Added captions to {len(captioned_files)} clips")
        
        # Step 4: Resize for vertical format
        final_files = extracted_files
        if resize_vertical and captioned_files:
            final_files = self.resize_clips_for_vertical(list(captioned_files.values()))
            logger.info(f"Step 4 complete: Resized {len(final_files)} clips")
        
        return {
            "best_clips": best_clips,
            "extracted_clips": extracted_files,
            "captioned_clips": captioned_files,
            "final_clips": final_files,
            "status": "completed"
        }
