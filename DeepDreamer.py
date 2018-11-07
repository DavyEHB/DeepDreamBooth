import DeepDreamCore as DDC
import helperfunctions as h
import numpy as np
import cv2
import time



def showImage(image, name):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    image = np.clip(image/255.0, 0.0, 1.0)
    opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) 
    cv2.imshow(name,opencvImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    print("hello")
    view_finder = "Viewfinder"

    dd = DDC.DeepDream()
    print(len(dd.model.layer_tensors))

    

    image = h.load_image(filename='images/hulk.jpg')
    img = cv2.imread('images/hulk.jpg')
    #h.plot_image(image)
    #Finaly show the frame

    #showImage(image,view_finder)


    layer_tensor = dd.model.layer_tensors[9]
    #layer_tensor = dd.model.layer_tensors[7][:,:,:,0:3]
    #layer_tensor = dd.model.layer_tensors[11]
    print(layer_tensor)

    start = time.time()

    #img_result = dd.optimize_image(layer_tensor, image,
    #            num_iterations=5, step_size=6.0, tile_size=400,
    #            show_gradient=False)

    img_result = dd.recursive_optimize(layer_tensor=layer_tensor, image=image,
                 num_iterations=15, step_size=6.0, rescale_factor=0.7,
                 num_repeats=10, blend=0.2)

    end = time.time()

    print("Time elapsed: ")
    print(end - start)
  

    showImage(img_result,view_finder)

if __name__ == "__main__":
    main()