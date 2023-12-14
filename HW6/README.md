# Rover Image Classification and Movement

This project trains an image classification model and uses the results to control the movement of a rover. The rover uses a camera to capture images, which are then classified by the model into different categories. Depending on the classification result, the rover performs a specific movement.

## Image Classification Model

We train an image classification model. The model is trained on a dataset of images of various objects, including paper cups, table tennis bats, black bottles, and paper cases.

## Rover Movement

The rover moves based on the result of the image classification:

- If the model classifies the image as a paper cup, the rover moves straight a little bit.
- If the model classifies the image as a table tennis bat, the rover moves back a little bit.
- If the model classifies the image as a black bottle, the rover moves in a triangle.
- If the model classifies the image as a paper case, the rover moves in a square.

## Running the Project

To run the project, first train the image classification model. Then, run the main script to start the rover's movement based on the model's classifications.
