from flask import Flask
app = Flask(__name__)

const = {
    'layout': 'hello-world',
    'dash.react': 'making-dash-apps-interactive',
    'slider-example': 'slider-example',
    'click-and-hover': 'click-and-hover',
    'text-input': 'text-input'
}

import userguide.index
import userguide.helloworld
import userguide.dash_react
import userguide.example_slider
import userguide.click_and_hover
import userguide.text_input
