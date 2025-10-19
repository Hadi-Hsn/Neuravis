import os
import json
import requests
from datetime import datetime
from openai import OpenAI
import gradio as gr
import PyPDF2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Pushover credentials
pushover_user = os.getenv('PUSHOVER_USER_KEY')
pushover_token = os.getenv('PUSHOVER_TOKEN_KEY')
pushover_url = "https://api.pushover.net/1/messages.json"

# Load business information
def load_business_summary():
    """Load business summary from text file"""
    try:
        with open('me/business_summary.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading business summary: {e}")
        return ""

def load_business_pdf():
    """Load business information from PDF"""
    try:
        with open('me/about_business.pdf', 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return ""

business_summary = load_business_summary()
business_pdf_content = load_business_pdf()

# Push notification function
def push(message):
    """Send push notification via Pushover"""
    print(f"Push: {message}")
    try:
        payload = {
            "user": pushover_user,
            "token": pushover_token,
            "message": message
        }
        response = requests.post(pushover_url, data=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Push notification error: {e}")
        return False

# Tool functions
def record_customer_interest(email, name, message):
    """Record customer interest - logs lead information"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[LEAD] {timestamp} | Name: {name} | Email: {email} | Message: {message}"
    
    # Log to file
    with open('customer_leads.log', 'a', encoding='utf-8') as f:
        f.write(log_message + "\n")
    
    # Send push notification
    push_msg = f"New Lead: {name} ({email}) - {message[:50]}..."
    push(push_msg)
    
    return f"Thank you {name}! We've recorded your interest and will contact you at {email} soon."

def record_feedback(question):
    """Record unanswered questions or feedback"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[FEEDBACK] {timestamp} | Question: {question}"
    
    # Log to file
    with open('customer_feedback.log', 'a', encoding='utf-8') as f:
        f.write(log_message + "\n")
    
    # Send push notification
    push_msg = f"Unanswered Question: {question[:100]}..."
    push(push_msg)
    
    return "I've recorded your question for our team to review. Is there anything else I can help you with?"

# OpenAI tools schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "record_customer_interest",
            "description": "Record a customer's contact information and interest in NeuraVis services. Use when customer wants to learn more, get contacted, or shows interest in our services.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "Customer's email address"
                    },
                    "name": {
                        "type": "string",
                        "description": "Customer's full name"
                    },
                    "message": {
                        "type": "string",
                        "description": "Customer's message, interest area, or specific needs"
                    }
                },
                "required": ["email", "name", "message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "record_feedback",
            "description": "Record questions that you cannot answer or customer feedback. Use when you don't have enough information to answer a question.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question or feedback from the customer"
                    }
                },
                "required": ["question"]
            }
        }
    }
]

# System prompt
system_prompt = f"""You are the AI assistant for NeuraVis Technologies, a company specializing in ethical and transparent AI solutions.

BUSINESS INFORMATION:
{business_summary}

ADDITIONAL DETAILS:
{business_pdf_content if business_pdf_content else 'See summary above'}

YOUR ROLE:
1. Stay in character as NeuraVis's helpful and professional AI representative
2. Answer questions about NeuraVis's mission, services, team, and values
3. When customers show interest, encourage them to share their contact information (name, email, and their needs)
4. Use the record_customer_interest function when they provide their contact details
5. If you don't know the answer to a question, use the record_feedback function to log it
6. Be friendly, concise, and helpful
7. Emphasize NeuraVis's commitment to ethical AI and human-centric solutions

IMPORTANT:
- Always try to answer based on the business information provided
- If asked about pricing, technical details, or specific implementations you're unsure about, record it as feedback
- Actively encourage interested visitors to leave their contact information
"""

# Tool calling function
def call_tool(tool_name, arguments):
    """Execute the requested tool function"""
    if tool_name == "record_customer_interest":
        return record_customer_interest(
            email=arguments.get("email"),
            name=arguments.get("name"),
            message=arguments.get("message")
        )
    elif tool_name == "record_feedback":
        return record_feedback(
            question=arguments.get("question")
        )
    else:
        return "Unknown tool"

# Main chat function
def chat_with_agent(message, history):
    """Main chat function for Gradio interface"""
    # Convert Gradio history format to OpenAI messages format
    messages = [{"role": "system", "content": system_prompt}]
    
    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        if assistant_msg:
            messages.append({"role": "assistant", "content": assistant_msg})
    
    messages.append({"role": "user", "content": message})
    
    try:
        # Initial API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        
        # Check if the model wants to call a tool
        if response_message.tool_calls:
            # Add assistant's response to messages
            messages.append(response_message)
            
            # Process each tool call
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"Calling tool: {function_name} with args: {function_args}")
                
                # Execute the tool
                function_response = call_tool(function_name, function_args)
                
                # Add tool response to messages
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response
                })
            
            # Get final response from the model
            second_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            
            return second_response.choices[0].message.content
        
        else:
            # No tool call needed, return the response
            return response_message.content
            
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        return "I apologize, but I'm experiencing technical difficulties. Please try again."

# Create Gradio interface
demo = gr.ChatInterface(
    fn=chat_with_agent,
    title="NeuraVis Technologies - AI Assistant",
    description="""Welcome to NeuraVis Technologies! 🤖
    
I'm here to help you learn about our ethical AI solutions and services. Feel free to ask me:
- About our mission and values
- What services we offer
- Our team and expertise
- How we can help your organization

If you're interested in working with us, I can collect your contact information!""",
    examples=[
        "What is NeuraVis Technologies?",
        "What services do you offer?",
        "Tell me about your team",
        "How can NeuraVis help my business?",
        "I'm interested in your AI consulting services"
    ],
    theme=gr.themes.Soft()
)

# Launch the app
if __name__ == "__main__":
    demo.launch()
