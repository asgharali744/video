// Main JavaScript for Viral Video Creator

let uploadedFileId = null;

// File upload handling
document.getElementById('videoFile').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        console.log('File selected:', file.name);
    }
});

// Upload button
document.getElementById('uploadBtn').addEventListener('click', uploadVideo);

// Process button
document.getElementById('processBtn').addEventListener('click', processVideo);

// Preset selection
document.getElementById('presetSelect').addEventListener('change', loadPreset);

async function uploadVideo() {
    const fileInput = document.getElementById('videoFile');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select a video file');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        // Show progress
        document.getElementById('uploadProgress').style.display = 'block';
        document.getElementById('uploadBtn').disabled = true;

        // Upload file
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Upload failed');
        }

        const videoInfo = await response.json();
        uploadedFileId = videoInfo.file_id;

        // Display video info
        displayVideoInfo(videoInfo);

        // Enable process button
        document.getElementById('processBtn').disabled = false;

        // Hide upload progress
        document.getElementById('uploadProgress').style.display = 'none';
        document.getElementById('uploadBtn').disabled = false;
    } catch (error) {
        console.error('Upload error:', error);
        alert('Error uploading video: ' + error.message);
        document.getElementById('uploadProgress').style.display = 'none';
        document.getElementById('uploadBtn').disabled = false;
    }
}

function displayVideoInfo(videoInfo) {
    const videoInfoDiv = document.getElementById('videoInfo');
    
    // Format duration
    const minutes = Math.floor(videoInfo.duration / 60);
    const seconds = Math.floor(videoInfo.duration % 60);
    const durationStr = `${minutes}m ${seconds}s`;

    // Format file size
    const fileSizeMB = (videoInfo.file_size / (1024 * 1024)).toFixed(2);

    // Display info
    document.getElementById('infoDuration').textContent = durationStr;
    document.getElementById('infoResolution').textContent = `${videoInfo.width}x${videoInfo.height}`;
    document.getElementById('infoSize').textContent = `${fileSizeMB} MB`;

    // Show info section
    videoInfoDiv.classList.remove('d-none');
}

async function loadPreset() {
    const presetSelect = document.getElementById('presetSelect');
    const selectedPreset = presetSelect.value;

    if (selectedPreset === 'custom') {
        return;
    }

    try {
        const response = await fetch('/api/presets');
        const presets = await response.json();
        const preset = presets[selectedPreset];

        if (preset) {
            document.getElementById('clipDuration').value = preset.clip_duration;
            document.getElementById('numClips').value = preset.num_clips;
            document.getElementById('addCaptions').checked = preset.add_captions;
            document.getElementById('resizeVertical').checked = preset.resize_vertical;
        }
    } catch (error) {
        console.error('Error loading preset:', error);
    }
}

async function processVideo() {
    if (!uploadedFileId) {
        alert('Please upload a video first');
        return;
    }

    const processingSettings = {
        clip_duration: parseFloat(document.getElementById('clipDuration').value),
        num_clips: parseInt(document.getElementById('numClips').value),
        add_captions: document.getElementById('addCaptions').checked,
        resize_vertical: document.getElementById('resizeVertical').checked
    };

    try {
        // Show processing section
        document.getElementById('processingSection').style.display = 'block';
        document.getElementById('processBtn').disabled = true;

        // Simulate progress updates
        updateProgress(10, 'Analyzing video content...');
        
        setTimeout(() => updateProgress(30, 'Detecting scenes and motion...'), 1000);
        setTimeout(() => updateProgress(50, 'Extracting best clips...'), 3000);
        setTimeout(() => updateProgress(70, 'Generating captions with Whisper AI...'), 5000);
        setTimeout(() => updateProgress(85, 'Resizing for vertical format...'), 7000);

        // Send processing request
        const response = await fetch(`/api/process/${uploadedFileId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(processingSettings)
        });

        if (!response.ok) {
            throw new Error('Processing failed');
        }

        const result = await response.json();

        updateProgress(100, 'Processing complete!');

        // Display results
        displayResults(result);

        document.getElementById('processBtn').disabled = false;
    } catch (error) {
        console.error('Processing error:', error);
        alert('Error processing video: ' + error.message);
        document.getElementById('processBtn').disabled = false;
    }
}

function updateProgress(percent, message) {
    const progressBar = document.getElementById('processingBar');
    const logText = document.getElementById('logText');

    progressBar.style.width = percent + '%';
    progressBar.textContent = percent + '%';

    // Append log message
    const timestamp = new Date().toLocaleTimeString();
    logText.textContent += `[${timestamp}] ${message}\n`;

    // Auto-scroll to bottom
    const logDiv = document.getElementById('processingLog');
    logDiv.scrollTop = logDiv.scrollHeight;
}

function displayResults(result) {
    const clipsGrid = document.getElementById('clipsGrid');
    const resultsSection = document.getElementById('resultsSection');

    clipsGrid.innerHTML = '';

    result.clips.forEach((clip, index) => {
        const clipCard = document.createElement('div');
        clipCard.className = 'col-md-4 col-lg-3';
        clipCard.innerHTML = `
            <div class="clip-card">
                <video class="clip-preview" controls>
                    <source src="${clip.url}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                <div class="clip-actions">
                    <a href="${clip.url}" download="${clip.filename}">📥 Download</a>
                    <a href="${clip.url}" target="_blank">🎬 Preview</a>
                </div>
            </div>
            <p class="text-center mt-2 text-white"><strong>Clip ${index + 1}</strong></p>
        `;
        clipsGrid.appendChild(clipCard);
    });

    resultsSection.style.display = 'block';
}

// Initialize presets on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded - Viral Video Creator ready');
});
