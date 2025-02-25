import os
from openai import OpenAI
import requests
import fal_client 

#if error use venv interpreter 
client = OpenAI(
    api_key = ''
)

def generate_New_Image(user_prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt= user_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    return image_url


# def edit_Existing_Image():
#     response = client.images.create_variation(
#         model="dall-e-2",
#         image=open("corgi_and_cat_paw.png", "rb"),
#         n=3,
#         size="1024x1024"
#     )



def variations(image_png):

    variations_List = []

    response = client.images.create_variation(
        model="dall-e-2",
        image=open(image_png, "rb"),
        n=1,
        size="1024x1024"
    )

    variations_List.append(response.data[0].url)

    return variations_List

def download_image(image_url, filename="downloaded_image.png"):
    # Get the image content
    response = requests.get(image_url)
    response.raise_for_status()  # Raises HTTPError if the response was unsuccessful

    # Open a file in binary write mode and write the content
    with open(filename, "wb") as f:
        f.write(response.content)

    print(f"Image saved to {filename}")

def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
           print(log["message"])


def run_trellis(url):
    result = fal_client.subscribe(
        "fal-ai/trellis",
        arguments={
            "image_url": url
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )
    print(result)


if __name__ == "__main__":
    user_prompt = input("Enter your 3D model description: ")
    user_prompt_eng = "I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS:" + user_prompt

    variations_List = []
    os.makedirs("myimage", exist_ok=True)

    i = 0 

    # Generate and download multiple images
    urls = [generate_New_Image(user_prompt_eng) for _ in range(2)] 

    
    run_trellis(urls[0])




    # for url in urls:
    #     file_dir = f"source/download{i}.jpg"
    #     download_image(url, file_dir)
    #     print(f"Downloaded: {file_dir}")
    #     i += 1 
    


    # i = 0 

    # for url in urls:
    #     png_name = f"source/download{i}.jpg"
    #     variations_List.append(variations(png_name))
    #     print(f"Got list for: {png_name}")
    #     i += 1 
    
    
    # i = 0 

    # print(len(variations_List))

    # for variation in variations_List:
    #     file_dir = f"source/download{i}_Variation{i}.jpg"
    #     vara = variation[0] #since it is put into a list in varitations funciton 
    #     download_image(vara, file_dir)
    #     print(f"Downloaded: {file_dir}")
    #     i += 1 


#--------





