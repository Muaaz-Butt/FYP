import requests
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from .schemas import AutomationResponse

class AIService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key="AIzaSyBhods3mtmtY2n1wfCr2IrHM2-6LuM6Gkc"
        )
        self.parser = PydanticOutputParser(pydantic_object=AutomationResponse)

    def fetch_remote_html(self, url):
        """Visits the university portal and grabs the HTML code."""
        try:
            headers = {'User-Agent': 'Mozilla/5.0'} # Pretend to be a browser
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            raise Exception(f"Failed to fetch portal HTML: {str(e)}")

    def extract_form_structure(self, html_content):
        """Simplifies HTML for the LLM."""
        soup = BeautifulSoup(html_content, 'html.parser')
        simplified_elements = []
        for element in soup.find_all(['input', 'select', 'textarea', 'button']):
            info = {
                "tag": element.name,
                "id": element.get('id'),
                "name": element.get('name'),
                "type": element.get('type', 'text'),
                "label": ""
            }
            if element.get('id'):
                lbl = soup.find('label', attrs={'for': element.get('id')})
                if lbl: info["label"] = lbl.get_text().strip()
            simplified_elements.append(info)
        return simplified_elements

    def get_automation_instructions(self, target_url, student_data, app_id):
        # 1. Fetch HTML automatically
        html_content = self.fetch_remote_html(target_url)
        
        # 2. Extract structure
        form_structure = self.extract_form_structure(html_content)
        

        prompt = ChatPromptTemplate.from_template(
            "Map the following student data to the HTML form structure.\n"
            "STUDENT PROFILE:\n{student_data}\n\n"
            "FORM STRUCTURE:\n{form_structure}\n\n"
            "URL: {url}\n"
            "{format_instructions}"
        )

        chain = prompt | self.llm | self.parser
        return chain.invoke({
            "student_data": student_data,
            "form_structure": form_structure,
            "url": target_url,
            "format_instructions": self.parser.get_format_instructions()
        })