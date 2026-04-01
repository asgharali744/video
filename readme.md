 🎬 Viral Video Creator - Convert Long Videos to Short Clips

Convert long-form videos into engaging short viral clips with **auto-generated captions**, **scene detection**, and **TikTok-style formatting**.

## Features

✨ **Key Capabilities:**
- 🎥 Convert long videos to short viral clips (TikTok, Instagram Reels, YouTube Shorts)
- 🤖 Auto-generate captions using OpenAI Whisper AI
- 🎬 Scene detection and motion analysis
- 📊 Intelligent clip extraction based on interesting moments
- 📱 Auto-resize to vertical format (9:16)
- 🎨 TikTok-style caption styling
- 💾 Multiple format support (MP4, AVI, MOV, MKV, etc.)
- ⚡ Web-based user interface
- 🔄 Batch processing support

## Technology Stack

- **Backend:** Flask, Python 3.8+
- **Video Processing:** FFmpeg, OpenCV
- **Caption Generation:** OpenAI Whisper
- **Scene Detection:** scenedetect, optical flow analysis
- **Frontend:** HTML5, Bootstrap 5, JavaScript
- **Database:** SQLite (for future project management)

## Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg (for video processing)
- Conda or venv for virtual environment

### Step 1: Clone and Setup

```bash
# Clone repository
git clone <repository-url>
cd viral-video-creator

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install FFmpeg

**Windows (using Chocolatey):**
```bash
choco install ffmpeg
```

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Note: The first time Whisper is used, it will download the model (~1.4GB for base model).

### Step 4: Run the Application

```bash
cd src
python app.py
```

The application will start at `http://localhost:5000`

## Usage

### Web Interface

1. **Upload Video:**
   - Click "Select Video File" to choose your video
   - Supported formats: MP4, AVI, MOV, MKV, FLV, WMV, WebM
   - Click "Upload Video" to process

2. **Configure Settings:**
   - Choose a preset (TikTok, Instagram Reels, YouTube Shorts) or customize:
     - **Clip Duration:** 5-120 seconds
     - **Number of Clips:** 1-20 clips
     - **Add Captions:** Enable Whisper AI transcription
     - **Resize Vertical:** Convert to 9:16 format

3. **Process:**
   - Click "🚀 Process Video"
   - Monitor progress in real-time
   - Download generated clips when complete

### Programmatic Usage

```python
from src.video_cutter import VideoCutter

# Initialize cutter
cutter = VideoCutter("input_video.mp4", output_dir="./outputs")

# Process complete pipeline
result = cutter.process_complete_pipeline(
    clip_duration=30,
    num_clips=5,
    add_captions=True,
    resize_vertical=True
)

# Access results
clips = result['final_clips']
print(f"Generated {len(clips)} clips")
```

### Using Individual Modules

**Video Processing:**
```python
from src.video_processor import VideoProcessor

processor = VideoProcessor("input.mp4")
info = processor.get_video_info()
processor.cut_video_clip(10, 40, "output_clip.mp4")
```

**Caption Generation:**
```python
from src.caption_generator import CaptionGenerator

gen = CaptionGenerator(model_name="base")
result = gen.transcribe_video("video.mp4")
captions = gen.generate_captions_from_segments(result['segments'])
```

**Scene Detection:**
```python
from src.scene_detector import SceneDetector

detector = SceneDetector("video.mp4", threshold=27.0)
scenes = detector.detect_scene_changes()
motion_areas = detector.detect_motion_areas()
faces = detector.detect_faces()
```

## Project Structure

```
viral-video-creator/
├── src/
│   ├── app.py                 # Flask web application
│   ├── config.py              # Configuration settings
│   ├── video_processor.py      # Video processing utilities
│   ├── caption_generator.py    # Whisper caption generation
│   ├── scene_detector.py       # Scene and motion detection
│   ├── video_cutter.py         # Main clip extraction pipeline
│   └── __init__.py
├── templates/
│   └── index.html             # Web UI template
├── static/
│   ├── style.css              # Web UI styling
│   └── script.js              # Web UI interactions
├── uploads/                   # User uploaded videos
├── outputs/                   # Generated clips
├── tests/                     # Unit tests
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── .github/
    └── copilot-instructions.md
```

## Configuration

Edit `src/config.py` to customize:

```python
# Video processing defaults
MIN_CLIP_DURATION = 5           # seconds
MAX_CLIP_DURATION = 60          # seconds
DEFAULT_CLIP_DURATION = 30      # seconds

# Whisper configuration
WHISPER_MODEL = "base"          # tiny, base, small, medium, large
LANGUAGE = "en"                 # Language code

# Scene detection
SCENE_THRESHOLD = 27.0          # Sensitivity for scene changes

# File limits
MAX_CONTENT_LENGTH = 5GB        # Max upload size
```

## API Endpoints

### Upload Video
**POST** `/api/upload`
```bash
curl -F "file=@video.mp4" http://localhost:5000/api/upload
```

### Process Video
**POST** `/api/process/<file_id>`
```json
{
    "clip_duration": 30,
    "num_clips": 5,
    "add_captions": true,
    "resize_vertical": true
}
```

### Get Video Info
**GET** `/api/video-info/<file_id>`

### Get Presets
**GET** `/api/presets`

## Performance Tips

1. **Faster Processing:**
   - Use smaller Whisper model ("tiny" or "base")
   - Reduce number of clips
   - Skip caption generation if not needed

2. **Better Results:**
   - Use larger Whisper model ("small" or "medium")
   - Increase scene detection threshold for slower videos
   - Process videos with clear scene changes

3. **System Requirements:**
   - **Minimum:** 4GB RAM, 2GB free disk space
   - **Recommended:** 8GB+ RAM, 10GB+ free disk space
   - GPU acceleration: NVIDIA GPU with CUDA for faster processing

## Troubleshooting

### FFmpeg not found
- Ensure FFmpeg is installed and in PATH
- Test: `ffmpeg -version`

### Whisper model download fails
- Check internet connection
- Models are cached in `~/.cache/whisper/`
- Use smaller model: `WHISPER_MODEL = "tiny"`

### Out of memory errors
- Reduce number of clips or clip duration
- Use Python 3.10+ for better memory management
- Process smaller videos first

### Slow processing
- GPU is not being used (install CUDA/cuDNN)
- Consider splitting large videos into segments

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is licensed under the MIT License.

## Roadmap

- [ ] GPU acceleration support (CUDA/ROCm)
- [ ] Advanced editing options (transitions, effects, filters)
- [ ] Multi-language support for captions
- [ ] Video analytics and engagement metrics
- [ ] Cloud storage integration
- [ ] Batch processing API
- [ ] Mobile app (React Native)
- [ ] Real-time preview

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

## Acknowledgments

- OpenAI Whisper for caption generation
- FFmpeg for video processing
- OpenCV for computer vision
- Bootstrap for web UI

---

**Happy Video Editing! 🎬✨**
