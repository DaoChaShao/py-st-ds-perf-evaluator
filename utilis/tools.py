from openai import OpenAI
from pdfplumber import open as pdf_open
from re import search
from streamlit import (sidebar, header, selectbox, caption, segmented_control,
                       empty, write, text_input, file_uploader)
from time import perf_counter


def api_key_checker(key: str) -> bool:
    """ Check the API Key """
    if key.startswith("sk-") and len(key) == 35:
        return True


def hyperparams_getter(message: empty) -> dict:
    """ Set and get parameters of the model """
    parameters: dict = {}

    with sidebar:
        header("Model Parameters")
        options_box: list = ["deepseek-chat"]
        model: str = selectbox(
            "Select the LLM", options_box, disabled=True,
            help="Select the Model you want to use"
        )
        caption(f"The model is {model}")

        api_key: str = text_input(
            "API Key", placeholder="Please enter the api key", type="password", max_chars=40,
            help=f"Enter your API Key of {model}"
        )
        if api_key_checker(api_key):
            caption("API Key is valid")

        options_temp = [0.0, 1.3, 1.5]
        temperature: float = segmented_control(
            "Choose the Temperature of the LLM", options_temp, selection_mode="single",
            default=1.5, disabled=True,
            help="Temperature is a hyperparameter that controls randomness of the model")
        match temperature:
            case 0.0:
                caption("For: Coding / Math")
                sys_content: str = "You are a professional coder and mathematician"
            case 1.3:
                caption("For: General Conversation / Chatbot")
                sys_content: str = "You are a helpful assistant"
            case 1.5:
                caption("For: Creative Writing / Evaluation")
                sys_content: str = "You are a senior one Chinese teacher"

        if model not in options_box:
            message.error("Please select a model")
        else:
            parameters["model"] = model
            if api_key == "":
                message.error(f"Please enter the API Key of {model.upper()}")
            else:
                parameters["api_key"] = api_key
                if temperature not in options_temp:
                    message.error("Please choose a Temperature of the LLM you selected")
                else:
                    parameters["temperature"] = temperature
                    parameters["sys_content"] = sys_content

    return parameters


def file_loader() -> str:
    """ This function loads the file from the user """
    uploaded_file = file_uploader("Upload a file", type="PDF", help="Upload a PDF file of a student")
    if uploaded_file:
        with pdf_open(uploaded_file) as doc:
            text = "\n".join([page.extract_text() for page in doc.pages])
            content = text.split("作答明细")[0]
            # write(content)
            return content


def name_getter(content: str) -> str | None:
    """ Get the name of the student """
    match = search(r"(高中语文)\s*([\u4e00-\u9fa5]{2,4})", content)
    if match:
        return match.group(2)
    else:
        return None


def performance_analyzer(name: str, params: dict, content: str) -> str:
    """ Analyze the performance of the student """
    context: str = (f"{params["sys_content"]}."
                    f"Your student {name} has completed the exam."
                    f"The exam level is senior one Chinese."
                    f"The performance of the exam is given in transcript {content}.")
    instruction: str = f"Please giving a creative and constructive evaluation based on the transcript."
    few_shots: str = (f"The evaluation should be started with '亲爱的{name}同学：', using markdown format ** **."
                      f"The title in evaluation body should be used markdown format ** **."
                      f"The evaluation should be ended with '—— KK老师'.")
    words_header: int = 100
    words_body: int = 150
    words_footer: int = 100
    structure: str = (f"The evaluation should consist of five parts."
                      f"1. Summary of the performance without any title, limited within {words_header} words."
                      f"2. '表现优异的地方', limited within {words_body} words."
                      f"3. '需要改进的地方', limited within {words_body} words."
                      f"4. '改进建议', limited within {words_body} words."
                      f"5. '教师总结', limited within {words_footer} words.")
    constraints: str = (f"Your evaluation should be clear, friendly, helpful and positive."
                        f"Do not repeat the student's name in the evaluation.")

    prompt: str = (f"{context}"
                   f"{instruction}"
                   f"{few_shots}"
                   f"{structure}"
                   f"{constraints}")

    return prompt


def deepseek_api_model(params: dict, prompt: str) -> str:
    """ Load Language Model """
    api_key: str = params["api_key"]
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    messages = [
        {"role": "system", "content": params["sys_content"]},
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(
        model=params["model"],
        messages=messages,
        temperature=params["temperature"],
        stream=False)

    return response.choices[0].message.content


class Timer(object):
    """ This class is used for recording the time """

    def __init__(self, description: str, precision: int = 5):
        self._description = description
        self._precision = precision
        self._start = None
        self._end = None
        self._elapsed = None

    def __enter__(self):
        self._start = perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._end = perf_counter()
        self._elapsed = self._end - self._start

    def __repr__(self):
        return f"{self._description} consumes {self._elapsed:.{self._precision}f} seconds"
