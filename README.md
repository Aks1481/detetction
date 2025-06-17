Real-Time Sales Objection Detector + Chatbot
============================================

A Streamlit-based real-time chatbot that detects and categorizes common sales objections using rule-based logic with regex and fallback LLM (OpenAI GPT-3.5). It also suggests responses, logs interactions, and optionally collects customer emails for follow-ups.

🔧 Features
----------
- Detects objections in real-time chat from sales leads (e.g., Price, Timing, Trust)
- Suggests tailored responses for each objection category
- Uses OpenAI GPT-3.5 for fallback objection detection when regex doesn't match
- Logs chat history and email addresses
- Sends a follow-up email after the chat
- Prompts email after 60 seconds of inactivity

🛠️ Tech Stack
-------------
- Python
- Streamlit (Frontend UI)
- OpenAI GPT-3.5 (Fallback LLM)
- smtplib (Email sending)
- Pandas (Logging CSV)
- dotenv (Environment variable handling)

📦 Installation
---------------
1. Clone the repository

2. Install dependencies:
   pip install -r requirements.txt

3. Create a `.env` file in the root directory with the following:
   ```
   OPENAI_API_KEY=your_openai_api_key  
   SMTP_EMAIL=your_email_address  
   SMTP_PASSWORD=your_email_password  
   SMTP_SERVER=smtp.gmail.com  
   SMTP_PORT=587
   ```

4. Run the app:
```
   streamlit run app.py
```
📄 File Structure
----------------
- `app.py` – Main Streamlit application
- `chat_log.csv` – CSV log of conversations
- `emails.csv` – CSV log of collected emails
- `.env` – Environment variables (not committed to GitHub)

📬 Follow-Up Email
------------------
After 60 seconds of user inactivity, the app prompts for an email and sends a follow-up using the configured SMTP server.

📚 Objection Categories
-----------------------
- Price
- Authority
- Need
- Trust
- Timing
- Competition
- General

🤖 Fallback Model
-----------------
If no regex matches, the system queries GPT-3.5 to extract and respond to objections.

🛡️ Disclaimer
-------------
Make sure to securely manage your SMTP and OpenAI keys. Do not expose `.env` or sensitive credentials in public repositories.

📧 Contact
----------
For feedback or contributions, feel free to raise an issue or pull request.

