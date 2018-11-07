import DeepDreamCore as DDC
import helperfunctions as h

def main():
    print("hello")

    dd = DDC.DeepDream()
    print(len(dd.model.layer_tensors))

    image = h.load_image(filename='images/hulk.jpg')
    print(image)
    #h.plot_image(image)

    layer_tensor = dd.model.layer_tensors[2]
    print(layer_tensor)

    img_result = dd.optimize_image(layer_tensor, image,
                   num_iterations=10, step_size=6.0, tile_size=400,
                   show_gradient=False)

    print(img_result)

if __name__ == "__main__":
    main()