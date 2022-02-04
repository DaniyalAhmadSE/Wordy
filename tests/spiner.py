from time import sleep
from models.bst import BST
from pkg.loadingspinner import loadingspinner as spin

spin.setText("Test...")
spin.setFrames(["x", "+"])
spin.setTextColor("yellow")
spin.setSpinnerColor("red")
spin.start()
sleep(1)
spin.setText("You see, it works!")
spin.setTextColor("green")
spin.setSpinnerColor("green")
sleep(0.5)
spin.stop()
print("")
