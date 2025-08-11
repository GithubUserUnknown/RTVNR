from PlateFinder import PlateFinder
from OCR import OCR
import cv2
import datetime
import pymongo



if __name__ == "__main__":
    
    findPlate = PlateFinder(minPlateArea=4100, maxPlateArea=15000) 
    model = OCR(modelFile="model/binary_128_0.50_ver3.pb", labelFile="model/binary_128_0.50_labels_ver2.txt") 

    cap = cv2.VideoCapture('test1.MP4')

    # Open the file in write mode
    with open('CARPLATES.txt', 'a') as file:
        while (cap.isOpened()): 
            ret, img = cap.read() 
            
            if ret == True: 
                cv2.imshow('original video', img) 
                
                if cv2.waitKey(25) & 0xFF == ord('q'): 
                    break
                
                possible_plates = findPlate.find_possible_plates(img) 
                if possible_plates is not None: 
                    
                    for i, p in enumerate(possible_plates): 
                        chars_on_plate = findPlate.char_on_plate[i] 
                        recognized_plate, _ = model.label_image_list(chars_on_plate, imageSizeOuput=128) 

                        # Get the current time
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Print the recognized plate
                        print(recognized_plate)

                        def address(Street="Fafadih",City="Raipur",State="Chattisgarh",Zip=497001):
                            Street=Street
                            City=City
                            State=State
                            Zip=Zip
                            return f"{Street} {City} {State} {Zip}"
                        
                         # Write to the file
                        file.write(f"{current_time} - {recognized_plate} -{address()} \n")

                        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

                        mydb = myclient["carLocation"]
                        mycol = mydb["location"]
                        
                        def Maddress(Street="Fafadih", City="Raipur", State="Chattisgarh", Zip=497001):
                            return {
                                "Street": Street,
                                "City": City,
                                "State": State,
                                "Zip": Zip
                            }
                        
                       

                        CarLoc = { "current_time":current_time , "recognized_plate": recognized_plate, "address":Maddress() }

                        x = mycol.insert_one(CarLoc)

                        print(x.inserted_id)
                        
                        cv2.imshow('plate', p) 
                        
                        if cv2.waitKey(25) & 0xFF == ord('q'): 
                            break
            else: 
                break
            
    cap.release() 
    cv2.destroyAllWindows()