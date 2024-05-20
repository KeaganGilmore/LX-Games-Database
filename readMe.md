# LX Games Data API

## Overview

The LX Games Data API is a simple Flask API designed to manage data tracking for the LX Games project within LXLibrary. This API facilitates data storage and retrieval for various game types and will be utilized internally to support the educational objectives of the LX Games project.

## Purpose

The LX Games project aims to create a stimulating education experience while leveraging machine learning techniques to gain insights and improve educational outcomes. The LX Games Data API serves as an essential component of this initiative, enabling the collection and analysis of game-related data to inform the development of educational content and methodologies.

## Features

- Allows for the storage and retrieval of game data in JSON format.
- Supports multiple game types, each with its own endpoint for data management.
- Provides a simple interface for adding and retrieving game data.

## Usage

### Adding Game Data

To add game data, send a POST request to the corresponding endpoint for the desired game type, providing the JSON data for the game session.

### Retrieving Game Data

To retrieve game data, send a GET request to the appropriate endpoint for the desired game type.

## Installation and Setup

- Clone the repository.
- Install dependencies using `pip install -r requirements.txt`.
- Run the Flask application using `python app.py`.

## Contribution Guidelines

Contributions to the LX Games Data API are welcome. Please open an issue to discuss proposed changes before submitting a pull request. Ensure that any new features or changes align with the project's objectives and adhere to coding standards.


