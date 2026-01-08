"""
Resume Tailor - Main FastAPI Application
A web app to customize resumes based on job descriptions using Claude AI
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

from modules.pdf_extractor import PDFExtractor
from modules.jd_scraper import JDScraper
from modules.claude_analyzer import ClaudeAnalyzer

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Resume Tailor",
    description="AI-powered resume customization based on job descriptions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Initialize components
pdf_extractor = PDFExtractor()
jd_scraper = JDScraper()

# Initialize Claude analyzer (will be created per request to handle API key)
def get_claude_analyzer():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="ANTHROPIC_API_KEY not configured. Please set it in .env file"
        )
    return ClaudeAnalyzer(api_key)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML page"""
    html_path = Path("templates/index.html")
    if html_path.exists():
        return html_path.read_text()
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Resume Tailor</title>
    </head>
    <body>
        <h1>Resume Tailor</h1>
        <p>Frontend not found. Please ensure templates/index.html exists.</p>
    </body>
    </html>
    """


@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and extract text from a PDF resume

    Args:
        file: PDF file upload

    Returns:
        Extracted resume text and metadata
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Save uploaded file
    file_path = UPLOAD_DIR / file.filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text from PDF
        result = pdf_extractor.extract_text(str(file_path))

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to extract PDF"))

        return JSONResponse({
            "success": True,
            "filename": file.filename,
            "text": result["text"],
            "pages": result["pages"],
            "message": "Resume uploaded and processed successfully"
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    finally:
        # Clean up uploaded file
        if file_path.exists():
            file_path.unlink()


@app.post("/api/fetch-job-description")
async def fetch_job_description(url: str = Form(...)):
    """
    Fetch job description from a URL

    Args:
        url: Job posting URL

    Returns:
        Job description text and metadata
    """
    # Validate URL
    if not jd_scraper.validate_url(url):
        raise HTTPException(status_code=400, detail="Invalid URL format")

    # Fetch job description
    result = jd_scraper.fetch_job_description(url)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error", "Failed to fetch job description"))

    return JSONResponse({
        "success": True,
        "url": result["url"],
        "title": result.get("title"),
        "text": result["text"],
        "length": result["length"],
        "message": "Job description fetched successfully"
    })


@app.post("/api/analyze")
async def analyze_resume(
    resume_text: str = Form(...),
    job_description: str = Form(...)
):
    """
    Analyze resume against job description and provide recommendations

    Args:
        resume_text: Extracted resume text
        job_description: Job description text

    Returns:
        AI-generated recommendations for tailoring the resume
    """
    try:
        # Get Claude analyzer
        analyzer = get_claude_analyzer()

        # Analyze resume
        result = analyzer.analyze_resume_for_job(resume_text, job_description)

        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Analysis failed"))

        return JSONResponse({
            "success": True,
            "recommendations": result["recommendations"],
            "model": result["model"],
            "usage": result["usage"],
            "message": "Analysis completed successfully"
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@app.post("/api/tailor-section")
async def tailor_section(
    section_name: str = Form(...),
    original_content: str = Form(...),
    job_description: str = Form(...)
):
    """
    Generate a tailored version of a specific resume section

    Args:
        section_name: Name of the section (e.g., "Summary", "Experience")
        original_content: Original section content
        job_description: Job description text

    Returns:
        Tailored section content
    """
    try:
        # Get Claude analyzer
        analyzer = get_claude_analyzer()

        # Generate tailored section
        result = analyzer.generate_tailored_section(
            section_name,
            original_content,
            job_description
        )

        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Section generation failed"))

        return JSONResponse({
            "success": True,
            "section": result["section"],
            "tailored_content": result["tailored_content"],
            "message": "Section tailored successfully"
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tailoring error: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    api_key_configured = bool(os.getenv("ANTHROPIC_API_KEY"))
    return {
        "status": "healthy",
        "api_key_configured": api_key_configured
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
