# AI Blog Post Generator

This application allows users to generate blog posts using OpenAI's GPT models. The process is broken down into multiple steps, including topic generation, outline creation, content writing, and content polishing.

## Features

- Generate engaging blog topics based on a specified domain and target audience.
- Create a structured outline for the selected topic.
- Write detailed content based on the outline.
- Polish the generated content for clarity and flow.
- Persist generated content in the browser's local storage.

## Requirements

- Python 3.7+
- Node.js (for React frontend)
- OpenAI API key

## Setup Instructions

### Backend (FastAPI)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

3. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up your OpenAI API key:**
   - Create a `.env` file in the backend directory and add your OpenAI API key:
     ```env
     OPEN_AI_API_KEY=your_openai_api_key_here
     ```

6. **Run the FastAPI server:**
   ```bash
   uvicorn prompt_chaining_api:app --reload
   ```

   The backend will be running at `http://localhost:8000`.

### Frontend (React)

1. **Navigate to the frontend directory:**
   ```bash
   cd blog-generator
   ```

2. **Install the required packages:**
   ```bash
   npm install
   ```

3. **Run the React application:**
   ```bash
   npm start
   ```

   The frontend will be running at `http://localhost:3000`.

## Usage Instructions

1. Open your web browser and navigate to `http://localhost:3000`.
2. Enter a domain (e.g., "artificial intelligence") and a target audience (e.g., "business professionals").
3. Click the "Generate Blog" button to start the process.
4. The application will generate topics, create an outline, write content, and polish it.
5. All generated content will be displayed below, and it will persist even after refreshing the page.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
