'''
    Made by: Tero Jokela

    Started: 16.11.2017 | 15.21
'''
import os
import sys
# We use this to get random numbers
from random import randint
# Our image manipulator/filter libraries
from PIL import Image, ImageFilter

# This function makes a new folder to a desired path if one doesn't already exist
def Directory(path, folderName):
    completePath = path + folderName + '/'
    if not os.path.exists(completePath):
        os.makedirs(completePath)
        return completePath
    else:
        return completePath

# Stretches your desired image by a percentage you give it and then saves it as "(original name) + _stretched".
# Saved as a PNG file
def stretched(image, percentage):
    print("Starting . . . ")

    targetImage = Image.open(image)

    # Calculate the new size for our new image and resize it
    newSize = (int(targetImage.width * (1.0 + (float(percentage) / 100.0))), targetImage.height)
    stretchedImage = targetImage.resize(newSize)

    print("Original resolution: ", targetImage.width, " - ", targetImage.height)
    print("New resolution: ", stretchedImage.width, " - ", stretchedImage.height)
    
    # Save the image
    print("Saving . . . ")
    stretchedImage.save(image[:-4] + "_stretched.png")

    print("Finished!")


# This gives a "breating" effect to a picture and saves it as a GIF
def breathingGIF(image):
    print("Starting . . . ")
    
    try:
        targetImage = Image.open(image)
        
        # "frames" is a list of all the frames that the GIF is going to have
        print("Beginning making the frames . . . ")
        frames = []
    
        # blurRange is how blurred the GIF is going to get at max
        blurRange = 13
        for i in range(blurRange):
            frameBlurDown = targetImage.filter(ImageFilter.GaussianBlur(i))
            frames.append(frameBlurDown)

        for i in range(blurRange, 0, -1):
            frameBlurDown = targetImage.filter(ImageFilter.GaussianBlur(i))
            frames.append(frameBlurDown)

        # Save the image
        print("Frames made!\nSaving . . . ")
        targetImage.save(image[:-4] + "_breathing.gif", save_all=True, append_images=frames, duration=0, optimize=False, loop=0)
        print("Finished!")
        print("Saved as [ " + image[:-4] + "_breathing.gif ]")
        
    # Basic errors
    except FileNotFoundError:
        print("Image not found . . . ")
    except OSError:
        print("Image not found . . . ")
    except:
        print("Unkown error [" + str(sys.exc_info()[0]) + "]")

# You pass in three color channels and it returns one of them chosen randomly
def getRandomColorChannel(Red, Green, Blue):
    whichOne = randint(1, 3)

    if whichOne == 1:
        return Red
    elif whichOne == 2:
        return Green
    else:
        return Blue

# Makes multiple images with our "coolColors" filter which just shuffles the RGB channels to give some weird and cool effects
def coolColors(image, amount):
    print("Starting . . . ")

    # Open the image so we can manipulate it
    targetImage = Image.open(image)

    # Split the image in to 4 lanes
    R, G, B, A = targetImage.split()
        
    # "amount" is how many images we want to make, we also save them seperately
    for i in range(1, int(amount) + 1):
        # Get random color lanes and merge them in to a new image
        finished = Image.merge("RGBA", (getRandomColorChannel(R, G, B), getRandomColorChannel(R, G, B), getRandomColorChannel(R, G, B), A))

        # Make sure the directory exists (See comment of this function)
        Directory(os.getcwd() + "/", image[:-4])

        # Save the image
        finished.save(image[:-4] + "/" + image[:-4] + "_coolColors" + str(i) + "." + image[-3:])
            
        print("Image [ " + image[:-4] + "_coolColors" + str(i) + "." + image[-3:] + " ] saved!")

    print("Finished!")

# Does the same thing as the function above, but instead of saving every picture seperately
# we save the frames in to a GIF
def coolColorsGIF(image, amount):
    print("Starting . . . ")

    # Get the target image
    targetImage = Image.open(image)

    # Split the color channels
    R, G, B, A = targetImage.split()
        
    # This list holds all the frames
    frames = []

    # Make a random picture and add it as a frame to our "frames" list
    for i in range(1, int(amount) + 1):
        frame = Image.merge("RGBA", (getRandomColorChannel(R, G, B), getRandomColorChannel(R, G, B), getRandomColorChannel(R, G, B), A))

        frames.append(frame)

        print("Frame " + str(i) + " made!")
        
    # Save the GIF with all the frames included
    print("Saving . . . ")
    targetImage.save(image[:-4] + "_coolColorsGIF.gif", save_all=True, append_images=frames, duration=0, optimize=False, loop=0)

    print("Finished!")

# Blend's 2 images together with a desired alpha for the second image which is on top
def blend(image, image2, alpha):
    print("Starting . . . ")

    try:
        firstImage = Image.open(image)
        secondImage = Image.open(image2)

        # Make sure they have an alpha channel for transparency
        firstImage = firstImage.convert(mode="RGBA")
        secondImage = secondImage.convert(mode="RGBA")
        # Make the second image the same size as the first image
        secondImage = secondImage.resize((firstImage.width, firstImage.height))

        # Create a new image and blend the 2 images together and save it
        finalImage = Image.new("RGBA", (firstImage.width, firstImage.height))
        finalImage = Image.blend(firstImage, secondImage, float(alpha))
        finalImage.save(image[:-3] + "_and_" + image2[:-3] + "_blend.png")
        print("Finished!")

    # Basic errors
    except FileNotFoundError:
        print("Image not found . . . ")
    except OSError:
        print("Image not found . . . ")
    except ValueError:
        print("I can't do this to GIFs...")
    except:
        print("Unkown error [" + str(sys.exc_info()[0]) + "]")    

# Our entry point of our program if used as itself
# Get the user's input on what effect/filter he/she wants
def main():
    print('What kind of effect do you want? (breathing, coolColors, coolColorsGIF, blend, stretched)')
    filterChoice = input('> ')

    if filterChoice == 'breathing':
        print('You chose "' + filterChoice + '"!')
        print("What's the name of your picture? (Remember the file-extension)")
        breathingGIF(input("> "))
    elif filterChoice == 'coolColors':
        print('You chose "' + filterChoice + '"!')
        print("What's the name of your picture? (Remember the file-extension)")
        coolColors(input("> "), input("How many?\n> "))
    elif filterChoice == 'coolColorsGIF':
        print('You chose "' + filterChoice + '"!')
        print("What's the name of your picture? (Remember the file-extension)")
        coolColorsGIF(input("> "), input("How many?\n> "))
    elif filterChoice == 'blend':
        print('You chose "' + filterChoice + '"!')
        print("What are the names of your pictures? (Remember the file-extensions)")
        blend(input("First picture\n> "), input("Second picture\n> "), input("Alpha\n> "))
    elif filterChoice == 'stretched':
        print('You chose "' + filterChoice + '"!')
        print("What's the name of your picture? (Remember the file-extension)")
        stretched(input("> "), input("How stretched do you want it? (+%)\n> "))
    else:
        print("Sorry, I didn't understand\n")
        main()

# If this is being ran by itself, go to "main"
if __name__ == '__main__':
    main()
    