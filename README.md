# Resume Tailor

An AI-powered web application that customizes your resume based on job descriptions using Anthropic's Claude API.

## Features

- **PDF Resume Parsing**: Upload and extract text from PDF resumes
- **Job Description Scraping**: Fetch job descriptions from URLs automatically
- **AI-Powered Analysis**: Get intelligent recommendations using Claude AI
- **Match Scoring**: See how well your resume matches the job requirements
- **Actionable Recommendations**: Receive specific suggestions for:
  - Keywords to include
  - Skills to emphasize
  - Content modifications
  - Priority actions

## Architecture

- **Backend**: FastAPI (Python web framework)
- **PDF Processing**: pdfplumber
- **Web Scraping**: BeautifulSoup + requests
- **AI Integration**: Anthropic Claude API (claude-3-5-sonnet)
- **Frontend**: Vanilla HTML/CSS/JavaScript

## Prerequisites

- Python 3.8+
- Anthropic API key ([Get one here](https://console.anthropic.com/))

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd resume_tailor
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

1. **Start the application**:
   ```bash
   python main.py
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload
   ```

2. **Open your browser**:
   Navigate to `http://localhost:8000`

3. **Follow the three-step process**:
   - **Step 1**: Upload your PDF resume
   - **Step 2**: Enter the job description URL
   - **Step 3**: Get AI-powered recommendations

## API Endpoints

### `POST /api/upload-resume`
Upload and extract text from a PDF resume.

**Parameters**:
- `file`: PDF file (multipart/form-data)

**Response**:
```json
{
  "success": true,
  "filename": "resume.pdf",
  "text": "extracted resume text...",
  "pages": 2,
  "message": "Resume uploaded and processed successfully"
}
```

### `POST /api/fetch-job-description`
Fetch job description from a URL.

**Parameters**:
- `url`: Job posting URL (form data)

**Response**:
```json
{
  "success": true,
  "url": "https://example.com/job",
  "title": "Software Engineer",
  "text": "job description text...",
  "length": 5000,
  "message": "Job description fetched successfully"
}
```

### `POST /api/analyze`
Analyze resume against job description.

**Parameters**:
- `resume_text`: Extracted resume text (form data)
- `job_description`: Job description text (form data)

**Response**:
```json
{
  "success": true,
  "recommendations": "AI-generated recommendations...",
  "model": "claude-3-5-sonnet-20241022",
  "usage": {
    "input_tokens": 1500,
    "output_tokens": 800
  },
  "message": "Analysis completed successfully"
}
```

### `GET /api/health`
Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "api_key_configured": true
}
```

## Project Structure

```
resume_tailor/
├── main.py                    # FastAPI application
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── README.md                 # This file
├── modules/
│   ├── __init__.py
│   ├── pdf_extractor.py      # PDF processing module
│   ├── jd_scraper.py         # Job description scraper
│   └── claude_analyzer.py    # Claude AI integration
├── templates/
│   └── index.html            # Frontend interface
└── uploads/                   # Temporary PDF storage (auto-created)
```

## How It Works

1. **PDF Extraction**: The app uses `pdfplumber` to extract text content from your PDF resume, preserving formatting and structure.

2. **Job Description Fetching**: BeautifulSoup scrapes the job posting URL, cleaning and extracting the relevant job description text.

3. **AI Analysis**: Claude AI analyzes both texts and provides:
   - Match percentage and explanation
   - Skills gap analysis
   - Recommended additions and modifications
   - ATS-friendly keywords
   - Priority actions ranked by impact

4. **Recommendations Display**: Results are formatted and displayed in an easy-to-read format with clear sections.

## Configuration

### Claude Model
By default, the app uses `claude-3-5-sonnet-20241022`. You can modify this in `modules/claude_analyzer.py`:

```python
def analyze_resume_for_job(
    self,
    resume_text: str,
    job_description: str,
    model: str = "claude-3-5-sonnet-20241022"  # Change here
):
```

### Server Configuration
Modify host and port in `main.py`:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Change here
```

## Security Notes

- PDF files are temporarily stored and immediately deleted after processing
- Never commit your `.env` file with API keys
- The app includes CORS middleware for development; configure appropriately for production
- Validate and sanitize all user inputs

## Limitations

- Only supports PDF resumes (not Word documents)
- Web scraping may fail on some job sites with heavy JavaScript or anti-scraping measures
- API costs apply based on Claude usage (input/output tokens)

## Troubleshooting

### "ANTHROPIC_API_KEY not configured"
- Make sure you've created a `.env` file
- Verify the API key is correct and not expired
- Restart the server after updating `.env`

### "Failed to extract PDF"
- Ensure the PDF is not password-protected
- Check if the PDF contains actual text (not just images)
- Try converting your resume to a text-based PDF

### "Failed to fetch job description"
- Some websites block automated scraping
- Try a different job posting URL
- Check if the URL is accessible in your browser

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Anthropic Claude](https://www.anthropic.com/)
- PDF processing by [pdfplumber](https://github.com/jsvine/pdfplumber)
