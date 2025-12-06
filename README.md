# Reinforcement Learning for Neck Deep's December Game

**Goal**: Train an OpenAI Gymnasium reinforcement learning agent to master [Neck Deep's December game](https://december.neckdeepuk.com/) and place in the top 3 to win band merchandise!

## Project Overview

This project aims to create an autonomous agent that can play the December game by:
1. Using computer vision to observe the game state
2. Detecting game objects (player, obstacles, collectibles)
3. Reading game metrics (health, score) via OCR
4. Training an RL agent to make optimal decisions
5. Achieving top 3 placement in the leaderboard

## Demo

Watch the YOLOv8 object detection in action:

[![YOLOv8 Detection Demo](https://img.youtube.com/vi/eKbmbajl2U0/maxresdefault.jpg)](https://youtu.be/eKbmbajl2U0)

## Game Information

- **Game URL**: https://december.neckdeepuk.com/
- **Game State**: Score and Health are displayed on screen
- **Objective**: Maximize score while maintaining health

## What's Been Done

### 1. Environment Setup
- Created Python virtual environment (`.venv`)
- Installed dependencies:
  - `opencv-python` - Video processing and image handling
  - `easyocr` - OCR for reading score and health values
  - `labelImg`, `PyQt5`, `lxml` - YOLO dataset annotation tools
  - Additional dependencies for EasyOCR (torch, torchvision, scipy, etc.)

### 2. Video Frame Extraction
- **Script**: `BuildCustomSet.py`
- Extracted frames from `Gameplay.mp4` every 100 frames
- Saved extracted frames to `frames/` directory
- Frame naming convention: `frame_100.jpg`, `frame_200.jpg`, etc.

### 3. Object Detection Dataset (YOLO)
- **Dataset Location**: `datasets/NeckDeep/`
- **Dataset Configuration**: `datasets/NeckDeep/NeckDeep.yaml`
- **Classes** (7 total):
  0. Player
  1. Cone
  2. Coin
  3. Hole
  4. Plane
  5. Roadblock
  6. Ball

- **Training Set**: 27 frames in `datasets/NeckDeep/images/train/`
- **Validation Set**: 5 frames in `datasets/NeckDeep/images/val/`
- **Labels**: Corresponding YOLO format annotations in `datasets/NeckDeep/labels/`

### 4. Label Management
- **Script**: `remap_labels.py`
- Remaps YOLO label class indices to match the YAML configuration
- Ensures consistency between original annotations and current class order
- Updates `classes.txt` files to match YAML structure

### 5. OCR Setup for Game State Reading

#### Health Detection
- **Script**: `EasyOCR/Health/GetHealth.py`
- **Coordinates**: (115, 150, 400, 175) - stored in `EasyOCR/Health/Coords.txt`
- Uses EasyOCR to read health value from cropped region

#### Score Detection
- **Script**: `EasyOCR/Score/GetScore.py`
- **Coordinates**: (100, 125, 400, 150) - stored in `EasyOCR/Score/Coords.txt`
- Uses EasyOCR to read score value from cropped region

### 6. YOLO Model Training
- ✅ Trained YOLO model on the NeckDeep dataset
- Model weights: `yolov8n.pt` (pre-trained) - fine-tuned on custom dataset
- Model ready for object detection in game frames

## Project Structure

```
ReinforcementLearning/
├── .venv/                          # Virtual environment
├── BuildCustomSet.py               # Frame extraction script
├── remap_labels.py                 # Label remapping utility
├── requirements.txt                # Python dependencies
├── yolo.ps1                        # YOLO command wrapper
├── Gameplay.mp4                    # Source gameplay video
├── yolov8n.pt                      # YOLO model weights
├── frames/                         # Extracted video frames
├── datasets/
│   └── NeckDeep/
│       ├── NeckDeep.yaml           # YOLO dataset config
│       ├── images/
│       │   ├── train/              # Training images
│       │   └── val/                # Validation images
│       └── labels/
│           ├── train/              # Training labels
│           └── val/                # Validation labels
└── EasyOCR/
    ├── Health/
    │   ├── GetHealth.py            # Health OCR script
    │   └── Coords.txt              # Health region coordinates
    └── Score/
        ├── GetScore.py             # Score OCR script
        └── Coords.txt              # Score region coordinates
```

## What Needs to Be Done

### 1. Create Gymnasium Environment
- [ ] Implement custom Gymnasium environment wrapper
- [ ] Connect to game through screen capture
- [ ] Define observation space (game frame + detected objects)
- [ ] Define action space (game controls: movement, jumping, etc.)
- [ ] Implement reward function:
  - Positive reward for collecting coins
  - Positive reward for score increases
  - Negative reward for health loss
  - Bonus reward for high scores
- [ ] Implement `step()`, `reset()`, and `render()` methods

### 2. Game State Integration
- [ ] Integrate OCR modules to read health and score in real-time
- [ ] Integrate YOLO model for object detection
- [ ] Combine visual state + OCR state + detected objects into observation
- [ ] Handle edge cases (OCR failures, detection errors)

### 3. Reinforcement Learning Agent
- [ ] Choose RL algorithm (PPO, DQN, A3C, etc.)
- [ ] Implement or configure RL agent
- [ ] Set up hyperparameter tuning
- [ ] Design neural network architecture for policy/value networks

### 4. Training Pipeline
- [ ] Set up training loop
- [ ] Add logging and monitoring (TensorBoard, Weights & Biases, etc.)
- [ ] Implement checkpointing for model saving
- [ ] Create evaluation scripts

### 5. Testing & Optimization
- [ ] Test trained agent in game
- [ ] Fine-tune rewards and hyperparameters
- [ ] Optimize for speed and efficiency
- [ ] Handle game restarts and edge cases

### 6. Deployment & Competition
- [ ] Package agent for production use
- [ ] Run agent on actual game website
- [ ] Monitor performance and iterate
- [ ] Achieve top 3 placement! 🏆

## Technical Stack

- **Computer Vision**: OpenCV, EasyOCR
- **Object Detection**: YOLO (Ultralytics)
- **Reinforcement Learning**: OpenAI Gymnasium
- **Deep Learning**: PyTorch (via EasyOCR dependencies)
- **Game Interaction**: TBD (Selenium, PyAutoGUI, or similar)

## Usage

### Setting Up Environment
```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
pip install -r requirements.txt
pip install easyocr  # Already installed
```

### Extracting Frames
```bash
python BuildCustomSet.py
```

### Reading Game State
```bash
# Health
python EasyOCR/Health/GetHealth.py

# Score
python EasyOCR/Score/GetScore.py
```

### Remapping Labels
```bash
python remap_labels.py
```

## Notes

- Health region coordinates: (115, 150, 400, 175)
- Score region coordinates: (100, 125, 400, 150)
- Game displays "Score" and "Health" values that need to be read via OCR
- YOLO dataset includes 7 classes for game object detection

## Resources

- [Neck Deep December Game](https://december.neckdeepuk.com/)
- [OpenAI Gymnasium Documentation](https://gymnasium.farama.org/)
- [EasyOCR Documentation](https://github.com/JaidedAI/EasyOCR)
- [YOLO Documentation](https://docs.ultralytics.com/)

## License

This is a personal project for educational and competition purposes.

---

**Current Status**: 🚧 In Progress - Dataset created, YOLO trained, OCR setup complete, RL environment pending

**Target**: 🎯 Top 3 Leaderboard Position to win merch!

