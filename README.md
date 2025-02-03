# AwakeMate

**AwakeMate** is your attentiveness checker, whether you're on the road or at your desk! Imagine a smart system that not only keeps you alert while driving but also helps you stay productive and focused at home. By monitoring your facial cues through your webcam, AwakeMate determines if you're **active**, **drowsy**, or **sleepy**, and it even sounds an alarm if it catches you distracted by your phone. With AwakeMate, safety and productivity are always within reach.

## Features

- **Real-Time Face and Eye Detection:**  
  Leveraging OpenCV and the `face_recognition` library, AwakeMate rapidly detects your face and key eye landmarks. This real-time analysis is crucial whether you're navigating busy highways or powering through a workday.

- **Advanced Eye Aspect Ratio (EAR) Calculation:**  
  Using precise Euclidean measurements, AwakeMate calculates the Eye Aspect Ratio (EAR) to determine your alertness:
  - **Active:** Eyes wide open—you're fully engaged, whether you're steering or strategizing.
  - **Drowsy:** Eyes partially closed—time for a quick break before fatigue sets in.
  - **Sleepy:** Eyes closed—dangerous behind the wheel or unproductive at home!

- **Intelligent Alert System:**  
  AwakeMate uses Pygame to play a crisp beep when it detects drowsiness, sleepiness, or if you're distracted by your phone. This immediate audible alert snaps you back into action, keeping you safe on the road and productive at your desk.

- **Seamless Web-Based Video Stream:**  
  Enjoy a live video feed via a Flask-powered web application, complete with a real-time overlay displaying your current status. Whether you're checking your alertness before a drive or during a long work session, AwakeMate has you covered.

## How It Works

1. **Video Capture:**  
   AwakeMate taps into your webcam—be it integrated in your car or attached to your computer—to capture your facial cues in real time.

2. **Face and Landmark Detection:**  
   Using the powerful `face_recognition` library, it identifies your face and pinpoints critical eye landmarks with outstanding accuracy, even in varied lighting conditions.

3. **EAR Calculation:**  
   With exact Euclidean distance measurements, AwakeMate gauges how open your eyes are, translating this data into a clear alertness level.

4. **Status Determination:**  
   Based on the EAR:
   - **Active:** EAR ≥ 0.28 (Eyes wide open and engaged)
   - **Drowsy:** 0.20 ≤ EAR < 0.28 (Eyes beginning to droop—consider a break)
   - **Sleepy:** EAR < 0.20 (Eyes closed—high risk, either pull over or reenergize!)
   
   A frame counter ensures your state is accurately confirmed, avoiding false alarms from brief blinks.

5. **Audio Alerts:**  
   When signs of drowsiness, sleepiness, or distraction are detected, Pygame instantly plays a beep—giving you that critical nudge to refocus, whether you're behind the wheel or at your workstation.

6. **Web Integration:**  
   A dynamic Flask application streams your live video feed, complete with an overlay showing your current status. This makes it effortless to monitor your alertness level in any environment.

## Versatility: On the Road and at Home

**For Drivers:**  
AwakeMate is a game-changer on the road. It acts as a vigilant co-pilot, ensuring that fatigue or distraction never compromises your safety. If your eyes start to close or you get caught using your phone, AwakeMate's timely alerts help you make safe decisions instantly.

**For Home and Office:**  
Not just for drivers, AwakeMate is also your productivity partner at home or in the office. Keep distractions at bay and ensure that your focus remains sharp during long work sessions or study periods. With real-time monitoring and instant alerts, you can maximize your efficiency and maintain peak performance all day long.

## Installation

### Prerequisites

- **Python 3.6+**
- **pip** (Python package installer)

### Required Python Packages

Install the necessary libraries using pip:

```bash
pip install opencv-python numpy face_recognition scipy pygame flask
```

---

Embrace the power of AwakeMate—your vigilant partner for safer driving and boosted productivity. Whether you're hitting the road or conquering your to-do list at home, AwakeMate is here to keep you alert, engaged, and always in control!
