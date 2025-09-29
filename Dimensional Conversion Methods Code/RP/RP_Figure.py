import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image
from pyts.image import RecurrencePlot
import pandas as pd


def load_data(file_path):
    """
    Load the Excel data file from the specified path.

    Parameters:
    file_path (str): Path to the data file

    Return:
    numpy.ndarray: Loaded data array
    """
    try:
        df = pd.read_excel(file_path)
        return df.values
    except FileNotFoundError:
        print(f"Error: File not found {file_path}。")
    except Exception as e:
        print(f"An error occurred while loading the file:  {e}")
    return None


def create_directories(save_path):
    """
    Create a directory to store images and data files.

    Parameters:
    save_path (str): Root path for saving
    """
    img_path = os.path.join(save_path, "images")
    data_path = os.path.join(save_path, "data")
    for path in [img_path, data_path]:
        if not os.path.exists(path):
            os.makedirs(path)
    return img_path, data_path


def generate_rp_images(data, img_size):
    """
    Generate recursive pattern (RP) images.

    Parameters:
    data (numpy.ndarray): Input data array
    img_size (int): Image Generation Size

    Return:
    numpy.ndarray: Generated RP image array
    """
    rp = RecurrencePlot(dimension=7, time_delay=10)
    return rp.fit_transform(data.T)


def save_images_and_data(rp_images, img_path, data_path):
    """
    Save the recursive graph (RP) image and its corresponding data file.

    Parameters:
    rp_images (numpy.ndarray): Generated RP image array
    img_path (str): Path for saving images
    data_path (str): Path for saving data files
    """
    img_num = rp_images.shape[0]
    for i in range(img_num):
        rp_img = rp_images[i, :, :]

        # Create a new graphic
        fig, ax = plt.subplots(figsize=(6, 6))
        # Display Recursive Diagram
        ax.imshow(rp_img)

        # Remove the scale values and their numerical labels from the x-axis and y-axis.
        ax.set_xticks([])
        ax.set_yticks([])

        img_save_path = os.path.join(img_path, f"{i}.png")
        data_save_path = os.path.join(data_path, f"{i}.csv")
        try:
            # Save the graphic with bbox_inches=‘tight’ and pad_inches = 0 to remove white borders.
            fig.savefig(img_save_path, bbox_inches='tight', pad_inches=0)
            np.savetxt(data_save_path, rp_img, delimiter=',')
        except Exception as e:
            print(f"An error occurred while saving the {i}th image or data file.: {e}")
        finally:
            plt.close(fig)  # Close the graphics to release resources.
    return img_num


def main():
    # Modify the variable parameters according to your needs.
    filename = "DataAverage.xlsx"  # Use relative paths
    savepath = "./data"  # Image save path
    img_sz = 165  # Determine the size of the generated image

    print(f"Image size：{img_sz} * {img_sz}")
    img_path, data_path = create_directories(savepath)
    print(f"Visualization images are saved in the folder. {img_path} Data files are stored in the folder. {data_path} ")

    src_data = load_data(filename)
    if src_data is None:
        return

    rp_images = generate_rp_images(src_data, img_sz)
    img_num = save_images_and_data(rp_images, img_path, data_path)
    print(f"Generation complete. A total of {img_num} images were processed.")


if __name__ == "__main__":
    main()
