# NeuraVis Business Assistant Agent

An intelligent AI-powered chatbot that represents **NeuraVis Technologies**, built with OpenAI's GPT and deployed via Gradio.

## 🎥 Video Demo

[![Watch the Demo Video](https://img.shields.io/badge/▶️_Watch_Demo_Video-FF0000?style=for-the-badge&logo=googledrive&logoColor=white)](https://drive.google.com/file/d/1tdmvuhTKL3w6S0zN9S33uSyDqtHn6qfM/view?usp=sharing)

**Click the button above to watch the full demonstration!** The video showcases all key features including business Q&A, lead collection, and feedback logging.

<details>
<summary>🎬 Embedded Video Player (Click to expand)</summary>

<div align="center">
  <a href="https://drive.google.com/file/d/1tdmvuhTKL3w6S0zN9S33uSyDqtHn6qfM/view?usp=sharing">
    <img src="https://drive.google.com/thumbnail?id=1tdmvuhTKL3w6S0zN9S33uSyDqtHn6qfM&sz=w1000" alt="Video Thumbnail" width="600"/>
  </a>
  <p><i>Click the thumbnail above to play the video</i></p>
</div>

**Direct Player Links:**

- [▶️ Open in Google Drive Player](https://drive.google.com/file/d/1tdmvuhTKL3w6S0zN9S33uSyDqtHn6qfM/preview)
- [📥 Download Video](https://drive.google.com/uc?export=download&id=1tdmvuhTKL3w6S0zN9S33uSyDqtHn6qfM)

</details>

## �🎯 Features

- **Business Q&A**: Answers questions about NeuraVis's mission, services, team, and values
- **Lead Collection**: Records customer contact information via `record_customer_interest` tool
- **Feedback Logging**: Captures unanswered questions via `record_feedback` tool
- **Push Notifications**: Sends alerts via Pushover when leads or feedback are recorded
- **Interactive Chat**: Gradio-based web interface for easy interaction

## 📁 Project Structure

```
business_bot/
├── me/
│   ├── about_business.pdf      # Business profile (PDF)
│   └── business_summary.txt    # Business summary (TXT)
├── business_agent.ipynb        # Main Jupyter notebook
├── app.py                      # Deployment script for HuggingFace Spaces
├── .env                        # API keys (not committed to git)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Edit the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=your_actual_openai_api_key_here
```

### 3. Run the Notebook

Open and run `business_agent.ipynb` in Jupyter or Google Colab:

```bash
jupyter notebook business_agent.ipynb
```

Or for Colab, upload the notebook and run all cells.

### 4. Test the Chatbot

The Gradio interface will launch automatically. Try these examples:

- "What is NeuraVis Technologies?"
- "What services do you offer?"
- "Tell me about your team"
- "I'm interested in AI consulting" (will prompt for contact info)

## 🛠️ Tool Functions

### `record_customer_interest(email, name, message)`

- **Purpose**: Logs customer leads
- **Triggers**: When customer provides contact information
- **Actions**:
  - Saves to `customer_leads.log`
  - Sends push notification

### `record_feedback(question)`

- **Purpose**: Logs unanswered questions
- **Triggers**: When agent doesn't know the answer
- **Actions**:
  - Saves to `customer_feedback.log`
  - Sends push notification

## 📊 Viewing Logs

Logs are created automatically:

- `customer_leads.log` - All customer contact information
- `customer_feedback.log` - Unanswered questions and feedback

View them in the notebook using the last cell, or directly in a text editor.

## 🌐 Deployment to HuggingFace Spaces

### Option 1: Using the Web Interface

1. Go to [HuggingFace Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose "Gradio" as the SDK
4. Upload all files from this project
5. Add `OPENAI_API_KEY` as a secret in Space settings
6. Your app will deploy automatically!

### Option 2: Using Git

```bash
# Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME
cd SPACE_NAME

# Copy files
cp app.py requirements.txt me/ ./

# Push to HuggingFace
git add .
git commit -m "Initial commit"
git push
```

Don't forget to add `OPENAI_API_KEY` in the Space settings!

## 🧪 Testing Tool Calls

To verify the tools are working:

1. Ask: "I'm interested in your services. My name is John Doe and my email is john@example.com"
2. Check `customer_leads.log` for the entry
3. Check your Pushover app for the notification

For feedback testing:

1. Ask: "What's your pricing for enterprise clients?"
2. Check `customer_feedback.log` for the logged question

## 📝 Customization

### Modify Business Information

Edit `me/business_summary.txt` or `me/about_business.pdf` and restart the notebook.

### Change the Model

In both `business_agent.ipynb` and `app.py`, change:

```python
model="gpt-4o-mini"  # Change to gpt-4, gpt-3.5-turbo, etc.
```

### Adjust System Prompt

Modify the `system_prompt` variable to change the agent's behavior.

## 🔑 Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## 📦 Dependencies

- `openai` - OpenAI API client
- `gradio` - Web UI framework
- `requests` - HTTP requests for push notifications
- `PyPDF2` - PDF reading
- `python-dotenv` - Environment variable management

## 🎓 Assignment Checklist

- [x] Two tool functions implemented (`record_customer_interest`, `record_feedback`)
- [x] Push notifications configured
- [x] System prompt created with business context
- [x] OpenAI ChatCompletion with tool calling
- [x] Gradio interface for interaction
- [x] Deployment script (`app.py`) ready for HuggingFace Spaces

## 📞 Support

For issues or questions about NeuraVis Technologies, the agent will log them via the `record_feedback` tool!

---

**Built for EECE 798S - Agentic Systems | Assignment 3**
