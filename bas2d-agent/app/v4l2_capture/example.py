from webcamvideostream_fnctl import WebcamVideoStream
import time, cv2

def main():
    try:
        # time sync to main server

        # os.system("sudo chmod 777 /dev/ttyACM0")
        vs = WebcamVideoStream(src="/dev/video0", src_width=1280, src_height=960, fps=60).start()

        while True:
            try:
                # read frames from stream
                time_start = time.time()
                frame = vs.read()
                time.sleep(0.02)

                cv2.imshow('test', frame)
                key = cv2.waitKey(1)

                print(1 / (time.time() - time_start))

            except KeyboardInterrupt:
                break

    finally:
        vs.stop()

if __name__ == "__main__":
    main()
