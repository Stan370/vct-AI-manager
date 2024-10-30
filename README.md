# vct-AI-manager

## Introduction

The VCT AI Manager is a project designed to leverage large language models (LLMs) for generating optimized team compositions in competitive gaming, specifically for Valorant. This project utilizes a combination of modern web technologies and AWS Bedrock to create a robust architecture that facilitates data management, processing, and user interaction.

### Prerequisites
* Python 3.9 or higher
* pip
* [Model Access in Amazon Bedrock](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess)

## Architecture Overview

### Frontend
- **Technologies**: Tailwind CSS + TypeScript
- **Framework**: Built using React or Next.js
- **Description**: The frontend provides a user-friendly interface for users to interact with the application, input prompts, and view generated team compositions.

### Backend
- **Technologies**: Python-based server
- **Frameworks**: Flask or FastAPI
- **Description**: The backend manages LLM queries and responses, handling requests from the frontend and processing them to generate meaningful outputs.

### LLM Processing
- **Integration**: Amazon Bedrock or other APIs (like OpenAI)
- **Description**: The application integrates with LLM services to process user prompts and generate detailed team compositions based on the input provided.

## Datasets

The datasets used in this project include player profiles, performance metrics, and historical match data. These datasets are crucial for training the LLM to understand player roles, strengths, weaknesses, and overall team synergy. The data is collected from various sources, preprocessed, and stored in the database for efficient access and analysis. The data was from [s3 bucket](https://vcthackathon-data.s3.us-west-2.amazonaws.com), [vlr.gg](https://www.vlr.gg/vct-2024) and [kaggle](https://www.kaggle.com/datasets/ryanluong1/valorant-champion-tour-2021-2023-data/data).

- **Scripts**: Python scripts for data collection and preprocessing
- **Description**: Custom scripts are developed to gather and preprocess data for training AI models, ensuring that the data is clean and structured for optimal performance.



## Getting Started

To get started with the VCT AI Manager, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/vct-ai-manager.git
   cd vct-ai-manager
   ```

2. **Install Dependencies**:
   For the frontend:
   ```bash
   cd vct-ai-manager
   npm install
   ```

   For the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
   To get a local copy up and running, follow these simple steps.

3. **Set Up the Environment**:
   Initialize your database and run any necessary migrations.
   config your AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY in .env.local

4. **Deploy the Application**:
   Start the backend server:
   ```bash
   cd backend
   python app.py

   ```

   Start the frontend development server:
   ```bash
   cd frontend
   npm start
   ```

5. **Access the Application**:
   Open your browser and navigate to [http://localhost:3000](http://localhost:3000) to start using the VCT AI Manager.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
