import cv2

# video_path = "videos/1.mp4"  # Use absolute path if needed
# cap = cv2.VideoCapture(video_path)

# if not cap.isOpened():
#     print("Error: Could not open video file")
# else:
#     print("Video opened successfully!")

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             print("End of video or cannot read frame")
#             break
#         cv2.imshow("Test Video", frame)
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             break

# cap.release()
# cv2.destroyAllWindows()

print(cv2.__version__)
