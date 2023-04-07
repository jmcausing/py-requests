# Python app that accepts string request
# Author: John Mark Causing
# Date: April 7, 2023
# Example usage:
# curl https://py-requests-optgf.kinsta.app/greet?name=john
# Hello, john!


from flask import Flask, request
import atexit
import os, logging, sys
import face_recognition

class process_encoding:
     ## Debug print
    print('# Start class process_encoding')

    """
    Video Face detection that alerts if it detects an unknown face/intruder 
    """

    def setup(self):
        ## Debug print
        print('# setup() - Setting up..')     

        ## Log settings
        self.py_script_path = os.path.dirname(os.path.realpath(__file__))
        self.log_file_name='vfs.log'
        self.log_path = f'{self.py_script_path}/logs/{self.log_file_name}'
        self.log_level = logging.DEBUG  ## possible values: DEBUG, INFO, WARNING, ERROR, CRITICAL
        self.log_format = '%(asctime)s - [%(levelname)s]: %(message)s'
        self.log_date_format = '%Y-%m-%d %H:%M:%S'

        ## Set up logging
        ls = self.logSetup(self.log_path, self.log_level, self.log_format, self.log_date_format)        
        if ls != True:
            #### SETUP SLACK FIRST! THIS WILL NOT WORK!!!
            ####
            ####
            self.alert_and_shutdown(exitCode=1, msg='Setup() - Error setting up logs')


        # Image folder and files location for known friendly faces.
        self.target_file = [] # List of image files
        self.target_file_dir = 'known_faces_images' # or specific path '/mnt/c/Users/JMC/python/face/images'  

        ## Check if folder known_faces_images exist
        if not os.path.exists(self.target_file_dir):
            logging.error(f"setup() - Cannot locate the folder {self.target_file_dir} \nShutting down.")
            exit()
                
        # Check if folder self.target_file_dir is empty
        if len(os.listdir(self.target_file_dir)) == 0:
            logging.error(f"setup() - folder {self.target_file_dir} is empty!")

        # If it reeached here, then self.target_file_dir is ready and not empty!
        # Start processing the files inside self.target_file_dir
        for file in os.listdir(self.target_file_dir):
                self.target_file.append(file)

        ## Debug        
        logging.debug(f"setup() - Image files found in {self.target_file_dir}: {self.target_file}")

        # Setup known face encoding
        print('# setup() - Start encoding known faces..')
        self.known_face_encodings = []         
        self.encode_known_faces()

        # Setup Flask that accepts string requests
        app = Flask(__name__)
        @app.route("/greet")
        def greet():

            name = request.args.get("name")

            if name:
                return f"Hello, {name}! xx"
            else:
                return "Please provide a name."

        # Read the log file
        #
        # MAKE SURE TO SECURE THIS AFTER TESTING
        # So no one can access this log file!
        #
        # http://localhost:8080/logs
        @app.route("/logs")
        def logs():
            with open(self.log_path, 'r') as file:
                content = ''
                for line in file:
                    content += f'<p>{line.strip()}</p>\n'

            return f"<p>Reading log file:<p> <br></p>{content}</p>"
        
        # Start Flask web server with port 8080 (Kinsta app hosting requires port 8080)
        app.run(debug=False, host='0.0.0.0', port=8080)

        ## Debug print    
        print('# Setup finished!')
        print('#')        

    # Load and encode all images from the list self.target_file (The known faces)
    def encode_known_faces(self):
        for image in self.target_file:
            print(f"# encode_known_faces() - Encoding image {image}")
            load_image = face_recognition.load_image_file(f"{self.target_file_dir}/{image}")
            self.known_face_encodings.append(face_recognition.face_encodings(load_image))      


        #print(self.known_face_encodings)
        try:
            check_known_face_encodings = self.known_face_encodings[0]
            ## DEBUG
            print('# encode_known_faces() - list self.known_face_encodings is not empty!')
            logging.info(f'# encode_known_faces() - list self.known_face_encodings is not empty. These are the encodings: {self.known_face_encodings}')
        except IndexError:
            logging.error(f'# encode_known_faces() - list self.known_face_encodings ({self.known_face_encodings}) is EMPTY!!')
            exit()
        

   # Setup logging
    def logSetup(self, log_path, log_level, log_format, log_date_format):
        # Setting up log facility
        target_dir = f'{self.py_script_path}/logs'
        if not os.path.isdir(target_dir):
            try:
                os.mkdir(target_dir)
            except OSError as e:
                logging.error(f"Couldn't create log folder: {e!r}\nShutting down.")
                return f'{e!r}'
        try:
            logging.basicConfig(filename=log_path, level=log_level, format=log_format, datefmt=log_date_format)
        except Exception as e:
            return f'{e!r}'
        else:
            logging.info('logSetup() - Logging setup complete')
            return True
        
    # Start run()    
    def run(self):
        print("# run() - Starting...")
        # Setup our environment
        self.setup()


def detect_exit():
    logging.info(f'detect_exit() - Script was shutdown/interrupted')

def main(request): # 
    # Detect and log if the script was shutdown/exit
    atexit.register(detect_exit)
    check = process_encoding()
    return check.run()


if __name__ == '__main__':
    try:
        main(None)
    except Exception as e:
        print(e)



