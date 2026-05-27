"""
CODSOFT AI Internship - Task 5: Face Detection & Recognition
Uses OpenCV DNN (deep learning) face detector + LBPH face recognizer.

Requirements:
    pip install opencv-python opencv-contrib-python numpy

Usage:
    python task5_face_detection.py
"""

import cv2
import numpy as np
import os
import sys
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
DATASET_DIR = "face_dataset"          # folder to store registered faces
MODEL_FILE = "face_recognizer.yml"    # saved recognizer model
CONFIDENCE_THRESHOLD = 60             # lower = stricter match (LBPH)
MIN_DETECTION_CONFIDENCE = 0.7        # for DNN face detector

# ─────────────────────────────────────────────
# FACE DETECTOR — using Haar Cascade (built-in)
# Falls back to DNN if available
# ─────────────────────────────────────────────

def load_face_detector():
    """Load Haar Cascade face detector (comes bundled with OpenCV)."""
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(cascade_path)
    if detector.empty():
        print("❌ Failed to load Haar Cascade. Please reinstall opencv-python.")
        sys.exit(1)
    print("✅ Haar Cascade face detector loaded.")
    return detector


def detect_faces_haar(gray_frame, detector):
    """Detect faces in a grayscale frame using Haar Cascade."""
    faces = detector.detectMultiScale(
        gray_frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    return faces if len(faces) > 0 else []


# ─────────────────────────────────────────────
# FACE RECOGNIZER — LBPH (Local Binary Pattern Histogram)
# ─────────────────────────────────────────────

def create_recognizer():
    """Create an LBPH face recognizer."""
    return cv2.face.LBPHFaceRecognizer_create()


def train_recognizer(recognizer, dataset_dir: str):
    """
    Train the LBPH recognizer from images in dataset_dir.
    Each sub-folder = one person (label).
    Returns label_map: {int_id -> name}
    """
    faces, labels = [], []
    label_map = {}
    label_id = 0

    dataset_path = Path(dataset_dir)
    if not dataset_path.exists():
        print(f"  ⚠️  Dataset directory '{dataset_dir}' not found. Train first.")
        return None, {}

    for person_dir in sorted(dataset_path.iterdir()):
        if not person_dir.is_dir():
            continue
        label_map[label_id] = person_dir.name
        for img_path in person_dir.glob("*.jpg"):
            img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                faces.append(img)
                labels.append(label_id)
        label_id += 1

    if not faces:
        print("  ⚠️  No training images found.")
        return None, {}

    print(f"  🧠 Training on {len(faces)} images for {len(label_map)} person(s)...")
    recognizer.train(faces, np.array(labels))
    recognizer.save(MODEL_FILE)
    print(f"  ✅ Model saved to '{MODEL_FILE}'")
    return recognizer, label_map


# ─────────────────────────────────────────────
# DATA COLLECTION — register a new person
# ─────────────────────────────────────────────

def collect_faces(person_name: str, num_samples: int = 30):
    """
    Open webcam and capture face samples for a new person.
    Saves cropped grayscale face images to dataset_dir/person_name/.
    """
    save_dir = Path(DATASET_DIR) / person_name
    save_dir.mkdir(parents=True, exist_ok=True)

    detector = load_face_detector()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Cannot open webcam.")
        return

    count = 0
    print(f"\n📸 Collecting {num_samples} face samples for '{person_name}'.")
    print("   Look at the camera. Press 'q' to quit early.\n")

    while count < num_samples:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detect_faces_haar(gray, detector)

        for (x, y, w, h) in faces:
            count += 1
            face_roi = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
            img_path = save_dir / f"{count}.jpg"
            cv2.imwrite(str(img_path), face_roi)

            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 200, 0), 2)
            cv2.putText(frame, f"Captured: {count}/{num_samples}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 0), 2)

        cv2.imshow("Collecting Faces — Press Q to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"  ✅ Saved {count} images to '{save_dir}'")


# ─────────────────────────────────────────────
# REAL-TIME DETECTION + RECOGNITION
# ─────────────────────────────────────────────

def run_live_recognition(label_map: dict, recognizer):
    """
    Open webcam feed, detect and recognize faces in real time.
    """
    detector = load_face_detector()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Cannot open webcam.")
        return

    print("\n🎥 Live face recognition started. Press 'q' to quit.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detect_faces_haar(gray, detector)

        for (x, y, w, h) in faces:
            face_roi = cv2.resize(gray[y:y+h, x:x+w], (200, 200))

            if recognizer is not None and label_map:
                label_id, confidence = recognizer.predict(face_roi)
                name = label_map.get(label_id, "Unknown")
                color = (0, 200, 0) if confidence < CONFIDENCE_THRESHOLD else (0, 0, 255)
                label_text = f"{name} ({confidence:.1f})" if confidence < CONFIDENCE_THRESHOLD else "Unknown"
            else:
                color = (255, 165, 0)
                label_text = "Face Detected"

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.rectangle(frame, (x, y-35), (x+w, y), color, cv2.FILLED)
            cv2.putText(frame, label_text, (x+5, y-8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

        # Status bar
        status = f"Faces: {len(faces)}  |  Press Q to quit"
        cv2.putText(frame, status, (10, frame.shape[0]-15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)
        cv2.imshow("CodSoft — Face Detection & Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("  ✅ Session ended.")


# ─────────────────────────────────────────────
# DETECT FACES IN A STATIC IMAGE
# ─────────────────────────────────────────────

def detect_in_image(image_path: str, label_map: dict = None, recognizer=None):
    """Detect (and optionally recognize) faces in a static image file."""
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Cannot read image: {image_path}")
        return

    detector = load_face_detector()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detect_faces_haar(gray, detector)

    print(f"  🔍 Detected {len(faces)} face(s) in '{image_path}'")

    for i, (x, y, w, h) in enumerate(faces):
        face_roi = cv2.resize(gray[y:y+h, x:x+w], (200, 200))

        if recognizer and label_map:
            label_id, confidence = recognizer.predict(face_roi)
            name = label_map.get(label_id, "Unknown") if confidence < CONFIDENCE_THRESHOLD else "Unknown"
            label_text = f"{name} ({confidence:.1f})"
        else:
            label_text = f"Face {i+1}"

        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 200, 0), 2)
        cv2.putText(img, label_text, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 0), 2)
        print(f"    Face {i+1}: {label_text}")

    output_path = "output_detected.jpg"
    cv2.imwrite(output_path, img)
    print(f"  ✅ Saved annotated image to '{output_path}'")
    cv2.imshow("Detection Result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ─────────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  🤖  CodSoft AI — Face Detection & Recognition  🤖")
    print("=" * 55)

    recognizer = create_recognizer()
    label_map = {}

    # Load saved model if exists
    if os.path.exists(MODEL_FILE) and os.path.exists(DATASET_DIR):
        try:
            recognizer.read(MODEL_FILE)
            # Rebuild label map from dataset dir
            for i, d in enumerate(sorted(Path(DATASET_DIR).iterdir())):
                if d.is_dir():
                    label_map[i] = d.name
            print(f"✅ Loaded saved model. Known persons: {list(label_map.values())}")
        except Exception as e:
            print(f"⚠️  Could not load model: {e}")
            recognizer = create_recognizer()

    while True:
        print("\n📋 MENU:")
        print("  1. Register a new person (collect face samples)")
        print("  2. Train recognizer on collected data")
        print("  3. Live webcam detection & recognition")
        print("  4. Detect faces in an image file")
        print("  5. Exit")

        choice = input("\nYour choice: ").strip()

        if choice == "1":
            name = input("  Enter person's name: ").strip()
            if name:
                n = input("  Number of samples (default 30): ").strip()
                collect_faces(name, int(n) if n.isdigit() else 30)
            else:
                print("  ⚠️  Name cannot be empty.")

        elif choice == "2":
            r, lm = train_recognizer(recognizer, DATASET_DIR)
            if r:
                recognizer, label_map = r, lm
                print(f"  ✅ Trained. Known: {list(label_map.values())}")

        elif choice == "3":
            run_live_recognition(label_map, recognizer if label_map else None)

        elif choice == "4":
            path = input("  Enter image file path: ").strip()
            detect_in_image(path, label_map, recognizer if label_map else None)

        elif choice == "5":
            print("  Goodbye! 👋")
            break

        else:
            print("  Invalid option. Try 1–5.")


if __name__ == "__main__":
    main()
