#!/bin/bash
export FLASK_APP=server
export FLASK_ENV=development

# Start Flask app with debug mode
flask --app server --debug run
